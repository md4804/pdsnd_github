import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

VALID_CALENDAR_MONTHS = calendar.month_name[1:7]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    month = None
    day = None
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? (case insensitive) ").lower()
        if city not in CITY_DATA:
            print("Invalid input. Please select from Chicago, New York City, or Washington")
        else:
            print()
            break
    
    # get user input for time filter option
    while True:
        filterOption = input("Would you like to filter the data by month, day, or not at all? Type \"none\" for no time filter. ").lower()
        if filterOption not in ['month', 'day', 'none']:
            print("Invalid input. Please select from the available options")
        else:
            break
            

    # get user input for month (all, january, february, ... , june)
    if filterOption == 'month':
        while True:
            month = input("Which month? January, February, March, April, May, or June? ").title()
            if month not in VALID_CALENDAR_MONTHS:
                print("Invalid input. Please select from the available months.")
            else:
                break    


    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif filterOption == 'day':
        while True:
            day = input("Which day of the week? Please type your response as the fulld ay of the week (e.g., Monday) ").title()
            if day not in list(calendar.day_name):
                print("Invalid input. Please select a valid day of the week")
            else:
                break      
    
    month = None if not month else month
    day = None if not day else day


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load all data into a dataframe
    df = pd.read_csv(f"{CITY_DATA[city.lower()]}")


    # If month isn't NULL, filter the dataframe by month
    if month:
        df = df[pd.to_datetime(df['Start Time']).dt.month_name() == month.title()]
    
    # If day isn't NULL, filter the dataframe by day
    if day:
        df = df[pd.to_datetime(df['Start Time']).dt.day_name() == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(f"Most frequent month of travel: {pd.to_datetime(df['Start Time']).dt.month_name().mode()[0]}")

    # display the most common day of week
    print(f"Most common day of travel: {pd.to_datetime(df['Start Time']).dt.day_name().mode()[0]}")

    # display the most common start hour
    print(f"Most popular hour: {pd.to_datetime(df['Start Time']).dt.hour.mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"The most commonly used start station: {df['Start Station'].mode()[0]}")

    # display most commonly used end station
    print(f"The most commonly used end station: {df['End Station'].mode()[0]}")

    # display most frequent combination of start station and end station trip
    most_common_pairing = (df['Start Station'] + ' going to ' + df['End Station']).mode()[0]
    print(f"The most common trip route: {most_common_pairing}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the longest and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display the longest travel time
    longest_time = df['Trip Duration'].max()
    print(f"Longest trip duration: {pd.to_timedelta(longest_time, unit = 's')}")

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print(f"Average trip duration: {pd.to_timedelta(mean_time, unit = 's')}")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df['User Type'].value_counts()
    print(f"Subscribers: {users['Subscriber']: >10}")
    print(f"Customers: {users['Customer']: >12}")

    # Display earliest year of birth (if city is NYC or Chicago)
    if 'Birth Year' in df:
        earliest_year_of_birth = int(df['Birth Year'].min())
        recent_year_of_birth = int(df['Birth Year'].max())
        most_common_year_of_birth = int(df['Birth Year'].mode()[0])

        print()
        print(f"Earliest Year Of Birth: {earliest_year_of_birth: >7}")
        print(f"Most Recent Year Of Birth: {recent_year_of_birth}")
        print(f"Most Common Year Of Birth: {most_common_year_of_birth}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def generator_function(df):
    """Helper generator function that displays the next 5 rows of a dataframe."""
    for i in range(0, len(df), 5):
        yield i


def raw_data(df, generator):
    """ Displays the raw data upon request from the user"""
    index = next(generator)

    if index + 5 >= len(df):
        print(df.iloc[index:])
    else:
        print(df.iloc[index: index + 5])



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        my_gen = generator_function(df)

        while True:
            choice = input("Would you like to see the raw data? Enter yes or no. ").lower()
            if choice != 'yes' and choice != 'no':
                print('Invalid input. Enter yes or no. ')
            elif choice == 'yes':
                raw_data(df, my_gen)
            elif choice == 'no':
                break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()

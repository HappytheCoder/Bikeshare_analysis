import time
import pandas as pd
import numpy as np
from tabulate import tabulate
from colorama import Fore, Back, Style
from datetime import datetime

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    answer_1 = ""
    answer_2 = ""
    answer_3 = ""
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")

    print(
        "\033[1m" + f'{Back.LIGHTYELLOW_EX}{Fore.BLACK}Hello! Let\'s explore some US bike share data!{Style.RESET_ALL}'.center(
            170) + "\033[1m")

    while True:
        try:
            print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")
            city = input(
                f"Please choose a city from the list ({Fore.BLUE}Chicago, New York City, and Washington{Style.RESET_ALL}):")

            city = ' '.join(
                city.split()).lower()  # Standardizing and converting user input to lowercase for consistency

            if city in CITY_DATA.keys():
                # Prompt the user to confirm or change the chosen city for analysis
                while True:
                    try:
                        answer_1 = input(
                            f"You have selected {Fore.BLUE}{city.title()}{Style.RESET_ALL} for analysis. Are you "
                            f"satisfied with your selection? [Y/N]: ").strip()
                        if answer_1.lower() == "y" or answer_1.lower() == "n":

                            break
                        else:
                            print(f"{Fore.RED}Invalid Input.Try Again {Style.RESET_ALL}")

                    except:
                        print(f"{Fore.RED}Error Occurred!!!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid Input.Try Again {Style.RESET_ALL}")

            if answer_1.lower() == "y":
                print(f"{Fore.LIGHTYELLOW_EX}Your input has been accepted!{Style.RESET_ALL}")
                break
        except:
            print(f"{Fore.RED}Error Occurred!!!{Style.RESET_ALL}")

    # get user input for month (all, january, february, ... , june)
    months = ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
              "november", "december"]
    while True:
        try:
            print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")
            # Prompt the user to enter the name of the month for filtering, or 'all' for no month filter
            month = input(
                f"Please enter the name of the month to filter by, or 'all' to apply no month filter:\n"
                f"{Fore.BLUE}({months}){Style.RESET_ALL})\n Enter here:").strip().lower()

            if month in months:
                while True:
                    # Prompt the user to confirm or change the chosen month for analysis
                    try:
                        answer_2 = input(
                            f"You have selected {Fore.BLUE}{month.title()}{Style.RESET_ALL} for analysis. Are you "
                            f"satisfied with your selection? [Y/N]: ").strip()
                        if answer_2.lower() == "y" or answer_2.lower() == "n":

                            break
                        else:
                            print(f"{Fore.RED}Invalid Input.Try Again {Style.RESET_ALL}")

                    except:
                        print(f"{Fore.RED}Error Occurred!!!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid Input.Try Again {Style.RESET_ALL}")

            if answer_2.lower() == "y":
                print(f"{Fore.LIGHTYELLOW_EX}Your input has been accepted!{Style.RESET_ALL}")
                break
        except:
            print(f"{Fore.RED}Error Occurred!!!{Style.RESET_ALL}")

    # get user input for day of week (all, monday, tuesday, ... sunday)

    days_of_week = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    while True:
        try:
            print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")
            # Prompt the user to enter the name of the day for filtering, or 'all' for no day filter
            day = input(
                f"Please enter the name of the day to filter by, or 'all' to apply no day filter:\n"
                f"{Fore.BLUE}({days_of_week}){Style.RESET_ALL})\n Enter here:").strip().lower()

            if day in days_of_week:
                # Prompt the user to confirm or change the chosen day for analysis
                while True:
                    try:
                        answer_3 = input(
                            f"You have selected {Fore.BLUE}{day.title()}{Style.RESET_ALL} for analysis. Are you "
                            f"satisfied with your selection? [Y/N]: ").strip()
                        if answer_3.lower() == "y" or answer_3.lower() == "n":

                            break
                        else:
                            print(f"{Fore.RED}Invalid Input. Please Try Again {Style.RESET_ALL}")

                    except:
                        print(f"{Fore.RED}Error Occurred!!!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid Input.Try Again {Style.RESET_ALL}")

            if answer_3.lower() == "y":
                print(f"{Fore.LIGHTYELLOW_EX}Your input has been accepted!{Style.RESET_ALL}")
                break
        except:
            print(f"{Fore.RED}Error Occurred!!!{Style.RESET_ALL}")

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])
    # extract month, hour and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()
    df["Start Hour"] = df["Start Time"].dt.hour
    # filter by month if applicable
    if month.lower() != "all":
        # first need to extract numerical value of the chosen month
        months = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
                  "october",
                  "november", "december"]
        month = (months.index(month.lower())) + 1  # Adjusting index to match month numbers (starting from 1)

        # Filtering by month to create the new dataframe
        df = df[df["month"] == month]
    # filter by month if applicable
    if day.lower() != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.lower().title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    # Inform the user about the ongoing process of calculating the most frequent times of travel
    print(f'{Fore.GREEN}\nCalculating User Stats...\n{Style.RESET_ALL}')
    start_time = time.time()
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    # Display the most common month
    if df["month"].value_counts().size > 1:
        most_common_month = df["month"].mode().iloc[0]
        most_common_month = months[most_common_month - 1].title()
        print(f"The {Fore.RED}Most Common{Style.RESET_ALL} month of travel is: {most_common_month} \n")
    else:
        print(
            f"{Fore.RED}Since you chose to filter the data set by{Fore.BLUE} {months[df['month'].value_counts().index[0] - 1]}{Fore.RED}, there is "
            f"no single most common month to display. If you prefer, you can start over and choose 'ALL' as your"
            f"filter.{Style.RESET_ALL}\n")

    # Display the most common day of the week
    if df["day_of_week"].value_counts().size > 1:
        most_common_day_of_week = df["day_of_week"].mode().iloc[0]
        print(f"The {Fore.RED}Most Common{Style.RESET_ALL} day of travel is: {most_common_day_of_week} \n")
    else:
        print(
            f"{Fore.RED}Since you chose to filter the data set by{Fore.BLUE} {df['day_of_week'].value_counts().index[0]}{Fore.RED}, there is "
            f"no single most common day to display. If you prefer, you can start over and choose 'ALL' as your "
            f"filter.{Style.RESET_ALL}\n")

    # Display the most common start hour in 12hr time (converting from 24 hr time)
    most_common_start_hour = df["Start Hour"].mode().iloc[0]
    most_common_start_hour = datetime.strptime(str(most_common_start_hour) + ":00", "%H:%M")
    most_common_start_hour = most_common_start_hour.strftime("%I:%M %p")

    print(f"The {Fore.RED}Most Common{Style.RESET_ALL} Start Hour of travel is: {most_common_start_hour} \n")
    # Display the total time taken for the calculations
    print(f"\n{Fore.GREEN}This took %s seconds." % (time.time() - start_time), f"{Style.RESET_ALL}")
    # Display a separator line
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print(f'{Fore.GREEN}\nCalculating User Stats...\n{Style.RESET_ALL}')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].mode().iloc[0]
    print(
        f"The {Fore.LIGHTYELLOW_EX}most Common{Fore.RED} Start Station{Style.RESET_ALL} is: {most_common_start_station}{Style.RESET_ALL} \n")
    # display most commonly used end station
    most_common_end_station = df["End Station"].mode().iloc[0]
    print(
        f"he {Fore.LIGHTYELLOW_EX}most Common{Fore.RED} End Station{Style.RESET_ALL} is: {most_common_end_station} \n")
    # display most frequent combination of start station and end station trip
    # Group the DataFrame by columns 'Start Station' and 'End Station' and calculate the size of each group
    most_common_combination_start_end = df.groupby(["Start Station", "End Station"]).size()

    # Find the most common combination
    most_common_combination_start_end_1 = most_common_combination_start_end.idxmax()

    # Print the most common combination
    # print(most_common_combination_start_end)

    # Access the individual values of the most common combination
    a_value = most_common_combination_start_end_1[0]
    b_value = most_common_combination_start_end_1[1]

    # Print the individual values
    print(
        f"The {Fore.RED}most common combination of start and end station{Style.RESET_ALL} is: {a_value} and  {b_value}")

    print(f"\n{Fore.GREEN}This took %s seconds." % (time.time() - start_time), f"{Style.RESET_ALL}")
    # Display a separator line
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # Inform the user about the ongoing process of calculating the most frequent times of travel
    print(f'{Fore.GREEN}\nCalculating User Stats...\n{Style.RESET_ALL}')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(f"The {Fore.RED}total travel time{Style.RESET_ALL} is: {int(total_travel_time / 3600)} hrs \n")

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print(f"The {Fore.RED}mean travel time{Style.RESET_ALL} is: {int(mean_travel_time / 60)} min \n")

    # Display the total time taken for the calculations
    print(f"\n{Fore.GREEN}This took %s seconds." % (time.time() - start_time), f"{Style.RESET_ALL}")
    # Display a separator line
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bike share users."""

    list_of_column_labels = df.columns.to_list()

    print(f'{Fore.GREEN}\nCalculating User Stats...\n{Style.RESET_ALL}')
    start_time = time.time()

    # Display counts of user types
    if "User Type" in list_of_column_labels:
        user_types = df["User Type"].value_counts()
        print(user_types.to_string())
        print(f"{Fore.GREEN}"'-' * 40, f"{Style.RESET_ALL} ")
    else:
        print(f"{Fore.RED}User Type information is not available for this city{Style.RESET_ALL}")
        print(f"{Fore.GREEN}"'-' * 40, f"{Style.RESET_ALL} ")

    # Display counts of gender
    if "Gender" in list_of_column_labels:

        gender = df["Gender"].value_counts()
        print(gender.to_string())
        print(f"{Fore.GREEN}"'-' * 40, f"{Style.RESET_ALL} ")

    else:

        print(f"{Fore.RED}Gender information is not available for this city{Style.RESET_ALL}")
        print(f"{Fore.GREEN}"'-' * 40, f"{Style.RESET_ALL} ")

    if "Birth Year" in list_of_column_labels:
        # Display earliest, most recent, and most common year of birth
        earliest_dob = df["Birth Year"].min()
        print(f"The {Fore.RED}Earliest{Style.RESET_ALL} year of birth is : {int(earliest_dob)} \n")

        most_recent_dob = df["Birth Year"].max()
        print(f"The {Fore.RED}Most Recent{Style.RESET_ALL} year of birth is : {int(most_recent_dob)} \n")

        most_common_dob = df["Birth Year"].mode()
        print(f"The {Fore.RED}Most Common{Style.RESET_ALL} year of birth is : {int(most_common_dob.iloc[0])} \n")

    else:
        print(f"{Fore.RED}Birth Year information is not available for this city{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}This took %s seconds." % (time.time() - start_time), f"{Style.RESET_ALL}")
    print('-' * 40)


def main():
    """
    This function serves as the main analysis tool for bike share data in the cities of Chicago, New York City,
    and Washington. It invokes various functions to gather user input and deliver a comprehensive, descriptive
    statistical analysis of bike share data for each city.

    Input: None Output: Descriptive statistical analysis for : Start Time stats, Station stats, Trip Duration stats
    and User Type stats
    """

    exit_program = 0  # exit variable

    while exit_program == 0:  # main loop of the main function

        while True:
            # This loop calls the function get_filters() to obtain user input data, and then uses the load_data()
            # function to create a DataFrame. The while loop is used to account for scenarios where users may select
            # filters that result in an empty data frame.
            try:
                city, month, day = get_filters()  # Call the function get_filters() to obtain user's city, month, and day
                # of the week
                # selections for bike share analysis

                df = load_data(city, month, day)  # Calls the function load_data, passing user's city, month, and day
                # selections. This loads the appropriate city file and filters it based on the selected day and month

                df = df.reset_index(drop=True)  # This resets the index labels to start from 0.
                # When the DataFrame is filtered, the index labels may be out of place.

                # checks to see if the loaded data frame based on user's selection is empty or not
                if not df.empty:
                    break
                else:
                    print(
                        f"{Fore.RED}Your filtering criteria resulted in an empty dataset. Please revise your month and "
                        f"day filters accordingly.{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}Error Occurred!!!{Style.RESET_ALL}")

        print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")

        counter = 0  # is a counter variable.
        num_rows_to_show = 5  # is a default value used to show number of rows
        counting = 0
        while True:
            # This loop asks users if they would like to look at the data set,
            # and if yes, it will show them 'num_rows_to_show' at each iteration,
            # until the users ask to stop, or we reach the end of the data frame

            try:
                if counting == 0:
                    look_at_data = input('Would you like to look at the raw data? [Y/N]: ').strip()
                    counting += 1
                else:
                    look_at_data = input(
                        'Would you like to look at the additional rows of the raw data? [Y/N]: ').strip()

                if look_at_data.lower() != "y":
                    look_at_data_2 = input("You have chosen not to look at the data, please confirm [Y/N]:").strip()
                    if look_at_data_2.lower() == "y":
                        print(f"{Fore.LIGHTYELLOW_EX}Your input has been accepted!{Style.RESET_ALL}")
                        break
                else:
                    print(f"{Fore.LIGHTYELLOW_EX}Your input has been accepted!{Style.RESET_ALL}")
                    print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")
                    if counter == 0:
                        counter += 1
                        if len(df) >= num_rows_to_show:
                            print(f"Here is the first {num_rows_to_show} rows of the data set:")
                            print(tabulate(df.head(num_rows_to_show), df.columns))
                        else:
                            print(f"Here is the first {num_rows_to_show} rows of the data set:")
                            print(tabulate(df.head(len(df)), df.columns))
                    else:
                        start_index = num_rows_to_show * counter
                        end_index = num_rows_to_show * (counter + 1)
                        if len(df) >= end_index:
                            print(f"Here are the next {num_rows_to_show} rows of the data set:")
                            print(tabulate(df.iloc[start_index:end_index], df.columns))
                        else:
                            print(
                                f"{Fore.RED}The data frame doesn't have enough rows to display. We will now proceed "
                                f"to descriptive analysis.{Style.RESET_ALL}")

                            time.sleep(5)
                            break
                        counter += 1
            except:
                print(f"{Fore.RED}Error Occurred!!!{Style.RESET_ALL}")

        while True:
            try:
                cont_with_analysis = input('Would you like to continue? [Y/N]: ').strip()
                if cont_with_analysis.lower() == "y":
                    cont_with_analysis_2 = input(
                        "You have chosen to continue with the analysis, please confirm [Y/N]:").strip()
                    if cont_with_analysis_2.lower() == "y":
                        print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")
                        print("Here is the list of available options:")

                        # Create a Series to display the available analysis options
                        Options = pd.Series(
                            data=["Time Stats".ljust(20), "Station Stats".ljust(20), "Trip Duration Stats".ljust(20),
                                  "User Type Stats".ljust(20), "Exit".ljust(20)], index=np.arange(1, 6))

                        print(Options.to_string())
                        print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")

                        analysis_choice = input("Please enter your NUMERICAL selection:")

                        # Check if the entered selection is within the valid range
                        if int(analysis_choice) in list(Options.index):
                            if int(analysis_choice) == 1:
                                # This section calls the function that displays statistics on the most frequent times
                                # of travel
                                print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")
                                print(
                                    f"{Fore.LIGHTYELLOW_EX}Your selection has been accepted. We will now perform:{Fore.BLUE}{Options[int(analysis_choice)]}{Style.RESET_ALL}")
                                time_stats(df)
                            elif int(analysis_choice) == 2:
                                # This section calls the function that displays statistics on the most frequent stations
                                # of travel
                                print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")
                                print(
                                    f"{Fore.LIGHTYELLOW_EX}Your selection has been accepted. We will now perform:{Fore.BLUE}{Options[int(analysis_choice)]}{Style.RESET_ALL}")
                                station_stats(df)
                            elif int(analysis_choice) == 3:
                                # This section calls the function that Displays statistics on the most frequent duration
                                # of travel
                                print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")
                                print(
                                    f"{Fore.LIGHTYELLOW_EX}Your selection has been accepted. We will now perform:{Fore.BLUE}{Options[int(analysis_choice)]}{Style.RESET_ALL}")
                                trip_duration_stats(df)
                            elif int(analysis_choice) == 4:
                                # This section calls the function that Displays statistics user types
                                # of travel
                                print(f"{Fore.GREEN} {'_' * 500}{Style.RESET_ALL}")
                                print(
                                    f"{Fore.LIGHTYELLOW_EX}Your selection has been accepted. We will now perform:{Fore.BLUE}{Options[int(analysis_choice)]}{Style.RESET_ALL}")
                                user_stats(df)
                            elif int(analysis_choice) == 5:
                                break
                        else:
                            print(f"{Fore.RED}You have chosen an invalid option. Please try again!!!{Style.RESET_ALL}")
                    else:

                        break
                else:
                    cont_with_analysis_2 = input(
                        "You have chosen not to continue with the analysis, please confirm [Y/N]:").strip()
                    if cont_with_analysis_2.lower() == "y":
                        break

            except:
                print(f"{Fore.RED}Error Occurred. Please use only numerical values !!!{Style.RESET_ALL}")
        while True:
            # This loop asks the users if they would like to restart or quit

            try:
                restart = input('\nWould you like to restart? [Y/N]:').strip()
                if restart.lower() != 'y':
                    restart_2 = input("You have chosen to exit the program, to confirm please enter [Y/N]:").strip()
                    if restart_2.lower() == "y":
                        exit_program = 1
                        break
                else:
                    break
            except ValueError:
                print(f"{Fore.RED}Error Occurred!!!{Style.RESET_ALL}")

        if exit_program == 1:
            print(f"\n{Fore.LIGHTBLUE_EX}You are now exiting the program. Thank you for using the Bike Share "
                  f"Analysis{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

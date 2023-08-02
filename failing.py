import numpy as np
import csv
import os
from time import sleep
# import call method from subprocess module
from subprocess import call

# define clear function
def clear():
    # check and make call for specific operating system
    _ = call('clear' if os.name == 'posix' else 'cls')

def loadCSVData(fname):
    # Function to load CSV data from the given file name and return it as a li5st of lists.
    datalist = []  # Initialize an empty list to store the data.
    openfile = open(fname)  # Open the file with the given file name.
    csvreader = csv.reader(openfile)  # Create a CSV reader object to read the file.
    for row in csvreader:  # Loop through each row in the CSV file.
        datalist.append(row)  # Append each row to the datalist.
    return datalist  # Return the final list of lists containing the CSV data.

a = np.array(loadCSVData("brdrxingusc_dataset.csv")) # Load the CSV file into a NumPy array called 'a'.

# Remove the 'types' column and transpose the table, so rows represent years and columns represent types.
b = np.array(a.T[1:,], dtype=np.int32)

invalid_input = "Please give a valid input."
quit_message = "Thanks for using this program."
types = a[1:,0]  # Define a list of vehicle types.

def main_menu():
    # Function to display the main menu and handle user choices.
    print("Main menu: Select your choice:\n1. View charts\n2. Show statistics\n3. Quit program")
    menu_input = input("Give your selection here: ")  # Take user input for the menu choice.
    try:
        menu_input = int(menu_input)  # Convert the input to an integer.
        if menu_input == 1:
            clear()
            view_charts()  # If user chose 1, call the view_charts() function.
        elif menu_input == 2:
            clear()
            show_statistics()  # If user chose 2, call the show_statistics() function.
        elif menu_input == 3:
            print(quit_message)  # If user chose 3, print the quit message.
        else:
            print(invalid_input)  # If the input is not valid, print an error message and show the menu again.
            main_menu()
    except:
        clear()
        print(invalid_input)  # If there's an exception in input conversion, print an error message and show the menu again.
        main_menu()

def view_charts():
    # Function to display charts (not implemented in this code).
    print("View charts")  # Placeholder message for chart view (to be implemented).

def show_statistics():
    # Function to show statistics based on user-selected vehicle type.
    print("Select a type:")
    for i in range(len(types)):
        print("{}. {}".format(i+1, types[i]))
    stats_input = input("Give your selection here: ")  # Take user input for the type selection.
    selected_type = types[int(stats_input)-1]  # Get the selected vehicle type based on user input. e.g.: 'buses', 'loaded trucks'
    selected_type_all_years = b[:, int(stats_input)]  # Get the column for the selected vehicle type. e.g.: [4059, 3928, 45986]
    selected_average = np.mean(selected_type_all_years)  # Calculate the average of the selected vehicle type. 
    clear()
    print("Mean number of {types} from {start_year} to {end_year} is {mean}".format(types=selected_type.lower(), start_year = b[0,0], end_year = b[-1,0], mean=int(selected_average)))

    # Find years where the number of types was higher than the average.
    x = np.where(selected_type_all_years > selected_average)
    print("The number of {types} were higher than average in these years:".format(types=selected_type.lower()), end=" ")
    for i in b[x, 0][0]:
        print(i, end=" ")
    print("")

    # Find the maximum number of vehicles and the year when it occurred.
    maximum = selected_type_all_years.max()
    most_year = b[np.where(b == maximum)[0], 0][0]
    print("The highest was {maximum} in {most_year}.".format(maximum=maximum, most_year=most_year))
    custom_range_avg(int(stats_input))  # Call the function to calculate the average for a custom range of years.

def custom_range_avg(selected_type):
    # Function to calculate the average of a custom range of years for a specific vehicle type.
    print("What do you want to do? \n1. Find the average of {} in custom range of years\n2. See the number of {} in a specific year\n3. Back to the main menu\n4. Quit the program".format(types[selected_type-1].lower(),types[selected_type-1].lower()))
    custom_range_input = int(input("Give your selection here: "))  # Take user input for the custom range choice.
    if custom_range_input == 1:
        clear()
        start = int(input("Please give the start year (between {} to {}): ".format(b[0,0], b[-1,0])))  # Take user input for the start year.
        end = int(input("Please give the end year (between {start} to {end_year}, end year will not be included in the average): ".format(start=start, end_year=b[-1,0])))  # Take user input for the end year.
        # Calculate the average number of vehicles for the custom range of years.
        custom_filter = np.mean(b[abs(start) % 100:abs(end) % 100, selected_type])
        print("The average number of {} from {} to {} is {:d}".format(types[selected_type-1].lower(), start, end, int(custom_filter)))
        custom_range_avg(selected_type)  # Call the function again to continue or choose another option.
    elif custom_range_input == 2:
        clear()
        chosen_year = input("Give the year you want to view, from {} to {}: ".format(b[0,0], b[-1,0]))
        chosen_index = int(chosen_year)%100
        print("There was {} {} in {}.".format(b[chosen_index,selected_type], types[selected_type-1].lower(), chosen_year))
        custom_range_avg(selected_type)
    elif custom_range_input == 3:
        clear()
        main_menu()  # Go back to the main menu.
    elif custom_range_input == 4:
        print(quit_message)  # Quit the program.
    else:
        print(invalid_input)  # If the input is not valid, show an error message.

main_menu()  # Start the main program by calling the main_menu() function.
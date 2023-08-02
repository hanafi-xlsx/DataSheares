import numpy as np
import csv
from os import system, name
from time import sleep
# import call method from subprocess module
from subprocess import call
import matplotlib.pyplot as plt
import math

# define clear function
def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 

    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

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

def list_items(items):
    result = ', '.join(str(item) for item in items[:-1])
    return result + ', and ' + str(items[-1])

def input_validation(message:str, stop:int, start:int = 1):
    num = 0
    while True:
        try:
            num = int(input(message))
        except ValueError:
            print("Please enter a valid integer from {} to {}".format(start, stop))
            continue
        if num >= start and num <= stop:
            print(f'You entered: {num}')
            return num
        else:
            print('The integer must be in the range {}-{}'.format(start, stop))
    

def go_to_main_menu():
    print("Going to main menu...")
    sleep(1)
    main_menu()
    
def quit_program():
    print("Quitting program...")
    sleep(1)
    print("Thanks for using DataSheares!")

def main_menu():
    # Function to display the main menu and handle user choices.
    print("Main menu:\n\nSelect your choice:\n1. View charts\n2. Show statistics\n3. Quit program\n")
    menu_input = input_validation("Give your selection here: ", 3)
    match(menu_input):
        case(1):
            clear()
            view_charts()  # If user chose 1, call the view_charts() function.
        case(2):
            clear()
            show_statistics()  # If user chose 2, call the show_statistics() function.
        case(3):
            quit_program()  # If user chose 3, print the quit message.

# Function to display charts
def view_charts():
    print("You selected 'view charts'.")  
    figure, axis = plt.subplots(2,1)
    opacity = 0.5
    error_config = {'ecolor': '0.3'}
    color = 'r'

    # Average number of bus passengers per bus vs year as a line plot
    xpoints_line = b[:,0]
    ypoints_line = b[:,1]/b[:,2]
    heading_font = {'family':'sans','color':'black','size': 15}
    axis[0].grid(axis = 'x')
    axis[0].set_title("Avg. pax per bus over the years", fontdict = heading_font)
    axis[0].plot(xpoints_line, ypoints_line, 
                 color=color, 
                 alpha=opacity, 
                 marker='s', 
                 linestyle="dashed", 
                 linewidth='3.2')

    # Number of personal vehicles vs year as a bar chart
    xpoints_bar = b[:,0]
    ypoints_bar = b[:,3]
    bar_width = 0.7
    bar_limit=[800000,1200000]
    axis[1].set_title("No. of personal vehicles over the years", fontdict = heading_font)
    axis[1].bar(xpoints_bar, ypoints_bar, bar_width,
                 alpha=opacity,
                 color=color,
                 error_kw=error_config,)
    axis[1].set(ylim=bar_limit)
    # using padding
    figure.tight_layout(pad=3.0)
    plt.show()

    print("\nWhat do you want to do? \n1. Show statistics\n2. Main menu\n3. Quit the program\n")
    view_charts_input = input_validation("Give your selection here: ", 3) # Take user input 
    match(view_charts_input):
        case(1):
            clear()
            show_statistics()
        case(2):
            clear()
            main_menu()
        case(3):
            quit_program()

def show_statistics():
    print("You selected 'show statistics'.\n")
    # Function to show statistics based on user-selected vehicle type.
    print("Select a type:")
    for i in range(len(types)):
        print("{}. {}".format(i+1, types[i]))
    stats_input = input_validation("\nGive your selection here: ", len(types)) # Take user input for the type selection.
    selected_type = types[int(stats_input)-1]  # Get the selected vehicle type based on user input. e.g.: 'buses', 'loaded trucks'
    selected_type_all_years = b[:, int(stats_input)]  # Get the column for the selected vehicle type. e.g.: [4059, 3928, 45986]
    selected_average = np.mean(selected_type_all_years)  # Calculate the average of the selected vehicle type. 
    clear()
    print("You selected '{}'\n".format(selected_type))
    print("Mean number of {types} from {start_year} to {end_year} is {mean}".format(types=selected_type.lower(), start_year = b[0,0], end_year = b[-1,0], mean=int(selected_average)))

    # Find years where the number of types was higher than the average.
    x = np.where(selected_type_all_years > selected_average)
    print("The number of {types} were higher than average in these years:".format(types=selected_type.lower()), end=" ")
    print(list_items(b[x, 0][0]))

    # Find the maximum number of vehicles and the year when it occurred.
    maximum = selected_type_all_years.max()
    most_year = b[np.where(b == maximum)[0], 0][0]
    print("The highest was {maximum} in {most_year}.".format(maximum=maximum, most_year=most_year))
    custom_range_avg(int(stats_input))  # Call the function to calculate the average for a custom range of years.

def custom_range_avg(selected_type:int):
    # Function to calculate the average of a custom range of years for a specific vehicle type.
    print("\nWhat do you want to do? \n1. Find the average of {} in custom range of years\n2. See the number of {} in a specific year\n3. Back to the main menu\n4. Quit the program\n".format(types[selected_type-1].lower(),types[selected_type-1].lower()))
    custom_range_input = input_validation("Give your selection here: ", 4) # Take user input for the custom range choice.
    match(custom_range_input):
        case(1):
            clear()
            print("You selected 'Find the average of {} in custom range of years'.\n".format(types[selected_type-1].lower()))
            print("Please give the start year (between {} to {}): ".format(b[0,0], b[-1,0]-1)) # Take user input for the start year.
            start = input_validation("Enter start year: ", b[-1,0]-1, b[0,0])
            print("Please give the end year (between {start} to {end_year}, end year will not be included in the average): ".format(start=start+1, end_year=b[-1,0]))  # Take user input for the end year.
            end = input_validation("Enter end year: ", b[-1,0], start+1)
            # Calculate the average number of vehicles for the custom range of years.
            custom_filter = np.mean(b[abs(start) % 100:abs(end) % 100, selected_type])
            clear()
            print("The average number of {} from {} to {} is {:d}".format(types[selected_type-1].lower(), start, end, int(custom_filter)))
            custom_range_avg(selected_type)  # Call the function again to continue or choose another option.
        case(2):
            clear()
            print("You selected: 'See the number of {} in a specific year'.\n".format(types[selected_type-1].lower()))
            print("Give the year you want to view, from {} to {}: ".format(b[0,0], b[-1,0]))
            chosen_year = input_validation("Select your year: ", b[-1,0], b[0,0])
            chosen_index = int(chosen_year)%100
            clear()
            print("There was {} {} in {}.".format(b[chosen_index,selected_type], types[selected_type-1].lower(), chosen_year))
            custom_range_avg(selected_type)
        case(3):
            clear()
            go_to_main_menu()  # Go back to the main menu.
        case(4):
            quit_program()  # Quit the program.

main_menu()  # Start the main program by calling the main_menu() function.

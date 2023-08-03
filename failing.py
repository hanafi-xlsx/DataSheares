import numpy as np
import csv
from os import system, name
from time import sleep
import matplotlib.pyplot as plt
from typing import List

type_index = None
type_string = None
type_array = None
invalid_input, quit_message, generic_input_message = "Please give a valid input.", "Thanks for using this program.", "Give your selection here: "

"""
this function takes in a file name and returns a datalist containing the file contents

:param file_name:   name of the file
:return:            list of rows, each row is a list
"""
def load_csv_data(file_name:str) -> list:
    # Function to load CSV data from the given file name and return it as a li5st of lists.
    openfile = open(file_name)  # Open the file with the given file name.
    csvreader = csv.reader(openfile)  # Create a CSV reader object to read the file.
    datalist = [row for row in csvreader]  # Initialize an empty list to store the data.
    return datalist  # Return the final list of lists containing the CSV data.

array_raw = np.array(load_csv_data("brdrxingusc_dataset.csv")) # Load the CSV file into a NumPy array called 'array_raw'.
types = array_raw[1:,0]  # Define a list of vehicle types.
array_clean = np.array(array_raw.T[1:,], dtype=np.int32) # Remove 'types' column and transposes the array

# clear() clears the terminal/output
def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 

    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

"""
this function creates a list in proper English when given a list of items

:param items:   a list of items e.g.: [2001, 2002, 2004]
:return:        the given list in proper English e.g.: '2001, 2002 and 2004'
"""
def list_items(items:list) -> str:
    list_length = len(items)
    match(list_length):
        case(1):
            return items[0]
        case(2):
            result = str(items[0]) + " and " + str(items[1])
            return result
        case _:
            result = ', '.join(str(item) for item in items[:-1])    
            return result + ', and ' + str(items[-1])

"""
input_validation() handles input validation for all inputs in this program

:param message: string for input message
:param stop:    last int allowed
:param start:   start int allowed (optional, default value is 1)
"""
def input_validation(message:str, stop:int, start:int = 1, invalids:List[int] = []) -> int:
    num = 0
    while True:
        try:
            num = int(input(message))
        except ValueError:
            print(f"Please enter a valid integer from {start} to {stop}")
            continue
        if num in invalids:
            print(f"'{num}' is an invalid input, please try something else")
        elif num >= start and num <= stop:
            print(f'You entered: {num}')
            return num
        else:
            print(f'The integer must be in the range {start}-{stop}')

def go_to_main_menu():
    print("Going to main menu...")
    sleep(1)
    main_menu()
    
def quit_program():
    print("Quitting program...")
    sleep(1)
    print("Thanks for using DataSheares!")

"""
get_stats() provides statistics for a given array

the array needs to have years in the first column and the type in the second column
"""
def get_stats(array:np.ndarray, type:str):
    mean, max_value = array[:,1].mean(), array.max()
    max_year  = array[np.where(array == max_value)[0], 0][0]
    values_above_avg = list_items(array[np.where(array[:,1] > mean), 0][0])
    print(f'''
    The average number of {type.lower()} from {array[0,0]} to {array[-1,0]} is {round(mean):d}
    The number of {type.lower()} were higher than average in these years: {values_above_avg}
    The highest was {max_value} in {max_year}.
    ''')


"""
main_menu() handles the main menu interface
"""
def main_menu():
    clear()
    # Function to display the main menu and handle user choices.
    print('''
    Main menu
    Select your choice:
    1. View charts
    2. Show statistics
    3. Quit program
    ''')
    menu_input = input_validation(generic_input_message, 3)
    match(menu_input):
        case(1):
            view_charts_menu()  # If user chose 1, call the view_charts_menu() function.
        case(2):
            show_statistics()  # If user chose 2, call the show_statistics() function.
        case(3):
            quit_program()  # If user chose 3, print the quit message.

"""
view_charts_menu() handles the view chart menu interface
"""
def view_charts_menu():
    clear()
    print("You selected 'view charts'.")  
    print('''
    What do you want to do? 
    1. Show assignment charts
    2. See your own desired charts
    3. Back to the main menu
    4. Quit the program
    ''')
    chart_input = input_validation(generic_input_message, 4)
    match(chart_input):
        case(1):
            assignment_charts()
        case(2):
            dynamic_charts()
        case(3):
            main_menu()
        case(4):
            quit_program()

"""
assignment_charts() shows the required statistics that fulfills the assignment specifications
"""
def assignment_charts():
    figure, axis = plt.subplots(2,1)
    opacity, error_config, color = 0.5, {'ecolor': '0.3'}, 'r'

    # Average number of bus passengers per bus vs year as a line plot
    xpoints_line, ypoints_line, heading_font = array_clean[:,0], array_clean[:,1]/array_clean[:,2], {'family':'sans','color':'black','size': 15}
    axis[0].grid(axis = 'x')
    axis[0].set_title("Avg. pax per bus over the years", fontdict = heading_font)
    axis[0].plot(xpoints_line, ypoints_line, 
                color=color, 
                alpha=opacity, 
                marker='s', 
                linestyle="dashed", 
                linewidth='3.2')

    # Number of personal vehicles vs year as a bar chart
    xpoints_bar, ypoints_bar, bar_width, bar_limit = array_clean[:,0], array_clean[:,3], 0.7, [800000,1200000]
    axis[1].set_title("No. of personal vehicles over the years", fontdict = heading_font)
    axis[1].bar(xpoints_bar, ypoints_bar, bar_width,
                alpha=opacity,
                color=color,
                error_kw=error_config,)
    axis[1].set(ylim=bar_limit)

    # using padding
    figure.tight_layout(pad=3.0)
    plt.show()
    view_charts_menu()

"""
dynamic_charts() lets the user dynamically generate their own desired charts from the data
"""
def dynamic_charts():
    global type_index
    clear()
    print("You selected 'See your own desired charts'.")
    print('''
    What kind of data do you want to see? 
    1. Data across the years
    2. Data for a given year
    3. Return to view charts menu
    ''')
    time_input = input_validation(generic_input_message, 3)
    match(time_input):
        # Chosen: data across the years
        case(1):
            clear()
            print("You selected 'Data across the years'")
            print('''
    What kind of data do you want to see? 
    1. Univariate (bar chart for a single datatype)
    2. Bivariate (single-line chart e.g.: Bus passengers per Bus)
    3. Multivariate (multi-line chart)
    4. Return to view charts menu
            ''')
            variable_input = input_validation(generic_input_message, 4)
            match(variable_input):
                # Chosen: Univariate (bar chart, single type)
                case(1):
                    clear()
                    print("You selected 'Univariate (bar chart for a single datatype)'\n\nSelect type:")
                    for idx, type in enumerate(types):
                        print(f"{idx+1}. {type}")
                    type_index = input_validation(generic_input_message, len(types))-1 # Take user input for the type selection.
                    clear()
                    print(f"You selected '{types[type_index]}'\n\n")
                # Chosen: Bivariate (single-line chart e.g.: Bus passengers per Bus)
                case(2):
                    clear()
                    print("You selected 'Bivariate (single-line chart e.g.: Bus passengers per Bus)'\n\n")
                    print("_____ per ______\n\nSelect 1st variable:")
                    for idx, type in enumerate(types):
                        print(f"{idx+1}. {type}")
                    first_type_index = input_validation(generic_input_message, len(types))-1 # Take user input for the type selection.
                    clear()
                    print(f"{types[first_type_index]} per ______\n\nSelect 2nd variable:")
                    for idx, type in enumerate(types):
                        if idx == first_type_index:
                            print(f"{idx+1}. {type} (already selected)")
                        else:
                            print(f"{idx+1}. {type}")
                    second_type_index = input_validation(generic_input_message, len(types), invalids=[first_type_index+1])-1 # Take user input for the type selection.
                    clear()
                    print(f"You have selected:\n\n{types[first_type_index]} per {types[second_type_index]}")
                # Chosen: Multivariate (multi-line chart, multiple types)
                case(3):
                    clear()
                    print("You selected 'Multivariate (multi-line chart for multiple datatypes)'\n\n")
                    """
                    TO-DO!!! create a multi-option input because user can pick as many types as they want
                    """
                # Chosen: return to view charts menu
                case(4):
                    view_charts_menu()

        # Chosen: data for a given year
        case(2):
            clear()
            print("You selected 'Data for a given year'")
            print('''
    What kind of chart do you want to see?
    1. Bar chart (comparison)
    2. Pie chart (composition)
    3. Return to view charts menu
            ''')
            chart_input = input_validation(generic_input_message, 3)
            match(chart_input):
                # Chosen: Bar chart (comparison)
                case(1):
                    clear()
                    print("You selected 'Bar chart (comparison)'")
                # Chosen: Pie chart (composition)
                case(2):
                    clear()
                    print("You selected 'Pie chart (composition)'")
                # Chosen: return to view charts menu
                case(3):
                    view_charts_menu()
            print(f"Available years: {array_clean[0,0]} - {array_clean[-1,0]}. What year would you like to view?")
            year_input = input_validation(generic_input_message, array_clean[-1,0], array_clean[0,0])
            print(year_input)
        # Chosen: return to view charts menu
        case(3):
            view_charts_menu()

"""
show_statistics() asks the user to pick a type then shows statistics for a single type throughout the years
"""
def show_statistics():
    global type_index
    global type_string
    clear()
    print("You selected 'show statistics'.\n")
    
    # Function to show statistics based on user-selected vehicle type.
    print("Select a type:")
    for idx, type in enumerate(types):
        print(f"{idx+1}. {type}")
    
    type_index = input_validation(generic_input_message, len(types))-1 # Take user input for the type selection.
    
    type_string, selected_type_array = types[type_index], array_clean[:, [0,type_index+1]]
    
    clear()
    print(f"You selected '{type_string}'")
    get_stats(selected_type_array, type_string)
    statistics_menu()  # Call the statistics_menu function

"""
statistics_menu() handles the statistics menu functionality
"""
def statistics_menu():
    global type_string

    # Function to calculate the average of a custom range of years for a specific vehicle type.
    print(f'''
    What do you want to do? 
    1. Show statistics for {types[type_index].lower()} in custom range of years
    2. See the number of {types[type_index].lower()} in a specific year
    3. Back to the main menu
    4. Quit the program
    ''')
    custom_range_input = input_validation(generic_input_message, 4) # Take user input for the custom range choice.

    match(custom_range_input):
        case(1):
            custom_year_statistics()
        case(2):
            clear()
            print(f"You selected: 'See the number of {type_string.lower()} in a specific year'.\n")

            print(f"Give the year you want to view, from {array_clean[0,0]} to {array_clean[-1,0]}: ")
            chosen_year = input_validation("Select your year: ", array_clean[-1,0], array_clean[0,0])
            chosen_index = chosen_year%100

            clear()
            print(f"There was {array_clean[chosen_index,type_index+1]} {types[type_index].lower()}"
                  f" in {chosen_year}.")
            statistics_menu()
        case(3):
            go_to_main_menu()  # Go back to the main menu.
        case(4):
            quit_program()  # Quit the program.

"""
custom_year_statistics() shows statistics for a single type for a custom range of years
"""
def custom_year_statistics():
    global type_index
    global type_string

    clear()
    print(f"You selected 'Show statistics for {type_string} in custom range of years'.\n")

    print(f"Please give the start year (between {array_clean[0,0]} to {array_clean[-1,0]-1}): ") # Take user input for the start year.
    start = input_validation("Enter start year: ", array_clean[-1,0]-1, array_clean[0,0])
    
    print(f"Please give the end year (between {start+1} to {array_clean[-1,0]},"
            " end year will be included in the average): ")  # Take user input for the end year.
    end = input_validation("Enter end year: ", array_clean[-1,0], start+1)
    
    custom_filter = array_clean[abs(start) % 100:abs(end+1) % 100, [0,type_index+1]]
    clear()
    get_stats(custom_filter, type_string)
    statistics_menu()

main_menu()  # Start the main program by calling the main_menu() function.

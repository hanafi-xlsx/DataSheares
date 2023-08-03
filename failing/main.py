import numpy as np
from time import sleep
from utils import input_validation, clear, load_csv_data
from charts import assignment_charts, dynamic_charts
from stats import get_stats
from quit import quit_program

type_index = None
type_string = None
type_array = None
quit_message = "Thanks for using this program."
array_raw = np.array(load_csv_data("brdrxingusc_dataset.csv")) # Load the CSV file into a NumPy array called 'array_raw'.
types = array_raw[1:,0]  # Define a list of vehicle types.
array_clean = np.array(array_raw.T[1:,], dtype=np.int32) # Remove 'types' column and transposes the array


def go_to_main_menu():
    print("Going to main menu...")
    sleep(1)
    main_menu()

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
    menu_input = input_validation(3)
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
    chart_input = input_validation(4)
    match(chart_input):
        case(1):
            assignment_charts(array_clean)
            view_charts_menu()
        case(2):
            dynamic_charts(array_clean, types)
            view_charts_menu()
        case(3):
            main_menu()
        case(4):
            quit_program()

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
    
    type_index = input_validation(len(types))-1 # Take user input for the type selection.
    
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
    custom_range_input = input_validation(4) # Take user input for the custom range choice.

    match(custom_range_input):
        case(1):
            custom_year_statistics()
        case(2):
            clear()
            print(f"You selected: 'See the number of {type_string.lower()} in a specific year'.\n")

            print(f"Give the year you want to view, from {array_clean[0,0]} to {array_clean[-1,0]}: ")
            chosen_year = input_validation(array_clean[-1,0], message="Select your year: ", start=array_clean[0,0])
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
    start = input_validation(array_clean[-1,0]-1, message="Enter start year: ", start=array_clean[0,0])
    
    print(f"Please give the end year (between {start+1} to {array_clean[-1,0]},"
            " end year will be included in the average): ")  # Take user input for the end year.
    end = input_validation(array_clean[-1,0], message="Enter end year: ", start=start+1)
    
    custom_filter = array_clean[abs(start) % 100:abs(end+1) % 100, [0,type_index+1]]
    clear()
    get_stats(custom_filter, type_string)
    statistics_menu()

main_menu()  # Start the main program by calling the main_menu() function.
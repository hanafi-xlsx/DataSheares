from pipinstall import install_pip_libraries
install_pip_libraries()
from time import sleep
from welcome import welcome_window
from utils import clear, load_csv_data, show_message, confirm_exit, get_csv_file, validation_function, play_audio
from charts import assignment_charts, dynamic_charts
from stats import get_stats, list_items
from tabulate import tabulate
import os
import sys
import subprocess
import numpy as np
import inquirer

type_index, type_string, type_array = None, None, None
quit_message = "Thanks for using this program."

def go_to_main_menu():
    print("Going to main menu...")
    sleep(1)
    main_menu()

"""
main_menu() handles the main menu interface
"""
def main_menu():
    clear()
    print("Welcome to DataSheares. This is the main menu.\n")
    main_menu = inquirer.list_input("Select your choice",
                    choices=[('View charts',1), ('Show statistics',2), ('Quit program',3)],
                    carousel=True)
    match(main_menu):
        case(1):
            view_charts_menu()  # If user chose 1, call the view_charts_menu() function.
        case(2):
            show_statistics()  # If user chose 2, call the show_statistics() function.
        case(3):
            quit_program()  # If user chose 4, print the quit message.

def retrieve_data():
    global types, array_clean
    file_path, types, array_clean = None, None, None
    while not file_path:
        file_path = get_csv_file("Please select your .csv file.")
        if not file_path:
            confirm_exit()
    try:
        array_raw = np.array(load_csv_data(file_path)) # Load the CSV file into a NumPy array called 'array_raw'.
        types = array_raw[1:,0]  # Define a list of vehicle types.
        array_clean = np.array(array_raw.T[1:,], dtype=np.int32) # Remove 'types' column and transposes the array   
    except:
        show_message(2, "Error", "Invalid .csv file.")
        return retrieve_data()
    play_audio("orb")
    main_menu()

"""
view_charts_menu() handles the view chart menu interface
"""
def view_charts_menu():
    clear()
    print("You selected 'view charts'.\n")  
    charts_menu = inquirer.list_input("What do you want to do?",
                    choices=[('Show assignment charts',1), ('See your own desired charts',2), ('Back to the main menu',3), ('Quit program',4)],
                    carousel=True)
    match(charts_menu):
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
    global type_strings
    global type_menu
    clear()
    print("You selected 'Show statistics'.\n")
    # Function to show statistics based on user-selected vehicle type.
    type_menu = inquirer.checkbox("Select a type",
                        choices=[(type, idx) for idx, type in enumerate(types)],
                        carousel=True,
                        validate=validation_function)
    type_menu.sort()
    type_strings = 0
    while type_strings == 0:
        type_strings = list_items([types[i] for i in type_menu])
    type_menu = [x+1 for x in type_menu]
    type_menu.insert(0,0)
    selected_type_array = array_clean[:, type_menu]
    clear()
    print(f"You selected '{type_strings}'")
    print(f"Statistics for {type_strings.lower()} from {array_clean[0,0]} to {array_clean[-1,0]}")
    get_stats(selected_type_array, [types[i-1] for i in type_menu if i!=0])
    statistics_menu()  # Call the statistics_menu function

"""
statistics_menu() handles the statistics menu functionality
"""
def statistics_menu():
    global type_string

    stats_menu = inquirer.list_input("Select a type",
                    choices=[(f"Show statistics for {type_strings.lower()} in custom range of years", 1), (f"See the number of {type_strings.lower()} in a specific year",2), ("Back to the main menu",3), ("Quit program",4)],
                    carousel=True)

    match(stats_menu):
        case(1):
            custom_year_statistics()
        case(2):
            clear()
            print(f"You selected: 'See the number of {type_strings.lower()} in a specific year'.\n")

            year_select = inquirer.checkbox(f"Give the year you want to view, from {array_clean[0,0]} to {array_clean[-1,0]}",
                            choices=[i for i in range(array_clean[0,0], array_clean[-1,0]+1)],
                            carousel=True,
                            validate=validation_function)
            
            chosen_years = year_select
            chosen_indexes = [year%100 for year in chosen_years]
            chosen_years_array = np.array(array_clean[chosen_indexes, :])
            chosen_years_array = chosen_years_array[:, type_menu]
            headers = [types[i-1] for i in type_menu if i!=0]
            headers.insert(0,'Year')
            clear()
            print(tabulate(chosen_years_array, headers=headers, tablefmt="rounded_grid"))
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
    global type_strings

    clear()
    print(f"You selected 'Show statistics for {type_strings.lower()} in custom range of years'.\n")

    start = inquirer.list_input(f"Please give the start year (between {array_clean[0,0]} to {array_clean[-1,0]-1})",
                choices=[i for i in range(array_clean[0,0], array_clean[-1,0])],
                carousel=True)
    
    end = inquirer.list_input(f"Please give the end year (between {start+1} to {array_clean[-1,0]})",
                choices=[i for i in range(start+1, array_clean[-1,0]+1)],
                carousel=True)
    custom_filter = array_clean[abs(start) % 100:abs(end+1) % 100, type_menu]
    clear()
    print(f"Statistics for {type_strings.lower()} from {start} to {end}")
    get_stats(custom_filter, [types[i-1] for i in type_menu if i!=0])
    statistics_menu()

def quit_program():
    clear()
    play_audio("click")
    current_folder = os.getcwd()
    subprocess.run(['python', 'quit.py'], stderr=subprocess.DEVNULL, shell=True,  cwd=current_folder)
    sys.exit()

clear()
welcome_window()
retrieve_data()
main_menu()  # Start the main program by calling the main_menu() function.
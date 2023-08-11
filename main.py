from time import sleep
from disposable import welcome_window
from utils import clear, get_data
from charts import assignment_charts, dynamic_charts
from stats import get_stats, list_items
from quit import quit_program
from tabulate import tabulate
from PIL import Image, ImageTk
import tkinter as tk
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
    print("Welcome to DataSheares. This is the main menu.\n")
    main_menu = inquirer.list_input("Select your choice",
                    choices=[('View charts',1), ('Show statistics',2), ('Re-select data',3), ('Quit program',4)],
                    carousel=True)
    match(main_menu):
        case(1):
            view_charts_menu()  # If user chose 1, call the view_charts_menu() function.
        case(2):
            show_statistics()  # If user chose 2, call the show_statistics() function.
        case(3):
            retrieve_data()  # If user chose 3, select a new .csv file to unpack.
        case(4):
            quit_program()  # If user chose 4, print the quit message.

def retrieve_data():
    global types, array_clean
    types, array_clean = get_data()
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
                        carousel=True)
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

            year_select = inquirer.list_input(f"Give the year you want to view, from {array_clean[0,0]} to {array_clean[-1,0]}",
                            choices=[i for i in range(array_clean[0,0], array_clean[-1,0]+1)],
                            carousel=True)
            
            chosen_year = year_select
            chosen_index = chosen_year%100
            values = array_clean[chosen_index, type_menu]
            headers = [types[i-1] for i in type_menu if i!=0]
            headers.insert(0,'Year')
            clear()
            print(tabulate([[round(x) for x in values]], headers=headers, tablefmt="rounded_grid"))
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

welcome_window()
retrieve_data()
main_menu()  # Start the main program by calling the main_menu() function.
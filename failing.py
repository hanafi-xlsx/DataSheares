import numpy as np
import csv
from os import system, name
from time import sleep
import matplotlib.pyplot as plt

invalid_input, quit_message, generic_input_message = "Please give a valid input.", "Thanks for using this program.", "Give your selection here: "

# define clear function
def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 

    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def load_csv_data(fname:str) -> list:
    # Function to load CSV data from the given file name and return it as a li5st of lists.
    openfile = open(fname)  # Open the file with the given file name.
    csvreader = csv.reader(openfile)  # Create a CSV reader object to read the file.
    datalist = [row for row in csvreader]  # Initialize an empty list to store the data.
    return datalist  # Return the final list of lists containing the CSV data.

array_raw = np.array(load_csv_data("brdrxingusc_dataset.csv")) # Load the CSV file into a NumPy array called 'array_raw'.
types = array_raw[1:,0]  # Define a list of vehicle types.

# Remove the 'types' column and transpose the array, so rows represent years and columns represent types.
array_clean = np.array(array_raw.T[1:,], dtype=np.int32)


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

def input_validation(message:str, stop:int, start:int = 1) -> int:
    num = 0
    while True:
        try:
            num = int(input(message))
        except ValueError:
            print(f"Please enter a valid integer from {start} to {stop}")
            continue
        if num >= start and num <= stop:
            print(f'You entered: {num}')
            return num
        else:
            print(f'The integer must be in the range {start}-{stop}')

def get_stats(array:np.ndarray, type:str):
    mean, max_value = array[:,1].mean(), array.max()
    max_year  = array[np.where(array == max_value)[0], 0][0]
    values_above_avg = list_items(array[np.where(array[:,1] > mean), 0][0])
    print(f'''
    The average number of {type.lower()} from {array[0,0]} to {array[-1,0]} is {round(mean):d}
    The number of {type.lower()} were higher than average in these years: {values_above_avg}
    The highest was {max_value} in {max_year}.
    ''')

def go_to_main_menu():
    print("Going to main menu...")
    sleep(1)
    main_menu()
    
def quit_program():
    print("Quitting program...")
    sleep(1)
    print("Thanks for using DataSheares!")

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
            view_charts()  # If user chose 1, call the view_charts() function.
        case(2):
            show_statistics()  # If user chose 2, call the show_statistics() function.
        case(3):
            quit_program()  # If user chose 3, print the quit message.

# Function to display charts
def view_charts():
    clear()
    print("You selected 'view charts'.")  
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

    print('''
    What do you want to do?
        1. Show statistics
        2. Main menu
        3. Quit the program
          ''')
    view_charts_input = input_validation(generic_input_message, 3) # Take user input 
    
    match(view_charts_input):
        case(1):
            show_statistics()
        case(2):
            main_menu()
        case(3):
            quit_program()

def show_statistics():
    clear()
    print("You selected 'show statistics'.\n")
    
    # Function to show statistics based on user-selected vehicle type.
    print("Select a type:")
    for idx, type in enumerate(types):
        print(f"{idx+1}. {type}")
    
    input_type_index = input_validation(generic_input_message, len(types)) # Take user input for the type selection.
    
    selected_type_string, selected_type_array = types[input_type_index-1], array_clean[:, [0,input_type_index]]
    
    clear()
    print(f"You selected '{selected_type_string}'")
    get_stats(selected_type_array, selected_type_string)
    custom_range_avg(input_type_index)  # Call the custom_range_avg function

def custom_range_avg(selected_type_index:int):
    # Function to calculate the average of a custom range of years for a specific vehicle type.
    print(f'''
    What do you want to do? 
    1. Show statistics for {types[selected_type_index-1].lower()} in custom range of years
    2. See the number of {types[selected_type_index-1].lower()} in a specific year
    3. Back to the main menu
    4. Quit the program
    ''')
    custom_range_input = input_validation(generic_input_message, 4) # Take user input for the custom range choice.
    selected_type_string = types[selected_type_index-1]

    match(custom_range_input):
        case(1):
            clear()
            print(f"You selected 'Show statistics for {selected_type_string} in custom range of years'.\n")

            print(f"Please give the start year (between {array_clean[0,0]} to {array_clean[-1,0]-1}): ") # Take user input for the start year.
            start = input_validation("Enter start year: ", array_clean[-1,0]-1, array_clean[0,0])
            
            print(f"Please give the end year (between {start+1} to {array_clean[-1,0]},"
                  " end year will be included in the average): ")  # Take user input for the end year.
            end = input_validation("Enter end year: ", array_clean[-1,0], start+1)
            
            custom_filter = array_clean[abs(start) % 100:abs(end+1) % 100, [0,selected_type_index]]
            clear()
            get_stats(custom_filter, selected_type_string)
            custom_range_avg(selected_type_index)
        case(2):
            clear()
            print(f"You selected: 'See the number of {types[selected_type_index-1].lower()} in a specific year'.\n")

            print(f"Give the year you want to view, from {array_clean[0,0]} to {array_clean[-1,0]}: ")
            chosen_year = input_validation("Select your year: ", array_clean[-1,0], array_clean[0,0])
            chosen_index = chosen_year%100

            clear()
            print(f"There was {array_clean[chosen_index,selected_type_index]} {types[selected_type_index-1].lower()}"
                  f" in {chosen_year}.")
            custom_range_avg(selected_type_index)
        case(3):
            go_to_main_menu()  # Go back to the main menu.
        case(4):
            quit_program()  # Quit the program.

main_menu()  # Start the main program by calling the main_menu() function.

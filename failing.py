import numpy as np
import csv
from os import system, name
from time import sleep
import matplotlib.pyplot as plt

# define clear function
def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 

    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def load_csv_data(fname):
    # Function to load CSV data from the given file name and return it as a li5st of lists.
    datalist = []  # Initialize an empty list to store the data.
    openfile = open(fname)  # Open the file with the given file name.
    csvreader = csv.reader(openfile)  # Create a CSV reader object to read the file.
    for row in csvreader:  # Loop through each row in the CSV file.
        datalist.append(row)  # Append each row to the datalist.
    return datalist  # Return the final list of lists containing the CSV data.

array_raw = np.array(load_csv_data("brdrxingusc_dataset.csv")) # Load the CSV file into a NumPy array called 'a'.

# Remove the 'types' column and transpose the table, so rows represent years and columns represent types.
array_clean = np.array(array_raw.T[1:,], dtype=np.int32)

invalid_input = "Please give a valid input."
quit_message = "Thanks for using this program."
types = array_raw[1:,0]  # Define a list of vehicle types.
generic_input_message = "Give your selection here: "

def list_items(items):
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

def get_stats(array:np.ndarray, type:str):
    mean = array[:,1].mean()
    max_value = array.max()
    max_year = array[np.where(array == max_value)[0], 0][0]
    values_above_avg = list_items(array[np.where(array[:,1] > mean), 0][0])
    print("The average number of {} from {} to {} is {:d}".format(type.lower(), array[0,0], array[-1,0], int(mean)))
    print("The number of {} were higher than average in these years: {}".format(type.lower(), values_above_avg))
    print("The highest was {value} in {year}.".format(value=max_value, year=max_year))

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
    menu_input = input_validation(generic_input_message, 3)
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
    xpoints_line = array_clean[:,0]
    ypoints_line = array_clean[:,1]/array_clean[:,2]
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
    xpoints_bar = array_clean[:,0]
    ypoints_bar = array_clean[:,3]
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
    view_charts_input = input_validation(generic_input_message, 3) # Take user input 
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
    input_type_index = input_validation(generic_input_message, len(types)) # Take user input for the type selection.
    selected_type_string = types[int(input_type_index)-1]  # Get the selected vehicle type based on user input. e.g.: 'buses', 'loaded trucks'
    selected_type_array = array_clean[:, [0,int(input_type_index)]]  # Get the column for the selected vehicle type. e.g.: [4059, 3928, 45986]
    clear()
    print("You selected '{}'\n".format(selected_type_string))
    get_stats(selected_type_array, selected_type_string)
    custom_range_avg(int(input_type_index))  # Call the custom_range_avg function

def custom_range_avg(selected_type_index:int):
    # Function to calculate the average of a custom range of years for a specific vehicle type.
    print("\nWhat do you want to do? \n1. Show statistics for {} in custom range of years\n2. See the number of {} in a specific year\n3. Back to the main menu\n4. Quit the program\n".format(types[selected_type_index-1].lower(),types[selected_type_index-1].lower()))
    custom_range_input = input_validation(generic_input_message, 4) # Take user input for the custom range choice.
    selected_type_string = types[int(selected_type_index)-1]
    match(custom_range_input):
        case(1):
            clear()
            print("You selected 'Show statistics for {} in custom range of years'.\n".format(selected_type_string))
            print("Please give the start year (between {} to {}): ".format(array_clean[0,0], array_clean[-1,0]-1)) # Take user input for the start year.
            start = input_validation("Enter start year: ", array_clean[-1,0]-1, array_clean[0,0])
            print("Please give the end year (between {start} to {end_year}, end year will not be included in the average): ".format(start=start+1, end_year=array_clean[-1,0]))  # Take user input for the end year.
            end = input_validation("Enter end year: ", array_clean[-1,0], start+1)
            custom_filter = array_clean[abs(start) % 100:abs(end) % 100, [0,selected_type_index]]
            clear()
            get_stats(custom_filter, selected_type_string)
            custom_range_avg(selected_type_index)
        case(2):
            clear()
            print("You selected: 'See the number of {} in a specific year'.\n".format(types[selected_type_index-1].lower()))
            print("Give the year you want to view, from {} to {}: ".format(array_clean[0,0], array_clean[-1,0]))
            chosen_year = input_validation("Select your year: ", array_clean[-1,0], array_clean[0,0])
            chosen_index = int(chosen_year)%100
            clear()
            print("There was {} {} in {}.".format(array_clean[chosen_index,selected_type_index], types[selected_type_index-1].lower(), chosen_year))
            custom_range_avg(selected_type_index)
        case(3):
            clear()
            go_to_main_menu()  # Go back to the main menu.
        case(4):
            quit_program()  # Quit the program.

main_menu()  # Start the main program by calling the main_menu() function.

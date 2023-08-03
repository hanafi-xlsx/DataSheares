import matplotlib.pyplot as plt
from utils import clear, input_validation
import numpy as np

"""
assignment_charts() shows the required statistics that fulfills the assignment specifications
"""
def assignment_charts(array: np.ndarray):
    figure, axis = plt.subplots(2,1)
    opacity, error_config, color = 0.5, {'ecolor': '0.3'}, 'r'

    # Average number of bus passengers per bus vs year as a line plot
    xpoints_line, ypoints_line, heading_font = array[:,0], array[:,1]/array[:,2], {'family':'sans','color':'black','size': 15}
    axis[0].grid(axis = 'x')
    axis[0].set_title("Avg. pax per bus over the years", fontdict = heading_font)
    axis[0].plot(xpoints_line, ypoints_line, 
                color=color, 
                alpha=opacity, 
                marker='s', 
                linestyle="dashed", 
                linewidth='3.2')

    # Number of personal vehicles vs year as a bar chart
    xpoints_bar, ypoints_bar, bar_width, bar_limit = array[:,0], array[:,3], 0.7, [800000,1200000]
    axis[1].set_title("No. of personal vehicles over the years", fontdict = heading_font)
    axis[1].bar(xpoints_bar, ypoints_bar, bar_width,
                alpha=opacity,
                color=color,
                error_kw=error_config,)
    axis[1].set(ylim=bar_limit)

    # using padding
    figure.tight_layout(pad=3.0)
    plt.show()

"""
dynamic_charts() lets the user dynamically generate their own desired charts from the data

WORK IN PROGRESS
"""
def dynamic_charts(array: np.ndarray, types: np.ndarray):
    global type_index
    clear()
    print("You selected 'See your own desired charts'.")
    print('''
    What kind of data do you want to see? 
    1. Data across the years
    2. Data for a given year
    3. Return to view charts menu
    ''')
    time_input = input_validation(3)
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
            variable_input = input_validation(4)
            match(variable_input):
                # Chosen: Univariate (bar chart, single type)
                case(1):
                    clear()
                    print("You selected 'Univariate (bar chart for a single datatype)'\n\nSelect type:")
                    for idx, type in enumerate(types):
                        print(f"{idx+1}. {type}")
                    type_index = input_validation(len(types))-1 # Take user input for the type selection.
                    clear()
                    print(f"You selected '{types[type_index]}'\n\n")
                # Chosen: Bivariate (single-line chart e.g.: Bus passengers per Bus)
                case(2):
                    clear()
                    print("You selected 'Bivariate (single-line chart e.g.: Bus passengers per Bus)'\n\n")
                    print("_____ per ______\n\nSelect 1st variable:")
                    for idx, type in enumerate(types):
                        print(f"{idx+1}. {type}")
                    first_type_index = input_validation(len(types))-1 # Take user input for the type selection.
                    clear()
                    print(f"{types[first_type_index]} per ______\n\nSelect 2nd variable:")
                    for idx, type in enumerate(types):
                        if idx == first_type_index:
                            print(f"{idx+1}. {type} (already selected)")
                        else:
                            print(f"{idx+1}. {type}")
                    second_type_index = input_validation(len(types), invalids=[first_type_index+1])-1 # Take user input for the type selection.
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
                    return

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
            chart_input = input_validation(3)
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
                    return
            print(f"Available years: {array[0,0]} - {array[-1,0]}. What year would you like to view?")
            year_input = input_validation(array[-1,0], start=array[0,0])
            print(year_input)
        # Chosen: return to view charts menu
        case(3):
            return
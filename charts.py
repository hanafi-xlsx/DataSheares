import matplotlib.pyplot as plt
import numpy as np
import inquirer
from utils import clear, validation_function
from stats import list_items

heading_font = {'family':'sans','color':'black','size': 15}
opacity, error_config, color = 0.5, {'ecolor': '0.3'}, 'r'
marker, linestyle, linewidth = "s", "dashed", "3.2"
bar_width = 0.7
return_message = "Return to view charts menu."

"""
assignment_charts() shows the required statistics that fulfills the assignment specifications
"""
def assignment_charts(array: np.ndarray):
    figure, axis = plt.subplots(2,1)

    # Average number of bus passengers per bus vs year as a line plot
    xpoints_line, ypoints_line, = array[:,0], array[:,1]/array[:,2]
    axis[0].grid(axis = 'x')
    axis[0].set_title("Avg. pax per bus over the years", fontdict = heading_font)
    axis[0].plot(xpoints_line, ypoints_line, 
                color=color, 
                alpha=opacity, 
                marker=marker, 
                linestyle=linestyle, 
                linewidth=linewidth)

    # Number of personal vehicles vs year as a bar chart
    xpoints_bar, ypoints_bar, bar_limit = array[:,0], array[:,3], [800000,1200000]
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
"""
def dynamic_charts(array: np.ndarray, types: np.ndarray):
    global type_index
    clear()
    print("You selected 'See your own desired charts'.\n")
    time_input = inquirer.list_input("What kind of data do you want to see?",
                    choices=[("Data across the years",1),("Data for a given year",2),(return_message,3)],
                    carousel=True)
    match(time_input):
        # Chosen: data across the years
        case(1):
            clear()
            xpoints = array[:,0]
            print("You selected 'Data across the years'\n")
            variable_input = inquirer.list_input("What kind of data do you want to see?",
                                choices=[("Univariate (line chart for a single datatype)",1),("Bivariate (single-line chart e.g.: Bus passengers per Bus)",2),("Multivariate (multi-line chart)",3),(return_message,4)],
                                carousel=True)
            match(variable_input):
                # Chosen: Univariate (line chart, single type)
                case(1):
                    clear()
                    print("You selected 'Univariate (line chart for a single datatype)'\n")
                    type_index = inquirer.list_input("Select type",
                                    choices=[(type, idx) for idx, type in enumerate(types)],
                                    carousel=True)
                    clear()
                    print(f"You selected '{types[type_index]}'\n")
                    ypoints = array[:,type_index+1]
                    plt.plot(xpoints, ypoints,
                            color=color, 
                            alpha=opacity, 
                            marker=marker, 
                            linestyle=linestyle, 
                            linewidth=linewidth,
                            )
                    plt.ylabel(types[type_index])
                    plt.xlabel('Year')
                    plt.title(f"No. of {types[type_index].lower()} crossing over the years", fontdict = heading_font)
                    plt.show()
                # Chosen: Bivariate (single-line chart e.g.: Bus passengers per Bus)
                case(2):
                    clear()
                    print("You selected 'Bivariate (single-line chart e.g.: Bus passengers per Bus)'\n")
                    print("_____ per ______\n")
                    first_type_index = inquirer.list_input("Select 1st variable",
                                            choices=[(type, idx) for idx, type in enumerate(types)],
                                            carousel=True)
                    clear()
                    print(f'''You selected 'Bivariate (single-line chart e.g.: Bus passengers per Bus)
                          
{types[first_type_index]} per ______
                          ''')
                          
                    second_type_index = inquirer.list_input("Select 2nd variable",
                                            choices=[(type, idx) for idx, type in enumerate(types) if idx != first_type_index],
                                            carousel=True)
                    clear()
                    print(f"You have selected:\n\n{types[first_type_index]} per {types[second_type_index]}.\n")
                    ypoints =array[:,first_type_index+1]/array[:,second_type_index+1]
                    plt.plot(xpoints, ypoints,
                            color=color, 
                            alpha=opacity, 
                            marker=marker, 
                            linestyle=linestyle, 
                            linewidth=linewidth,
                            )
                    plt.ylabel(f"{types[first_type_index]} per {types[second_type_index]}")
                    plt.xlabel('Year')
                    plt.title(f"No. of {types[first_type_index]} per {types[second_type_index]} crossing over the years", fontdict = heading_font)
                    plt.show()
                # Chosen: Multivariate (multi-line chart, multiple types)
                case(3):
                    clear()
                    print("You selected 'Multivariate (multi-line chart for multiple datatypes)'\n")
                    multivariate_types = inquirer.checkbox("Select variables",
                                            choices=[(type, idx) for idx, type in enumerate(types)],
                                            carousel=True,
                                            validate=validation_function)
                    for i in multivariate_types:
                        plt.plot(array[:,i+1],
                            alpha=opacity, 
                            marker=marker, 
                            linestyle='solid', 
                            linewidth=linewidth,
                            label=types[i]
                            )
                    plt.plot(xpoints=xpoints)
                    plt.ylabel(list_items([types[i] for i in multivariate_types]))
                    plt.xlabel('Year')
                    plt.title("Vehicle crossings over the years", fontdict = heading_font)
                    plt.legend()
                    plt.show()
                # Chosen: return to view charts menu
                case(4):
                    return
        # Chosen: data for a given year
        case(2):
            clear()
            print("You selected 'Data for a given year'.\n")
            print(f"Available years: {array[0,0]} - {array[-1,0]}.\n")
            year_input = inquirer.list_input("What year would you like to view?",
                            choices=[i for i in range(array[0,0], array[-1,0]+1)],
                            carousel=True)
            chart_input = inquirer.list_input("What kind of chart do you want to see?",
                                choices=[("Bar chart (comparison)",1),("Pie chart (composition)",2),(return_message,3)],
                                carousel=True)
            match(chart_input):
                # Chosen: Bar chart (comparison)
                case(1):
                    clear()
                    print("You selected 'Bar chart (comparison)'")
                    plt.bar(types, 
                            height=array[year_input%100,1:],
                            color = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
                            )
                    plt.title(f"Crossing data in {year_input}", fontdict = heading_font)
                    plt.show()
                # Chosen: Pie chart (composition)
                case(2):
                    clear()
                    print("You selected 'Pie chart (composition)'")
                    wedgeprops = {"linewidth": 1, 'width':1, "edgecolor":"k"}
                    plt.pie(array[year_input%100,1:], 
                            labels=types,autopct="%0.2f%%", 
                            explode=[0.1] * len(array[year_input%100,1:]),
                            shadow=True,
                            wedgeprops=wedgeprops,
                            radius = 1.1,
                            )
                    plt.title(f"Crossings data in {year_input}", fontdict = heading_font)
                    plt.legend()
                    plt.show()
                # Chosen: return to view charts menu
                case(3):
                    return

        # Chosen: return to view charts menu
        case(3):
            return
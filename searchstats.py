import numpy as np
import csv
import sys
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self, type_array):
        super().__init__()

        self.setWindowTitle("Search Statistics")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        type_group = QVBoxLayout()
        self.label = QLabel("Select a type from the table:")
        type_group.addWidget(self.label, alignment=Qt.AlignCenter)
        self.type_combo_box = QComboBox(self)
        for ele in type_array:
            self.type_combo_box.addItem(ele)
        self.type_combo_box.currentIndexChanged.connect(self.type_selected)
        self.type_combo_box.setFixedWidth(200)
        type_group.addWidget(self.type_combo_box, alignment=Qt.AlignCenter)
        self.layout.addLayout(type_group)

        self.labels_layout = QVBoxLayout()
        selected_type_all_years = b[:, 1]  # Get the column for the selected vehicle type. e.g.: [4059, 3928, 45986]
        selected_average = np.mean(selected_type_all_years)  # Calculate the average of the selected vehicle type. 
        self.mean_label = QLabel("Mean number of {types} from {start_year} to {end_year} is {mean}".format(types=type_array[0].lower(), start_year = b[0,0], end_year = b[-1,0], mean=int(selected_average)))
        self.labels_layout.addWidget(self.mean_label, alignment=Qt.AlignCenter)
        x = np.where(selected_type_all_years > selected_average)
        years = list_items(b[x, 0][0])
        # self.higher_label = QLabel("The number of {types} were higher than average in these years: {years}".format(types=type_array[0].lower(), years=years))
        # self.labels_layout.addWidget(self.higher_label, alignment=Qt.AlignCenter)
        maximum = selected_type_all_years.max()
        most_year = b[np.where(b == maximum)[0], 0][0]
        self.highest_label = QLabel("The highest was {maximum} in {most_year}.".format(maximum=maximum, most_year=most_year))
        self.labels_layout.addWidget(self.highest_label, alignment=Qt.AlignCenter)
        self.layout.addLayout(self.labels_layout)

        year_group = QVBoxLayout()
        self.label = QLabel("Select the year you would like:")
        year_group.addWidget(self.label, alignment=Qt.AlignCenter)
        self.year_combo_box = QComboBox(self)
        year_array = np.array(b[:,0])
        year_list = year_array.tolist()
        years = ' '.join(map(str, year_list))
        years_array = years.split()
        for ele in years_array:
            self.year_combo_box.addItem(ele)
        self.year_combo_box.setFixedWidth(200)
        year_group.addWidget(self.year_combo_box, alignment=Qt.AlignCenter)
        self.layout.addLayout(year_group)

        self.display_label = QLabel("Display Area")
        self.layout.addWidget(self.display_label, alignment=Qt.AlignCenter)

        self.menu_button = QPushButton("Main Menu", self)
        self.menu_button.setFixedWidth(200)
        self.menu_button.clicked.connect(self.mainMenu)
        self.layout.addWidget(self.menu_button)

    def mainMenu(self):
        self.close()
        return
    
    def type_selected(self, index):
        selected_option = self.sender().currentText()
        selected_column = type_array.index(selected_option)
        selected_type_all_years = b[:, int(selected_column)]  # Get the column for the selected vehicle type. e.g.: [4059, 3928, 45986]
        selected_average = np.mean(selected_type_all_years)  # Calculate the average of the selected vehicle type. 
        self.mean_label.setText("Mean number of {types} from {start_year} to {end_year} is {mean}".format(types=selected_option.lower(), start_year = b[0,0], end_year = b[-1,0], mean=int(selected_average)))
        x = np.where(selected_type_all_years > selected_average)
        self.higher_label.setText("The number of {types} were higher than average in these years: ".format(types=selected_option.lower()) + list_items(b[x, 0][0]))
        maximum = selected_type_all_years.max()
        most_year = b[np.where(b == maximum)[0], 0][0]
        self.highest_label.setText("The highest was {maximum} in {most_year}.".format(maximum=maximum, most_year=most_year))

def list_items(items):
    result = ', '.join(str(item) for item in items[:-1])
    return result + ', and ' + str(items[-1])

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

def searchStats():
    global type_array
    type_array = []
    for ele in types:
        type_array.append(ele)
    print(type_array)
    app = QApplication([])
    window = MyWindow(type_array)
    window.resize(500,200)
    window.move(700, 250)
    window.show()
    app.exec_()
    print(b[:,0])
    return
    selected_option = input("\nGive your selection here: ")  # Take user input for the type selection.
    selected_type = types[int(selected_option)-1]  # Get the selected vehicle type based on user input. e.g.: 'buses', 'loaded trucks'
    selected_type_all_years = b[:, int(selected_option)]  # Get the column for the selected vehicle type. e.g.: [4059, 3928, 45986]
    selected_average = np.mean(selected_type_all_years)  # Calculate the average of the selected vehicle type. 
    # clear()
    print("You selected '{}'\n".format(selected_type))
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
    custom_range_avg(int(selected_option))  # Call the function to calculate the average for a custom range of years.

def custom_range_avg(selected_type):
    # Function to calculate the average of a custom range of years for a specific vehicle type.
    print("\nWhat do you want to do? \n1. Find the average of {} in custom range of years\n2. See the number of {} in a specific year\n3. Back to the main menu\n4. Quit the program\n".format(types[selected_type-1].lower(),types[selected_type-1].lower()))
    custom_range_input = int(input("Give your selection here: "))  # Take user input for the custom range choice.
    if custom_range_input == 1:
        # clear()
        print("You selected 'Find the average of {} in custom range of years'.\n".format(types[selected_type-1].lower()))
        start = int(input("Please give the start year (between {} to {}): ".format(b[0,0], b[-1,0])))  # Take user input for the start year.
        end = int(input("Please give the end year (between {start} to {end_year}, end year will not be included in the average): ".format(start=start, end_year=b[-1,0])))  # Take user input for the end year.
        # Calculate the average number of vehicles for the custom range of years.
        custom_filter = np.mean(b[abs(start) % 100:abs(end) % 100, selected_type])
        print("The average number of {} from {} to {} is {:d}".format(types[selected_type-1].lower(), start, end, int(custom_filter)))
        custom_range_avg(selected_type)  # Call the function again to continue or choose another option.
    elif custom_range_input == 2:
        # clear()
        print("You selected: 'See the number of {} in a specific year'.\n".format(types[selected_type-1].lower()))
        chosen_year = input("Give the year you want to view, from {} to {}: ".format(b[0,0], b[-1,0]))
        chosen_index = int(chosen_year)%100
        print("There was {} {} in {}.".format(b[chosen_index,selected_type], types[selected_type-1].lower(), chosen_year))
        custom_range_avg(selected_type)
    elif custom_range_input == 3:
        # clear()
        return "Main Menu"  # Go back to the main menu.
    elif custom_range_input == 4:
        sys.exit()  # Quit the program.
    else:
        print(invalid_input)  # If the input is not valid, show an error message.
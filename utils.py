from os import system, name
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
import csv
import numpy as np
datasheares_icon = "assets/appicon.png"

"""
this function takes in a file name and returns a datalist containing the file contents

:param file_name:   name of the file
:return:            list of rows, each row is a list
"""

def get_data():
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
        return get_data()
    return types, array_clean

def load_csv_data(file_name:str) -> list:
    # Function to load CSV data from the given file name and return it as a li5st of lists.
    openfile = open(file_name)  # Open the file with the given file name.
    csvreader = csv.reader(openfile)  # Create a CSV reader object to read the file.
    datalist = [row for row in csvreader]  # Initialize an empty list to store the data.
    return datalist  # Return the final list of lists containing the CSV data.

# clear() clears the terminal/output
def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 

    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def get_csv_file(window_title):
    app = QApplication([])
    file_dialog = QFileDialog()
    file_dialog.setWindowTitle(window_title)
    file_dialog.setNameFilter("CSV Files (*.csv)")
    file_dialog.setWindowFlags(file_dialog.windowFlags() | Qt.WindowStaysOnTopHint)
    file_dialog.exec_()
    file_path = file_dialog.selectedFiles()[0] if file_dialog.result() else None
    return file_path

def show_message(type, title, message):
    app = QApplication([])
    msg_box = QMessageBox()
    match(type):
        case(1):
            msg_box.setIcon(QIcon(datasheares_icon))
        case(2):
            msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()

def confirm_exit():
    app = QApplication(sys.argv)
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(datasheares_icon))
    msg_box.setWindowTitle("Confirm")
    msg_box.setText("Are you sure you want to close DataSheares? :((((")
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    choice = msg_box.exec_()
    if choice == QMessageBox.Yes:
        sys.exit()  # Exit the application
    else:
        app.quit()  # Close the message box and continue the application

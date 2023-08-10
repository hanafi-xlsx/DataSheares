from os import system, name
from tkinter import filedialog, messagebox
import csv
import sys
import numpy as np
"""
this function takes in a file name and returns a datalist containing the file contents

:param file_name:   name of the file
:return:            list of rows, each row is a list
"""

def get_csv_file():
    file_path, types, array_clean = None, None, None
    messagebox.showinfo("DataSheares", "Please select your .csv file.")
    while not file_path:
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            result = messagebox.askquestion("DataSheares", "Nigger what the fuck is wrong wit you? \nChoose your .csv file man wtf.")
            if not result == messagebox.YES:
                messagebox.showinfo("DataSheares", "I guess nigga aint cool enough to choose his .csv file.")
                sys.exit()
    try:
        array_raw = np.array(load_csv_data(file_path)) # Load the CSV file into a NumPy array called 'array_raw'.
        types = array_raw[1:,0]  # Define a list of vehicle types.
        array_clean = np.array(array_raw.T[1:,], dtype=np.int32) # Remove 'types' column and transposes the array   
    except:
        messagebox.showerror("DataSheares", "Sheares my nigger in christ, are you fucken with me? \nChoose a valid .csv file.")
        get_csv_file()
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

        
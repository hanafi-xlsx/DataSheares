from typing import List
from os import system, name
import csv

"""
this function takes in a file name and returns a datalist containing the file contents

:param file_name:   name of the file
:return:            list of rows, each row is a list
"""
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

"""
input_validation() handles input validation for all inputs in this program

:param message: string for input message
:param stop:    last int allowed
:param start:   start int allowed (optional, default value is 1)
"""
def input_validation(stop:int, start:int = 1, message:str = "Give your selection here: ",  invalids:List[int] = []) -> int:
    num = 0
    while True:
        try:
            num = int(input(message))
        except ValueError:
            print(f"Please enter a valid integer from {start} to {stop}")
            continue
        if num in invalids:
            print(f"'{num}' is an invalid input, please try something else")
        elif num >= start and num <= stop:
            print(f'You entered: {num}')
            return num
        else:
            print(f'The integer must be in the range {start}-{stop}')
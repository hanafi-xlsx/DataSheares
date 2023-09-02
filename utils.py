from os import system, name
from inquirer import errors
import csv

"""
this function takes in a file name and returns a datalist containing the file contents

:param file_name:   name of the file
:return:            list of rows, each row is a list
"""


def load_csv_data(file_name: str) -> list:
    # Function to load CSV data from the given file name and return it as a li5st of lists.
    openfile = open(file_name)  # Open the file with the given file name.
    # Create a CSV reader object to read the file.
    csvreader = csv.reader(openfile)
    # Initialize an empty list to store the data.
    datalist = [row for row in csvreader]
    return datalist  # Return the final list of lists containing the CSV data.

# clear() clears the terminal/output


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def validation_function(answers, current):
    if current == []:
        raise errors.ValidationError(
            '', reason='You need to select at least one option.')
    return True

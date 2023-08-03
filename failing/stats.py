from utils import list_items
import numpy as np
"""
get_stats() provides statistics for a given array

the array needs to have years in the first column and the type in the second column
"""
def get_stats(array:np.ndarray, type:str):
    mean, max_value = array[:,1].mean(), array.max()
    max_year  = array[np.where(array == max_value)[0], 0][0]
    values_above_avg = list_items(array[np.where(array[:,1] > mean), 0][0])
    print(f'''
The average number of {type.lower()} from {array[0,0]} to {array[-1,0]} is {round(mean):d}
The number of {type.lower()} were higher than average in these years: {values_above_avg}
The highest was {max_value} in {max_year}.
    ''')



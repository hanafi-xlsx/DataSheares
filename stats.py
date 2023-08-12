import numpy as np
from tabulate import tabulate

"""
this function creates a list in proper English when given a list of items

:param items:   a list of items e.g.: [2001, 2002, 2004]
:return:        the given list in proper English e.g.: '2001, 2002 and 2004'
"""
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

"""
get_stats() provides statistics for a given array

the array needs to have years in the first column and the type in the second column
"""
def get_stats(array:np.ndarray, types:list):
    tablefmt='rounded_grid'
    headers=['Average', 'Years above average', 'Highest (years)', 'Highest (value)']
    mean_list = [round(i.mean()) for i in array.T[1:]]
    max_value_list = [round(i.max()) for i in array.T[1:]]
    max_year_list = [array[np.where(array == max_value)[0], 0][0] for max_value in max_value_list]
    above_avg_list = [list_items(array[np.where(array[:,idx+1] > mean), 0][0]) for idx, mean in enumerate(mean_list)]
    display = zip(types, mean_list, above_avg_list, max_year_list, max_value_list)
    print(tabulate(display, tablefmt=tablefmt, headers=headers))

from time import sleep
from movingimages import data_shearing
import sys
def quit_program():
    print("Quitting program...")
    sleep(1)
    print("Thanks for using DataSheares!")
    data_shearing()
    sys.exit()

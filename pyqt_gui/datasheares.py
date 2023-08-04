import sys
import qdarktheme
from PyQt5.QtWidgets import QApplication
import mainmenu as mainmenu
import searchstats as searchstats

def dataSheares():
    menu = ["Display Table", "View Charts", "Search Statistics"]
    closeprogram = "Close DataSheares"
    selected_option = mainmenu.mainMenu()
    if selected_option == menu[0]:
        print("Running display table")
    elif selected_option == menu[1]:
        print("View Charts")
    elif selected_option == menu[2]:
        print("Search Statistics")
        searchstats.searchStats()
    elif selected_option == closeprogram:
        print("Closing DataSheares")
        sys.exit()
    print("Main Menu")
    dataSheares()

app = QApplication([])
qdarktheme.setup_theme("auto")
dataSheares()

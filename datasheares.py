import sys
import mainmenu
import searchstats

def dataSheares():
    menu = ["Display Table", "View Charts", "Search Statistics"]
    closeprogram = "Close DataSheares"
    selected_option = mainmenu.startApp()
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
    dataSheares()

dataSheares()
import sys
import mainmenu
import searchstats

menu = ["Display Table", "View Charts", "Search Statistics", "Close DataSheares"]

def startApp():
    selected_option = mainmenu.mainMenu(menu)
    if selected_option == menu[0]:
        print("Running display table")
    elif selected_option == menu[1]:
        print("View Charts")
    elif selected_option == menu[2]:
        print("Search Statistics")
        searchstats.searchStats()
    elif selected_option == menu[3]:
        print("Closing startApp")
        sys.exit()
    print("Main Menu")
    startApp()

startApp()

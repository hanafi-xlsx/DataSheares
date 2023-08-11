from tkinter import messagebox
import tkinter as tk
import subprocess
import sys
import os

def install_pip_libraries():
    modules = ["PyQt5", "numpy", "inquirer", "tabulate", "matplotlib"]
    root = tk.Tk()
    root.withdraw()
    try:
        module_statuses = {module: True if __import__(module) else False for module in modules}
    except:
        answer = messagebox.askquestion("Installation", "Do you want to begin the greatness?")
        match(answer):
            case("yes"):
                modules.append("pyqtdarktheme")
                print("Commencing installation. Please wait.")
                for module in modules:
                    subprocess.run(["pip", "install", module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print(module+" installed.")
                python_executable = sys.executable
                script_path = os.path.abspath(__file__)
                subprocess.run([python_executable, script_path])
                sys.exit()
            case("no"):
                exit()
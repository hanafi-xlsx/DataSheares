import subprocess

modules = ["PyQt5", "pyqtdarktheme", "numpy", "inquirer", "tabulate", "matplotlib"]

for module in modules:
    subprocess.run(["pip", "uninstall", "-y", module])

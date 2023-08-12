import subprocess

modules = ["PyQt5", "numpy", "inquirer", "tabulate", "matplotlib", "pygame", "pyqtdarktheme"]
for module in modules:
    subprocess.run(["pip", "uninstall", "-y", module])
    print(module+" uninstalled.")
            
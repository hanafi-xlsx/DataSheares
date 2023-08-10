import tkinter as tk
from tkinter import messagebox

def ask_resume_or_close():
    result = messagebox.askquestion("Resume or Close", "Do you want to resume or close the program?")
    
    if result == 'yes':
        print("Resuming program...")
    else:
        print("Closing program...")
        root.destroy()

root = tk.Tk()
root.withdraw()  # Hide the main window

ask_resume_or_close()

root.mainloop()

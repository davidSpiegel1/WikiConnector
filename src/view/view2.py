import tkinter as tk
from tkinter import ttk

# Going to 
# Possible new libaries to use:
# PyQT5/PyQT6. 
class view(tk.Tk):
    def __init__(self,kern):
        super().__init__()
        self.kern = kern
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.title("Wiki OS")
        
        self.login_screen()


    def login_screen(self):
        
        l = tk.Label(self,text=self.kern.get_current_user())
        l.pack()

        login = ttk.Combobox(self)

        login.pack(anchor='center')

        



    def run(self):
        self.mainloop()



try:
    import Tkinter as tk
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    from tkinter import ttk
from json import load
class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        
        self.style =  ttk.Style()

        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

        #self.style = ttk.Style()

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None
    
    def changeTheme(self,theme):
        #return self.style
        self.style.theme_use(theme)

    def __initialize_custom_style(self):
        #self.style = ttk.Style()
                
        #style.theme_create("n",parent="clam",settings=load(open("view/assets/nordTheme/nordicNotebook.json")))
        self.style.theme_use("n")

        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        self.style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        self.style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        self.style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])
    """def add_tab(self):
        tab_count = len(notebook.tabs())
        new_frame = ttk.Frame(notebook)
        notebook.add(new_frame, text=f'Tab {tab_count + 1}')
    def getAddFrame(self):
        # Create a frame to hold the add tab button
        add_tab_frame = ttk.Frame(notebook)
        add_tab_frame.pack(fill='both', expand=True)"""
    def add_tab(self,event=None):
        # Get the ID of the currently selected tab
        current_tab = self.select()

        # Check if the current tab is the "+" tab
        if self.tab(current_tab, "text") == "+":
            # Create a new frame for the new tab
            new_frame = ttk.Frame(self)
            tab_count = len(self.tabs()) - 1  # Subtract 1 to ignore the "+" tab
        
            # Insert new tab just before the "+" tab
            self.insert(tab_count, new_frame, text=f"Tab {tab_count + 1}")

            # Select the newly created tab
            self.select(tab_count) 
"""if __name__ == "__main__":
    root = tk.Tk()

    notebook = CustomNotebook(width=200, height=200)
    notebook.pack(side="top", fill="both", expand=True)
    

    for color in ("red", "orange", "green", "blue", "violet"):
        frame = tk.Frame(notebook, background=color)
        notebook.add(frame, text=color)
    
    #add = notebook.getAddFrame()
    #notebook.add(add,text='x')
    add_tab_frame = ttk.Frame(notebook)
    notebook.add(add_tab_frame, text="+")
    # Bind the tab change event
    notebook.bind("<<NotebookTabChanged>>", notebook.add_tab)


    root.mainloop()"""

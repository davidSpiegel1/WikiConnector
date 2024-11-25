import tkinter as tk
from tkinter import ttk

def update_suggestions(event):
    typed_text = combobox.get()
    
    # Filter options based on typed text
    if typed_text == "":
        combobox['values'] = options  # Show all options if no text is entered
    else:
        filtered_options = [option for option in options if typed_text.lower() in option.lower()]
        combobox['values'] = filtered_options if filtered_options else options

    # Open the dropdown to show suggestions
    combobox.event_generate('<Down>')

    # Keep the focus on the combobox so typing can continue
    combobox.icursor(len(typed_text))  # Keep cursor at the end
    combobox.focus_set()  # Ensure focus remains on the combobox for continued typing

# Sample options for the combobox
options = ["apple", "banana", "grape", "orange", "watermelon", "melon", "mango", "cherry", "strawberry"]

root = tk.Tk()

# Create combobox and bind update_suggestions to key release
combobox = ttk.Combobox(root, values=options)
combobox.pack(pady=10, padx=10)
combobox.bind("<KeyRelease>", update_suggestions)  # Update suggestions on each keystroke

root.mainloop()


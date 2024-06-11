# Will be the same program, just done with python because this is easier
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.geometry("200x200")


		# Attempting to make a notebook
		self.nb = ttk.Notebook(self)

		
		self.f1 = ttk.Frame(self.nb)
		self.f2 = ttk.Frame(self.nb)

		
		self.f1.pack(fill=tk.BOTH,expand=True)
		self.f2.pack(fill=tk.BOTH,expand=True)
		self.nb.add(self.f1,text="W1")
		self.nb.add(self.f2,text="W2")

		self.f3 = ttk.Frame(self.nb)
		self.nb.insert("end",self.f3,text="W3")
		B= tk.Button(self,text="Click",command=self.show)
		#this.query = tk.simpledialog.askstring("Input"
		B.place(x=100,y=100)
	def show(self):
		print("Hello")

#top = tkinter.Tk()

app = App()
app.mainloop()

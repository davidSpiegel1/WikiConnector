# Will be the same program, just done with python because this is easier
import tkinter as tk
from tkinter import ttk,font
#from tkinter import *
import os
import subprocess
#import pandas as pd
import csv


from dbEngine import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.geometry("200x200")
        self.title("Video Connector")
        self.center(self)

        # A global font might be useful
        self.font = font.Font(family="Courier",size=20,weight=font.BOLD)
        self.font2 = font.Font(family="Courier",size=15,weight=font.BOLD)

        # Attempting to make a notebook
        self.nb = ttk.Notebook(self)
        
        
        self.videoPane = ttk.Frame(self.nb)
        self.queryPane = ttk.Frame(self.nb)
        
        self.dbEng = dbEngine("HI")
        
        self.videoPane.pack(fill=tk.BOTH,expand=True)
        self.queryPane.pack(fill=tk.BOTH,expand=True)
        self.nb.add(self.videoPane,text="Video")
        self.nb.add(self.queryPane,text="Query")

        self.nb.pack(expand=1,fill="both")
        self.nb.select(1)
        #self.f3 = ttk.Frame(self.nb)
        #self.nb.insert("end",self.f3,text="W3")
        #self.center(self)
        B= tk.Button(self.queryPane,text="GO",command=self.show)

        self.bind('<Return>',lambda e: self.show())



        #this.query = tk.simpledialog.askstring("Input"
        B.pack(side='bottom')

        # Text box for it
        self.queryBox = ttk.Entry(self.queryPane,width=10,font=self.font)

                
        self.queryBox.pack(side='top')

        #self.queryBox.pady(10)
        #myX: int = B.winfo_x()
        #myY: int = B.winfo_y()
        #myX = myX*(0.50)
        #myY = myY*(0.55)
        #B.place(x=myX,y=myY)
        #self.center(B)
    def showSnippet(self,curId):
        print("HI",curId)
        for widget in self.videoPane.winfo_children():
            widget.destroy()

        
    # To help center the window we are using
    def center (self,win):
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width*2, height*2, x, y))
        win.deiconify()

    def show(self):
        #for widget in self.videoPane.winfo_children():
        #   widget.destroy()    
        #Make the scroll bar
        #if self.t is not None:
        #   self.t.delete('title',tk.END)
        #self.t = tk.Text(self.videoPane)
        #self.scrollbar = tk.Scrollbar(self.videoPane,command=self.t.yview)
        #self.scrollbar.pack(side='right',fill='y')
        #self.t.configure(yscrollcommand=self.scrollbar.set)
        #mylist = tk.Listbox(self.videoPane,yscrollcommand=self.scrollbar.set)
        
        

        text = self.queryBox.get()
        #print(":",text)
        #path = os.path.abspath(os.getcwd())+"/pythonVersion"
        os.chdir('../') 
        os.chdir('../')
        path = os.listdir()
        p2 = os.path.abspath(os.getcwd())
        model = p2+"/model"
        view = p2+"/view"
        #p = os.path.abspath(os.getcwd())+"/view"
        os.chdir(model)
        path2 = os.listdir()
        #print("Files: ",path2)
        #print("Path: ",p2)
        #os.system("python3 WikiSource.py Mike")
        #subprocess.call("python3 WikiSource.py Mike")
        os.system("python3 WikiSource.py "+text+"; mv test.csv "+view+"/pythonVersion")
        os.chdir("../")
        os.chdir("view/pythonVersion")
        #print("The dir",os.listdir())
        self.displayCSV()

    def displayViewer(self,info):
        print("Display Viewer!!")
        for widget in self.videoPane.winfo_children():
            widget.destroy()

        backbut = tk.Button(self.videoPane,text="<",command=self.displayCSV)
        backbut.pack(side='top',anchor='nw')
    
        
        #run = tk.Button(self.videoPane,text="run",command=lambda e=qb.get(): self.displayViewer(e))

        qb = ttk.Entry(self.videoPane,width=45,font=self.font2)
        
        qb.delete(0,tk.END)
        if  ':' in info:
            qb.insert(0,'select SNIPPET where PAGEID='+info.split(':')[1])
        else:
            qb.insert(0,info)

        qb.pack(side='top')
        t2 = qb.get()
        run = tk.Button(self.videoPane,text="run",command=lambda e=qb: self.queryEng(e))
        run.pack(side='top',anchor='ne')

        #qb.pack(side='top')
        text = qb.get()
        #print("The text",text)  
        #d = dbEngine("HI")
        self.dbEng.scan(text)
        self.dbEng.parse()
        print("The final amount:",self.dbEng.getFlist())
        fList = self.dbEng.getFlist()

        t = tk.Text(self.videoPane)
        scrollbar = tk.Scrollbar(self.videoPane,command=t.yview)
        scrollbar.pack(side='right',fill='y')
        t.configure(yscrollcommand=scrollbar.set)



        for val in fList:
            if '<span' in val:
                
                r = ''
                f= val.split('<span class="searchmatch">')
                
                for i in f:
                    r+=i
                print("What r is: ",r)
                #r2 = ''
                #f2 = r.split('class="searchmatch"')
                #for i2 in f2:
                #    r2 += i2
                #print("What r2 is: ",r2)
                r3 = ''
                f3 = r.split('</span>')
                for i3 in f3:
                    r3 += i3
                print("What r3 is: ",r3)
                label = tk.Label(t,text=r3,font=self.font2)
                label.pack(side='bottom')
                t.window_create("end",window=label)
                t.insert("end","\n")

            else:
                label = tk.Label(self.videoPane,text=val,font=self.font2)
                label.pack(side='bottom')
                t.window_create("end",window=label)
                t.insert("end","\n")
        t.pack(expand=1,side="left")
        #self.nb.select(0)
        
    def queryEng(self,qb):
        #for widget in self.videoPane.winfo_children():
        #    widget.destroy()
        text = qb.get()
        self.displayViewer(text)


    def displayCSV(self):
        for widget in self.videoPane.winfo_children():
            widget.destroy()    
        #Make the scroll bar
        #if self.t is not None:
        #   self.t.delete('title',tk.END)
        self.t = tk.Text(self.videoPane)
        self.scrollbar = tk.Scrollbar(self.videoPane,command=self.t.yview)
        self.scrollbar.pack(side='right',fill='y')
        self.t.configure(yscrollcommand=self.scrollbar.set)
        #mylist = tk.Listbox(self.videoPane,yscrollcommand=self.scrollbar.set)

        #csvFile = pandas.read_csv('test.csv')
        #print(csvFile)
        count = 0
        with open('test.csv',newline='') as cs:
            s = csv.reader(cs,delimiter=',')
            #if count == 0:
            for title in s:
                #print("The titles: ",title)
                print("The final title: ",title[0])
                

                #print("The other one: ",title[1])
                print("The snippet ",title[2])
                #self.videoPane.tkraise()
                id2 = title[1]
                bn = tk.Button(self.t,text=title[0],command=lambda e=id2: self.displayViewer(e))
                bn.pack()
                self.t.window_create("end",window=bn)
                self.t.insert("end","\n")
                #bn.pack()
                #mylist.insert(tk.END,title[0])
                #self.videoPane.attributes('-topmost', True)
                #self.videoPane.attributes('-topmost', False)
            #else:
            #for val in s:
            #print(val)
            #self.nb.select(0)
            count += 1
        #mylist.pack(side='left',fill='both')
        #self.scrollbar.config(command=mylist.yview)
        #t.configure(state="disabled")
        self.t.pack(expand=1,side="left")
        self.nb.select(0)
        #subprocess.call("ls")
        #subprocess.call("cd model; ls")
        #os.system("mv model/test.csv "+p2+"/pythonVersion")
        # mv test.csv /Users/davidspiegel/git/videoConnector/src/model/pythonVersion
        #os.chdir(path)
        #os.system("python3 main.py")
        #os.system("python3 main.py")
                
        #code = subprocess.call("mv model/test.csv "+view+"/pythonVersion")


#top = tkinter.Tk()

app = App()
app.mainloop()

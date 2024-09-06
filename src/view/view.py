# Will be the same program, just done with python because this is easier
import tkinter as tk
from tkinter import ttk,font
#from tkinter import *
import os
import subprocess
#import pandas as pd
import csv
from PIL import Image,ImageTk

from dbEngine import *
from controller import controller
#from model import AppleMusic,WikiSource,WorldBankSource,Entry

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.geometry("200x200")
        self.title("Video Connector")
        self.center(self)
        
        self.Controller = controller.Controller()

        # An instance variable might be good
        self.font = font.Font(family="Courier",size=20,weight=font.BOLD)
        self.font2 = font.Font(family="Courier",size=15,weight=font.BOLD)

        # The color for the background
        self.themes = {"dark": 
                        {"button": 
                            {"foreground":"white","background":"black"}
                        ,"frame": {"foreground":"white","background":"black"}
                        ,"notebook":{"foreground":"white","background":"grey"}}
                    ,"light": 
                        {"button": 
                            {"foreground":"black","background":"white"}
                        ,"frame":
                            {"foreground":"black","background":"white"}
                        ,"notebook":
                            {"foreground":"black","background":"grey"}}
                        }
        self.buttonStyle = ttk.Style()
        self.buttonStyle.configure("BW.TButton",foreground=self.themes["light"]["button"]["foreground"],background=self.themes["light"]["button"]["background"])

        self.frameStyle = ttk.Style()
        self.frameStyle.configure("BW.TFrame",foreground=self.themes["light"]["frame"]["foreground"],background=self.themes["light"]["frame"]["background"])

        self.notebookStyle = ttk.Style()
        self.notebookStyle.configure("BW.TNotebook",foreground=self.themes["light"]["notebook"]["foreground"],background=self.themes["light"]["notebook"]["background"])
        #self.buttonTheme = self.themes["dark"]["button"]
        #self.frameTheme = self.themes["dark"]["frame"]
        self.config(bg=self.themes["light"]["button"]["background"])
        # Attempting to make a notebook
        self.nb = ttk.Notebook(self)
        self.tempCon = "" 
        self.Connectors = {} # A Dictionary that will hold the name and the kind of connector
        self.possibleConnectors = ["Wiki","WorldBank","AppleMusic"]

        self.videoPane = ttk.Frame(self.nb,style="BW.TFrame")
        self.queryPane = ttk.Frame(self.nb, style="BW.TFrame")
        
        self.dbEng = dbEngine("HI")
        self.showEditor = False
        self.videoPane.pack(fill=tk.BOTH,expand=True)
        self.queryPane.pack(fill=tk.BOTH,expand=True)
        self.nb.add(self.videoPane,text="Video")
        self.nb.add(self.queryPane,text="Query")

        self.nb.pack(expand=1,fill="both")
        self.nb.select(1)
        self.nb.configure(style="BW.TNotebook")
        #self.f3 = ttk.Frame(self.nb)
        #self.nb.insert("end",self.f3,text="W3")
        #self.center(self)
        B= ttk.Button(self.queryPane,text="GO",style="BW.TButton",command=self.show)

        self.bind('<Return>',lambda e: self.show())

        B.pack(side='bottom')
        
        self.curConLabel = tk.Label(self.queryPane,text=self.Controller.getConnector())
        #try:
        # MUST Get icons working!!
        #i = Image.open("icon.png")
        #img = ImageTk.PhotoImage(i)    
        
            
        #except: 
        #    print("HERR")
        #imgLabel = tk.Label(self.queryPane)
        #imgLabel.config(image=img)
        #imgLabel.pack(expand=0,anchor='nw',side='bottom')
        
        self.curConLabel.pack(side='top')
        # Text box for it
        self.queryBox = ttk.Entry(self.queryPane,width=10,font=self.font)


          
        
        self.queryBox.pack(side='top')

        self.constructMenu()



    def constructMenu(self):
        self.menuBar = tk.Menu(self)
        self.connectMenu = tk.Menu(self.menuBar,tearoff=0)
        
        for ids in self.Connectors:
            name = self.Connectors[ids]
            self.connectMenu.add_command(label=name,command=lambda e = ids: self.EnableConnector(e))

        self.connectMenu.add_command(label="Add Connector",command=self.ShowConnectors)
        

        # Making an icon for the pref and quit
        self.connectPref = tk.Menu(self.menuBar,tearoff=0)
        self.connectPref.add_command(label="Dark Mode",command=self.EnableDarkMode)
        self.connectPref.add_command(label="Prefrences",command=self.ShowPrefrences)
        self.connectPref.add_command(label="Exit",command=self.exit)
        self.menuBar.add_cascade(label="VC",menu=self.connectPref)        
        
        self.menuBar.add_cascade(label="Connectors",menu=self.connectMenu)
        
        
        self.config(menu=self.menuBar)
    
    def EnableDarkMode(self):
        print("DARK MODE")
        self.frameStyle.configure("BW.TFrame",foreground=self.themes["dark"]["frame"]["foreground"],background=self.themes["dark"]["frame"]["background"])
        self.buttonStyle.configure("BW.TButton",foreground=self.themes["dark"]["button"]["foreground"],background=self.themes["dark"]["button"]["background"])
        
        self.notebookStyle.configure("BW.TNotebook",foreground=self.themes["dark"]["notebook"]["foreground"],background=self.themes["dark"]["notebook"]["background"])

        self.connectMenu.config(bg="black",fg="white")
        self.connectPref.config(bg="black",fg="white")
    def ShowPrefrences(self):
        root = tk.Tk()
        root.title("Prefrences")
        root.attributes('-alpha',0.5)
        v = tk.DoubleVar()
        scale = tk.Scale(root,variable=v,from_=0,to=10,orient=tk.HORIZONTAL)
        scale.pack(anchor=tk.CENTER) 
        self.center(root)
        root.mainloop()
    def exit(self):
        self.destroy()

    def showSnippet(self,curId):
        for widget in self.videoPane.winfo_children():
            widget.destroy()

    def ShowConnectors(self):
        newWindow = tk.Toplevel(self)
        newWindow.title("Get New Connector")
        self.center(newWindow)
        
        typeClicked = ""
        #var = tk.StringVar()# Variable
        for con in self.possibleConnectors:
            #var = tk.StringVar(con)
            b = tk.Checkbutton(newWindow,text=con,command=lambda e=con: self.setTempCon(e))
            
            b.pack(side='top')
        #print("typeClicked: ",typeClicked)
        
        #entry = tk.Entry(newWindow,width=45,font=self.font)
        #entry.pack(side='bottom')
        #ilb1 = tk.Label(newWindow,text="Name:",font=self.font)
        #lb1.pack(side="left")
        #but = tk.Button(newWindow,text="Add",command=lambda e= self.addConnector)
        #but.pack(side='bottom')
        
        lb1 = tk.Label(newWindow,text="Name:",font=self.font2)
        lb1.pack(side="left")
        entry = tk.Entry(newWindow,width=20,highlightthickness=3,font=self.font2)
        entry.config(highlightbackground = "blue", highlightcolor= "blue")
        entry.pack(side='left')
        
        
        but = tk.Button(newWindow,text="Add",command=lambda e= entry,e2=lb1,e3=newWindow: self.addConnector(e,e2,e3))
        but.pack(side='bottom',anchor='w')


    def addConnector(self,ent,label,root):
        print(self.tempCon)
        name = ent.get()
        if len(name) <= 0:
            label['text']="name required"
            ent.config(highlightbackground = "red", highlightcolor= "red")
        elif len(self.tempCon) <= 0:
            label['text']="connector required"
            #ent.config({"background":"red"})
            ent.config(highlightbackground = "red", highlightcolor= "red")    
        else:
            label['text'] = "Name:"
            #self.tempCon = ''
            ent.config(highlightbackground="blue",highlightcolor="blue")
            self.Connectors[self.tempCon] = name
            self.connectMenu.add_command(label=name,command=lambda e=self.tempCon: self.EnableConnector(e))
            newWin = tk.Toplevel(root)
            self.tempCon=''
            #b1 = tk.Button(newWin,text="OK",command=lambda: root.destroy())
            
            #b1.pack(side='bottom')
            root.destroy()
    
    def setTempCon(self,temp):
        self.tempCon = temp
    

    def EnableConnector(self,con):
        #if self.Controller is not None:
        self.Controller.setConnector(con)
        self.curConLabel.config(text=con)

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

        
        self.Controller.query(text)
        #print(":",text)
        #path = os.path.abspath(os.getcwd())+"/pythonVersion"
        """os.chdir('../') 
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
        #print("The dir",os.listdir())"""

        self.displayCSV()

    def displayViewer(self,info):
        print("Display Viewer!!")
        for widget in self.videoPane.winfo_children():
            widget.destroy()

        
        header = tk.Frame(self.videoPane)
        header.pack(side='top')
        backbut = tk.Button(header,text="<",command=self.displayCSV)
        backbut.pack(side='left',anchor='nw')
        
        
        
        #run = tk.Button(self.videoPane,text="run",command=lambda e=qb.get(): self.displayViewer(e))

        qb = ttk.Entry(header,width=45,font=self.font2)
        
        qb.delete(0,tk.END)
        if  ':' in info:
            print("What info is: ",info.split(':')[1])
            qb.insert(0,'select SNIPPET where PAGEID='+info.split(':')[1])
        elif 'select' in info:
            print("What info is: ",info)
            qb.insert(0,info)
        else:
            qb.insert(0,'select SNIPPET where PAGEID='+info)

        #qb.pack(side='bottom',anchor='e')
        
        

        t2 = qb.get()
        run = tk.Button(header,text="run",command=lambda e=qb: self.queryEng(e))
        #run = tk.Button(self.videoPane,text="run",command=lambda: self.queryEng(qb))   
        #run.pack(side='right',anchor='ne')

        #showEditor = tk.Button(self.videoPane,text="^",command=lambda e=info: self.showButton(e))
        showEditor = tk.Button(header,text="^",command=lambda: self.showButton(qb,run))
        showEditor.pack(side='right',anchor='ne')
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
        scrollbar.pack(side='right',fill='both')
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
                label.pack(side='left',expand=1,fill=tk.BOTH)
                t.window_create("end",window=label)
                t.insert("end","\n")

            else:
                label = tk.Label(self.videoPane,width=len(val),height=len(val),text=val,font=self.font2)
                label.pack(side='left',anchor='nw')
                t.window_create("end",window=label)
                t.insert("end","\n")
        t.pack(expand=1,side="left")
        #self.nb.select(0)
        
    def queryEng(self,qb):
        #for widget in self.videoPane.winfo_children():
        #    widget.destroy()
        text = qb.get()
        self.displayViewer(text)

    def showButton(self,qb,run):
        
        
        if self.showEditor == True:
            qb.pack_forget()
            run.pack_forget()
            self.showEditor = False
        else:
            qb.pack()
            run.pack()
            self.showEditor = True
            
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
        #print(csvFile)
        count = 0
        with open('view/test.csv',newline='') as cs:
            s = csv.reader(cs,delimiter=',')
            #if count == 0:
            for title in s:
                print("The titles: ",title)
                if len(title) >=2:
                    print("The final title: ",title[0])
                

                    #print("The other one: ",title[1])
                    #print("The snippet ",title[2])
                    #self.videoPane.tkraise()
                    id2 = title[1]
                    bn = tk.Button(self.t,text=title[0],command=lambda e=id2: self.displayViewer(e))
                    bn.pack()
                    self.t.window_create("end",window=bn)
                    self.t.insert("end","\n")
            count += 1
        self.t.pack(expand=1,side="left")
        self.nb.select(0)


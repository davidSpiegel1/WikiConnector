# Will be the same program, just done with python because this is easier
import tkinter as tk
from tkinter import ttk,font
#from tkinter import *
import os
import subprocess
import sys
#import pandas as pd
import csv
import traceback
from PIL import Image,ImageTk

from dbEngine import *
from controller import controller
from json import load
from customNotebook import *
#from model import AppleMusic,WikiSource,WorldBankSource,Entry

try:
    from bs4 import BeautifulSoup
except:
    subprocess.check_call([sys.executable,"-m","pip","install","beautifulsoup4"])

try:
    from tkhtmlview import HTMLLabel
except ImportError:
    print("tkhtmlview not found. Using pip to install")
    subprocess.check_add([sys.executable,"-m","pip","install","tkhtmlview"])
    print("tkhtmlview installed successfully!")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.title("Wiki Connector")
        self.center(self)
        
        self.Controller = controller.Controller()

        # An instance variable might be good
        self.font = font.Font(family="Courier",size=20,weight=font.BOLD)
        self.font2 = font.Font(family="Courier",size=15,weight=font.BOLD)
       
        self.themeLabel = "light"
        
        # The color for the background
        self.themes = {"dark": 
                        {"button": 
                            {"foreground":"#81a1c1","background":"#4c566a"}
                        ,"frame": 
                            {"foreground":"#81a1c1","background":"#4c566a"}
                        ,"notebook":{
                            "foreground":"#81a1c1","background":"#4c566a"}}
                    ,"light": 
                        {"button": 
                            {"foreground":"#5e81ac","background":"#81a1c1"}
                        ,"frame":
                            {"foreground":"#88c0d0","background":"#81a1c1"}
                        ,"notebook":
                            {"foreground":"black","background":"#d8dee9"}
                        }}
        self.style = ttk.Style()

        # Going to try to use 'theme_use' for the button style
        #self.buttonStyle.configure("BW.TButton",foreground=self.themes["light"]["button"]["foreground"],background=self.themes["light"]["button"]["background"])
            
        
        #self.notebookStyle = ttk.Style()
        try:
            self.style.theme_create("n",parent="clam",settings=load(open("view/assets/nordTheme/nordicNotebook.json")))
            self.style.theme_create("nd",parent="clam",settings=load(open("view/assets/nordTheme/nordicNotebookDark.json")))
            self.style.theme_use("n")
        #self.notebookStyle.configure("BW.TNotebook",foreground=self.themes["light"]["notebook"]["foreground"],background=self.themes["light"]["notebook"]["background"])
        except Exception as e:
            print("Error. Loading asset notebook theme did not work",e)
            traceback.print_exc()
        #self.buttonTheme = self.themes["dark"]["button"]
        #self.frameTheme = self.themes["dark"]["frame"]
        #self.config(bg=self.themes["light"]["button"]["background"])#,font=self.font)
        # Attempting to make a notebook
        #self.nb = ttk.Notebook(self,style="TNotebook")
        self.nb = CustomNotebook(width=20,height=20)
        # Needed connector information
        self.tempCon = "" 
        self.Connectors = {} # A Dictionary that will hold the name and the kind of connector
        self.possibleConnectors = ["Wiki","WorldBank","AppleMusic","WebViewBrowser","Terminal"]

        self.videoPane = tk.Frame(self.nb,background=self.style.lookup("TNotebook","background"))#,style="TFrame")
        self.queryPane = tk.Frame(self.nb,background=self.style.lookup("TNotebook","background")) #style="TFrame")
        
        self.dbEng = dbEngine("HI")
        self.showEditor = False
        self.videoPane.pack(fill=tk.BOTH,expand=True)
        self.queryPane.pack(fill=tk.BOTH,expand=True)
        #self.videoPane.configure(style="TFrame")
        #self.nb.add(self.videoPane,text="+")
        self.nb.add(self.queryPane,text="Query")
        self.nb.add(self.videoPane,text="+")
        self.nb.pack(expand=1,fill="both")
        #self.nb.select(1)
        self.nb.select(0)
        #self.nb.pack()
        #self.nb.configure(style="TNotebook")
        #self.f3 = ttk.Frame(self.nb)
        #self.nb.insert("end",self.f3,text="W3")
        #self.center(self)
        img2 = None
        try:
            pi2 = Image.open("view/assets/search2.png")
            i2 = pi2.resize((int(screen_width*0.01),int(screen_height*0.01)))
            img2 = ImageTk.PhotoImage(pi2)
        except:
            print("ERROR: NO ASSET go.png")
        #B= ttk.Button(self.queryPane,image=img2,command=self.show,style="C.TButton")

       # Define the button style
        #style.configure('Custom.TButton', background='lightblue', foreground='black', font=('Helvetica', 12))
        #try:
    # Create a ttk.Button with the new style
        B = ttk.Button(self.queryPane,image=img2, style='Custom.TButton',command=self.show)
        #button.pack(padx=10, pady=10)
        #B.configure(style="TButton")
        # ,image=img2
        B.image = img2

        self.bind('<Return>',lambda e: self.show() if self.nb.index(self.nb.select())==0 else print("NOT on tab for enter"))
        #B.bind("<Enter>",lambda e: .config(background="black"))
        B.pack(side='bottom')
        
        self.curConLabel = ttk.Label(self.queryPane,text=self.Controller.getConnector(),style="TLabel")
        #try:
        # MUST Get icons working!!
        try:
            pi = Image.open("view/assets/icon 2.png")
            i = pi.resize((int(self.winfo_height()*0.10),int(self.winfo_height()*0.10)))
            img = ImageTk.PhotoImage(i)
        except:
            print("Error. Could not load asset icon.png")
        #print("What the width is: ",self.winfo_width())
        #img = ImageTk.PhotoImage(i.convert('RGB')) 
        #img = ImageTk.PhotoImage(i)
        l3 = ttk.Label(self.queryPane,image=img,style="TLabel")
        l3.image = img
        l3.pack(anchor='center')   
        self.curConLabel.pack( anchor='center')
        # Text box for it
        #self.queryBox = tk.Entry(self.queryPane,width=10,font=self.font,foreground="#2e3440",background="#81a1c1")

        self.queryBox = ttk.Combobox(self.queryPane,style="TCombobox")
        """close_button = ttk.Button(self.nb, text="x", command=lambda e = self.queryPane: self.remove_tab(e),style='Custom.TButton')
        close_button.pack(side='top', anchor='w', padx=5, pady=50)"""
          
        
        self.queryBox.pack( anchor='center')

        self.queryBox.bind("<KeyRelease>",self.update_suggestions)

        self.constructMenu()

    def remove_tab(self,frame):
        #current_tab = self.nb.select()
        #if current_tab:  # Ensure there's a tab selected
        self.nb.forget(frame)

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




    def update_suggestions(self,event):

        typed_text = self.queryBox.get()
        
        options = []
        
        for connect in self.possibleConnectors:
            options.append("("+typed_text+")->"+connect)

        if typed_text == "":
            self.queryBox['values'] = self.possibleConnectors
        else:
            filtered_options = [con for con in self.possibleConnectors if typed_text.lower() in con.lower()]
            self.queryBox['values'] = filtered_options if filtered_options else options

        self.queryBox.event_generate("<Down>")
        self.queryBox.icursor(len(typed_text))
        self.queryBox.focus_set()

    def EnableDarkMode(self):

        if self.themeLabel == 'light':
            print("Dark mode")
            #self.frameStyle.configure("BW.TFrame",foreground=self.themes["dark"]["frame"]["foreground"],background=self.themes["dark"]["frame"]["background"])
            #self.buttonStyle.theme_use("Adapta")
            #self.buttonStyle.configure("BW.TButton",foreground=self.themes["dark"]["button"]["foreground"],background=self.themes["dark"]["button"]["background"])
            #self.frameStyle.theme_use("f")
            #self.buttonStyle.theme_use("b")
            #self.style.theme_use("n")
            self.nb.changeTheme("n")
            #self.notebookStyle.configure("BW.TNotebook",foreground=self.themes["dark"]["notebook"]["foreground"],background=self.themes["dark"]["notebook"]["background"])
            self.queryBox.config(foreground="#2e3440",background="#81a1c1")
            self.connectMenu.config(bg="black",fg="white")
            self.connectPref.config(bg="black",fg="white")


            self.videoPane.config(background=self.style.lookup("TNotebook","background"))#,style="TFrame")
            self.queryPane.config(background=self.style.lookup("TNotebook","background")) 
            self.themeLabel = 'dark'

        elif self.themeLabel == 'dark':
            print("Light mode")
            #self.buttonStyle.theme_create("e",parent="clam",settings=load(open("view/assets/nordTheme/nordicButtonDark.json")))
            #self.frameStyle.theme_use("fd")
            #self.buttonStyle.theme_use("bd")
            self.style.theme_use("nd")
            #self.nb.changeTheme("nd")
            #i.theme_use("nd")
            #i.configure(i,background="black")
            self.queryBox.config(foreground="#d8dee9",background="#2e3440")
            self.videoPane.config(background=self.style.lookup("TNotebook","background"))#,style="TFrame")
            self.queryPane.config(background=self.style.lookup("TNotebook","background")) 
            self.themeLabel = 'light'
    def ShowPrefrences(self):
        root = tk.Tk()
        root.title("Prefrences")
        
        st = ttk.Style(root)
        try:
            st.theme_create("n",parent="clam",settings=load(open("view/assets/nordTheme/nordicNotebook.json")))
            st.theme_create("nd",parent="clam",settings=load(open("view/assets/nordTheme/nordicNotebookDark.json")))
            st.theme_use("n")
        #f = ttk.Frame(root,style="TFrame")

        #self.notebookStyle.configure("BW.TNotebook",foreground=self.themes["light"]["notebook"]["foreground"],background=self.themes["light"]["notebook"]["background"])
        except Exception as e:
            print("Error. Loading asset notebook theme did not work",e)
            traceback.print_exc()

        f = ttk.Frame(root,style="TFrame")
        f.pack()
        #root.attributes('-alpha',1.0)
        v = tk.IntVar(value=1.0)
        scale = tk.Scale(f,variable=v,from_=0,to=100,orient=tk.HORIZONTAL)
        scale.pack(anchor=tk.CENTER)
        scale.bind("<ButtonRelease-1>",lambda e: root.attributes('-alpha',0.01*(100-scale.get())))
        #scale.bind("<ButtonRelease-2>",lambda e: print("THE BUTTON SCALE: ",0.1*scale.get()))
        
        l = tk.Label(f,textvariable=v)
        l.pack()
        #scale.bind("<ButtonRelease-2>",lambda e: l.config(text=str(100-v.get())))
        #l.pack()

        font = ttk.Label(f,text="Font",style="TLabel")
        font.pack()


        # Possible fonts:
        options = []
        #print("ALL the FONT familes!!",tk.font.families())
        for i in tk.font.families():
            options.append(i)
        clicked = tk.StringVar(f)
        clicked.set(self.font.actual()['family'])

        drop = tk.OptionMenu(f,clicked,*options)
        drop.bind("<ButtonRelease-1>",lambda e: l.config(font=self.font))
        drop.pack()


        
        # Doing the font size
        fontSize = ttk.Label(f,text="Font Size: ",style="TLabel")
        fontSize.pack()
        fsize = [15,20,25,30]
        hit = tk.IntVar(f)
        hit.set(15)

        fs = tk.OptionMenu(f,hit,*fsize)
        fs.pack()







        #apply = tk.Button(root,text="Apply",command=lambda e=scale: self.attributes('-alpha',0.01*(100-e.get())))
        apply = ttk.Button(f,text="Apply",command=lambda e=[scale,clicked,hit]: self.setSettings(e[0],e[1],e[2]),style="Custom.TButton")

        
        apply.pack()
        self.center(root)
        root.mainloop()

    def setSettings(self,scale,clicked,hit):
        self.attributes('-alpha',0.01*(100-scale.get()))
        self.font.configure(family=clicked.get(),size=hit.get()+5)
        self.font2.configure(family=clicked.get(),size=hit.get())
        print("The value inside: ",hit.get())
        
    def exit(self):
        self.destroy()

    def showSnippet(self,curId):
        for widget in self.videoPane.winfo_children():
            widget.destroy()

    def ShowConnectors(self):
        #newWindow = tk.Toplevel(self)
        
        #newWindow.title("Get New Connector")
        tab_cn = len(self.nb.tabs())-1
        self.nb.select(tab_cn)
        #self.center(newWindow)
        for widget in self.videoPane.winfo_children():
            widget.destroy()

        typeClicked = ""
        #var = tk.StringVar()# Variable
        for con in self.possibleConnectors:
            #var = tk.StringVar(con)
            #b = tk.Checkbutton(newWindow,text=con,command=lambda e=con: self.setTempCon(e))
            b = tk.Checkbutton(self.videoPane,text=con,command=lambda e=con: self.setTempCon(e))

            b.pack(side='top')
        #print("typeClicked: ",typeClicked)
        
        #entry = tk.Entry(newWindow,width=45,font=self.font)
        #entry.pack(side='bottom')
        #ilb1 = tk.Label(newWindow,text="Name:",font=self.font)
        #lb1.pack(side="left")
        #but = tk.Button(newWindow,text="Add",command=lambda e= self.addConnector)
        #but.pack(side='bottom')
        
        lb1 = ttk.Label(self.videoPane,text="Name:",font=self.font2,style="TLabel")
        lb1.pack(side="left")
        entry = tk.Entry(self.videoPane,width=20,highlightthickness=3,font=self.font2)
        entry.config(highlightbackground = "blue", highlightcolor= "blue")
        entry.pack(side='left')
        
        
        but = ttk.Button(self.videoPane,text="Add",command=lambda e= entry,e2=lb1,e3=self.videoPane: self.addConnector(e,e2,e3),style="Custom.TButton")
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
            self.ShowConnectors()
    
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
        
        text = self.queryBox.get()
        # Open the combobox dropdown and immediately close it
        self.queryBox.event_generate("<Button-1>")  # Opens the dropdown
        self.after(50, lambda: self.queryBox.event_generate("<Button-1>"))  # Closes it

        # We will add a tab:
        new_frame = ttk.Frame(self.nb)
        tab_cn = len(self.nb.tabs())-1
        curCon = self.Controller.getConnector()
        if tab_cn > 1:
            self.nb.insert(tab_cn,new_frame,text=f"{curCon} ({tab_cn})")
        else:
            self.nb.insert(tab_cn,new_frame,text=f"{curCon}")
        self.nb.select(tab_cn)

        if curCon != "WebViewBrowser" and curCon != "Terminal":
            self.Controller.query(text)
            self.displayCSV(new_frame)
        elif curCon == "WebViewBrowser":
            self.Controller.queryBrowser(text,new_frame)
            #iself.displayCSV(new_frame)
        else:
            #print("NOTHING FOR NOW")

            self.Controller.queryApp(text,new_frame,self.dbEng)

    def displayViewer(self,tuples):
        print("Display Viewer!!")
        soup = None
        with open("view/assets/htmlPages/textViewers.html","r",encoding="utf-8") as file:
            soup = BeautifulSoup(file,"html.parser")



        info = tuples[0]
        curFrame = tuples[1]
        #if not isinstance(curFrame,str):
        for widget in curFrame.winfo_children():
            widget.destroy()
        #else:
        #    return

        
        header = ttk.Frame(curFrame,style="TFrame")
        header.pack(side='top',expand=True,fill='x')
        backbut = ttk.Button(header,text="<",command=lambda e=curFrame: self.displayCSV(e),style="Custom.TButton")

        backbut.pack(side='left',padx=10)#,anchor='nw',fill='x',expand=True)
        
        
        
        #run = tk.Button(self.videoPane,text="run",command=lambda e=qb.get(): self.displayViewer(e))

        qb = ttk.Entry(header,width=45,font=self.font2,foreground="black")
        
        qb.delete(0,tk.END)
        if  ':' in info:
            print("What info is: ",info.split(':')[1])
            qb.insert(0,'select SNIPPET,TITLE where PAGEID='+info.split(':')[1])
        elif 'select' in info:
            print("What info is: ",info)
            qb.insert(0,info)
        else:
            #qb.insert(0,'select SNIPPET,TITLE where PAGEID='+info)
            # Change: Going to make just info for now
            qb.insert(0,info)

        #qb.pack(side='bottom',anchor='e')
        
        

        #t2 = qb.get()
        run = ttk.Button(header,text="run",command=lambda e=(qb,curFrame): self.queryEng(e),style="Custom.TButton")
        #run = tk.Button(self.videoPane,text="run",command=lambda: self.queryEng(qb))   
        #run.pack(side='right',anchor='ne')

        #showEditor = tk.Button(self.videoPane,text="^",command=lambda e=info: self.showButton(e))
        showEditor = ttk.Button(header,text="^",command=lambda: self.showButton(qb,run),style="Custom.TButton")
        showEditor.pack(side='right',padx=10)#,anchor='ne',fill='x',expand=True)
        #qb.pack(side='top')
        text = qb.get()
        #print("The text",text)  
        #d = dbEngine("HI")
        self.dbEng.scan(text)
        self.dbEng.parse()
        print("The final amount:",self.dbEng.getFlist())
        fList = self.dbEng.getFlist()

       # Apply a general style to body directly if needed
        if soup.body:
            body_style = "background-color: blue; text-align:center"
            soup.body['style'] = body_style 

        for val in fList:
            if soup is not None:
                #for body in soup.find_all('body'):
                #    body['style'] = "background-color: #ffeb3b; color: black; padding: 10px; text-align: center;"
                new_div = soup.new_tag("div")
                new_div.string = f'val: {val}'
                if 'SNIPPET:' in val:

                    new_div['style'] = "background-color: #4c566a; padding: 10px; color: #81a1c1; text-align: center; font-size: 20px;"
                else:
                    new_div['style'] = "background-color: #4c566a; padding: 20px; color: #b48ead; text-align: center; font-size: 50px;"
                if soup.body:
                    soup.body.append(new_div)
                else:
                    print("No <body> found!")

        print("The soup: ",str(soup))
        html_label = HTMLLabel(curFrame,html=str(soup),background="#4c566a")
        html_label.pack(fill='both',expand=True)
        #html_label.set_html(str(soup))


        """t = tk.Text(curFrame)
        scrollbar = tk.Scrollbar(curFrame,command=t.yview)
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
                label = tk.Label(curFrame,width=len(val),height=len(val),text=val,font=self.font2)
                label.pack(side='left',anchor='nw')
                t.window_create("end",window=label)
                t.insert("end","\n")
        t.pack(expand=1,side="left")
        #self.nb.select(0)"""
        
    def queryEng(self,touple):
        #for widget in self.videoPane.winfo_children():
        #    widget.destroy()
        qb = touple[0]
        curFrame = touple[1]
        text = qb.get()
        if text is not None:
            self.displayViewer((text,curFrame))

    def showButton(self,qb,run):
        
        
        if self.showEditor == True:
            qb.pack_forget()
            run.pack_forget()
            self.showEditor = False
        else:
            qb.pack()
            run.pack()
            self.showEditor = True
            
    def displayCSV(self,curPane):
        for widget in curPane.winfo_children():
            widget.destroy()    
        #Make the scroll bar
        #if self.t is not None:
        #   self.t.delete('title',tk.END)
        self.t = tk.Text(curPane)
        self.scrollbar = tk.Scrollbar(curPane,command=self.t.yview)
        self.scrollbar.pack(side='right',fill='y')
        self.t.configure(yscrollcommand=self.scrollbar.set)
        if self.themeLabel == 'dark':
            self.t.configure(backgound="#4c566a")
        else:
            self.t.configure(background="#5e81ac")
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
                    bn = ttk.Button(self.t,text=title[0],style="Custom.TButton",command=lambda e=(id2,curPane): self.displayViewer(e))
                    bn.pack(anchor='center')
                    self.t.window_create("end",window=bn)
                    self.t.insert("end","\n")
            count += 1
        self.t.pack(expand=True,fill=tk.BOTH,anchor='center')
        self.nb.select(len(self.nb.tabs())-2)


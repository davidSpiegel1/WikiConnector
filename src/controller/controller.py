# Will hopefully be the interface between the model and the python
import os
import subprocess
#import pandas as pd
import csv
from model import webViewBrowser
#from model import GoogleSource
from model import Terminal
import tkinter as tk
import threading


class Controller:
    def __init__(self):
        
        self.currentConnect = 'Wiki'
        self.possibleConnectors = {'Wiki','WorldBank','AppleMusic','WebViewBrowser'}
        self.google = None
        self.terminal = None

    def setConnector(self,connector):
        self.currentConnect = connector
        if self.currentConnect == "WebViewBrowser" and self.google is None:
            #self.google = GoogleSource.GoogleSource()
            print("Would be google")
    def getConnector(self):
        return self.currentConnect

    def query(self,query):
        text = query
        #test.csv#print(":",text)
        #path = os.path.abspath(os.getcwd())+"/pythonVersion"
        #os.chdir('./') 
        #os.chdir('/')
        #os.chdir('../')
        path = os.listdir()
        print("The path",path)
        p2 = os.path.abspath(os.getcwd())
        model = p2+"/model"
        view = p2+"/view"
        #p = os.path.abspath(os.getcwd())+"/view"
        #os.chdir(model)
        #path2 = os.listdir()
        #print("Files: ",path2)
        #print("Path: ",p2)
        #os.system("python3 WikiSource.py Mike")
        #subprocess.call("python3 WikiSource.py Mike")
        if self.currentConnect == 'Wiki':
            os.system("python3 model/WikiSource.py "+text+"; mv test.csv "+view)
        elif self.currentConnect == 'WorldBank':
            os.system("python3 model/WorldBankSource.py "+text+"; mv test.csv "+view)
        elif self.currentConnect == 'AppleMusic':
            os.system("python3 model/AppleMusic.py "+text+"; mv test.csv "+view)
        #os.chdir("../")
        #os.chdir('../')
        #os.chdir("view")
        #print("The dir",os.listdir())
    """def queryBrowser(self,query,parent_frame):
        #wb = webViewBrowser.WebViewBrowser("google.com")
        
        try:
            #parent_frame.update_idletasks()
            #threading.Thread(target=wb.load_url,args=(query,parent_frame,), daemon=True).start()
            #wb.load_url(query,parent_frame)
            url = self.google.search_google(query)
            self.google.load_url(url,parent_frame)
        except Exception as e:
            print("ERROR: Trouble opening thread for webview",e)"""


    def queryApp(self,appName,parent_frame,dbEngine):
        #button = tk.Button(parent_frame,text="HI")
        #button.pack()
        #print("HERE")
        self.terminal = Terminal.Terminal(appName,parent_frame,dbEngine)
        self.terminal.buildApp()

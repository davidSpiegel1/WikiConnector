# Will hopefully be the interface between the model and the python
import os
import subprocess
#import pandas as pd
import csv
#from model import webViewBrowser
#from model import GoogleSource
#from model import terminal
from model.terminal import *
from model import settings
from model.wiki import *
#import tkinter as tk
import threading


class Controller:
    def __init__(self,kern):
        self.kern = kern
        self.currentConnect = 'Wiki'
        self.possibleConnectors = {'Wiki','WorldBank','AppleMusic','WebViewBrowser'}
        self.google = None
        self.terminal = None

    def getCurApps(self):
        return self.kern.get_apps_name()

    def runApp(self,appName):
        print("Running: ",appName)
        if appName=="programTest":
            return self.kern.run_application(appName)
        elif appName=="terminal":
            try:
                return self.kern.run_application(appName,appName,self.kern)
            except CustomError as e:
                print("ERROR:",e)
        elif appName in self.kern.get_apps_name():#("settings","fileManager","wiki"):
            return self.kern.run_application(appName,appName,self.kern)
        elif "Q:(" in appName:
            print("CONNECTOR: ",appName)
            queryValidate = appName.split("Q:(")
            if len(queryValidate) <= 2:
                print("Right!",queryValidate)
                conValidate = queryValidate[1].split(")->")
                if len(conValidate) <= 2:
                    print("Right again!",conValidate)
                    curQuery = conValidate[0].strip()
                    curCon = conValidate[1].strip()
                    #return self.kern.run_query(curCon,curQuery)
                    return self.build_connector(curCon,curQuery)
                    print("Current query: ",curQuery)
                    print("Current connection: ",curCon)

                else:
                    print("Error. Too many )->",conValidate)
            else:
                print("Error. Too many Q:(s",queryValidate,len(queryValidate))
            #conName = appName.split("->")[1].strip()
            #q1 = appName.split("Q:(")[1].split(")->")[0].strip()
            #[1].split(")")
            #print("THE q1: ",q1)
            #if len(q1)<2:
            #fq = q1[0]
            #print("Final Query: ",fq)
            #if len(q1) >0:
            #    return self.kern.run_query(conName,q1)
    def build_connector(self,connector,query):
        connector = connector.strip()
        if connector in self.kern.get_apps():
            print("THE CONNECTOR: ",connector)
            
            q = self.kern.run_application(connector,connector,self.kern)
            q.setQuery(query)
            q.runQuery()
            return q
        else:
            self.register_connector(connector)
            q = self.kern.run_application(connector,connector,self.kern)
            q.setQuery(query)
            q.runQuery()
            return q

    def register_connector(self,connector):
        t = self.getType(connector)
        if t == 'wiki':
            #lib = {connector:wiki}
            self.kern.register_application(connector,wiki)
        else:
            print("Register did not work",t)


    def getType(self,connector):
        return self.getConnectorData(connector).split(";")[1].split(":")[1].strip()

    def getConnectorData(self,connector):
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        self.kern.get_file_system().change_directory("Modules")
        self.kern.get_file_system().change_directory("Connectors")
        return self.kern.get_file_system().open_file(connector)


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
        print("HERE")
        #self.terminal = Terminal.Terminal(appName,parent_frame,dbEngine)
        #self.terminal.buildApp()

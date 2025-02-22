import os
import io
import subprocess
import sys
import traceback
from model.OS.dbEngine import *
from model.Module import *
import requests
import json
try:
    import PyQt5.QtWidgets as qt
    import PyQt5.QtCore as qCore
    import PyQt5.QtGui as qGui
except ImportError:
    print("PyQt5 not found. Using pip to install")
    subprocess.check_call([sys,executable,"-m","pip","install","PyQt5"])

try:
    from PIL import Image, ImageCms
except ImportError:
    print("PIL not found. Using pip to install")
    subprocess.check_call([sys,executable,"-m","pip","install","PIL"])


class wiki(Connector):
    def __init__(self,name,kern):
        super().__init__(name,kern)
        print("Wiki App")
        self.kern = kern
        self.queryList = []
        #self.layout = qt.QVBoxLayout()
        self.buildMain("https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&formatversion=2&srsearch=")
        #self.pressent()

    def runQuery(self):
        print("Runnin wiki connector")
        if self.query != "":
            self.queryList = self.getWiki()
            #temp = ["1","2","3","4","5"]
            self.getList()
            
    def getList(self):
            #self.clearLayout(self.layout)
        if self.query != "":
            self.getDash()
            self.scroll_area = qt.QScrollArea(self)
            self.scroll_area.setWidgetResizable(True)
            self.layout.addWidget(self.scroll_area)

            b_con = qt.QFrame()
            self.b_lay  = qt.QVBoxLayout(b_con)

            for t in self.queryList:
                b = qt.QPushButton(t)
                b.clicked.connect(lambda checked=False,e=t: self.displayData(e))
                self.b_lay.addWidget(b)
            self.scroll_area.setWidget(b_con)
        else:
            print("Empty Query!")

    def displayData(self, title):
        # Will do sql-based language later...
        data = self.getCSV(self.conName).split(",")
        myStr = ""
        for d in range(len(data)):
            if data[d] == title:
                myStr = data[d]+data[d+1]+data[d+2]
        self.getDash(backList=True)
        b = qt.QLabel(myStr)
        self.layout.addWidget(b)




    def getWiki(self):
        titles = []
        try:
            print("Searching wiki api..")
            self.URL = self.URL+self.query
            response = requests.get(self.URL)
            print("Reponse: ",response)
            j = response.json()
            print("THe json: ",j)
            answers = j["query"]["search"]
            finalLine = "title,pageid,snippet"
            for answer in answers:
                title = str(answer["title"]).replace(",",".")
                titles.append(title)
                pageid = str(answer["pageid"]).replace(",",".")
                snippet = str(answer["snippet"]).replace(",",".")
                finalLine += ","+title+","+pageid+","+snippet
            print("Final line: ",finalLine)
            self.toCSV(self.conName,finalLine)


        except Exception as e:
            print("Error. Wiki did not work.")
        return titles



    def getDash(self,backList=False):
        self.clearLayout(self.layout)
        self.backButton = qt.QPushButton("<")
        if backList == True:
            self.backButton.clicked.connect(self.getList)
        else:
            self.backButton.clicked.connect(lambda checked=False,e=self.URL: self.buildMain(e))
        self.layout.addWidget(self.backButton)


    """def on(self,e):
        if e.text() == 'Off':
            e.setText("On")
            e.setStyleSheet("background-color: #3b4252;")
        else:
            e.setText("Off")
            e.setStyleSheet(self.mainStyle)
        print(self.getConnectorData(self.conName))"""

    #def getUsed(self,

    """def getConnectorData(self,connector):
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        self.kern.get_file_system().change_directory("Modules")
        self.kern.get_file_system().change_directory("Connectors")
        return self.kern.get_file_system().open_file(connector)"""

        
    #home = qt.QWidget()
    #self.show = qt.QLabel("HELLO")

    #self.layout.addWidget(self.show)
    #self.setLayout(self.layout)



        


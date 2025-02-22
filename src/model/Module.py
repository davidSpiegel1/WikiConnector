import os 
import subprocess
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qCore
import PyQt5.QtGui as qGui
from model.OS.Kernel import *
import requests


# The Module class gives an abstract overview of the two major data manipulation and viewing objects
class Module(qt.QWidget):
    def __init__(self,name):
        super().__init__()
        self.name = name
        self.theme = None

    # Must get this done soon. Have ability for mass setting of theme.
    def setTheme(self,theme):
        self.theme = theme

    def getName(self):
        return self.name
    
    # To run the object
    def run(self):
        return 

class App(Module):
    def __init__(self,name,kern):
        super().__init__(name)
        self.kern = kern
        self.background = None
        self.userData = None
    
    def run(self):
        print("Running App...")
        return self


# Connector class: Basically for centralization of data to OS and presenting data
class Connector(Module):
    def __init__(self,name,kern):
        super().__init__(name)
        self.conName = name
        self.URL = None
        self.query = ""
        self.kern = kern
        self.layout = qt.QVBoxLayout()
        self.mainStyle = self.styleSheet()
        
    def buildMain(self,url):
        #if kern not None:
        #    self.setKern(kern)
        self.clearLayout(self.layout)
        self.setURL(url)
        
        # The Connector Name
        nameLabel= qt.QLabel("Name: ")
        self.layout.addWidget(nameLabel)

        nameEdit = qt.QLineEdit(self)
        nameEdit.setText(self.conName)
        self.layout.addWidget(nameEdit)

        typeLabel = qt.QLabel("Type: ")
        self.layout.addWidget(typeLabel)

        typeName = qt.QLabel(" "+self.getType())
        typeName.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(typeName)

        # URL Information
        urlLabel = qt.QLabel("URL: ")
        self.layout.addWidget(urlLabel)

        urlEdit = qt.QLineEdit(self)
        urlEdit.setText(url)
        self.layout.addWidget(urlEdit)

        # On/ Off Toggle

        toggleButton = qt.QPushButton("Off")

        #toggleButton = self.on(toggleButton)#qt.QPushButton("Off")
        if self.getUsed()=='False':
            toggleButton.setText("Off")
            toggleButton.setStyleSheet(self.mainStyle)
        else:
            toggleButton.setText("On")
            toggleButton.setStyleSheet("background-color: #3b4252")

        toggleButton.setFixedSize(50,50)
        toggleButton.clicked.connect(lambda checked=False,e=toggleButton: self.on(e))
        toggleButton.setCheckable(True)
        self.layout.addWidget(toggleButton)


        # The main widget for a connector
        main = qt.QWidget()
        self.setLayout(self.layout)
        self.layout.addWidget(main)

    def on(self,e):
        if self.getUsed() == 'False':
            e.setText("On")
            e.setStyleSheet("background-color: #3b4252")
            self.setUsed('True')
        else:
            e.setText('Off')
            e.setStyleSheet(self.mainStyle)
            self.setUsed('False')

        #print(self.getUsed())
        return e

    def setUsed(self,string):
        self.setConnectorData(self.conName,used=string)

    def getUsed(self):
        return self.getConnectorData(self.conName).split(";")[3].split(":")[1].strip()

    def getType(self):
        return self.getConnectorData(self.conName).split(";")[1].split(":")[1].strip()

    def getConnectorData(self,connector,data=False):
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        self.kern.get_file_system().change_directory("Modules")
        self.kern.get_file_system().change_directory("Connectors")
        if data==True:
            self.kern.get_file_system().change_directory("Data")
        return self.kern.get_file_system().open_file(connector)

    def toCSV(self,connector,data):
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        self.kern.get_file_system().change_directory("Modules")
        self.kern.get_file_system().change_directory("Connectors")
        self.kern.get_file_system().change_directory("Data")
        self.kern.get_file_system().create_file(connector+".csv",data)

    def getCSV(self,connector):
        return self.getConnectorData(connector+".csv",data=True)

    def setConnectorData(self,connectorName,used=None):
        usedOg = self.getUsed()
        name = connectorName
        typeOg = self.getType()
        if used is not None:
            usedOg = used

            finalList = "Name: "+name+"; Type: "+typeOg+"; URL: "+self.URL+"; Used: "+usedOg
            #print("THE FINAL LIST: ",finalList)
            self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
            self.kern.get_file_system().change_directory("Modules")
            self.kern.get_file_system().change_directory("Connectors")
            #self.kern.get_file_system().change_directory("Data")
            self.kern.get_file_system().create_file(connectorName,finalList)




    def getConName(self):
        return self.conName
    def setConName(self,name):
        self.conName = name
    def getURL(self):
        return self.URL
    def setQuery(self,query):
        self.query = query
    def setURL(self,url):
        self.URL=url
    # Do not need this right now
    """def getAPI(self,query):
        print("Preforming get")
        self.query = query
        requests.get(url)
        return r.json()"""
    
    def runQuery(self):
        print("Running Connector...")
        if self.query != "":
            temp = ["A","B","C","D","E","F","G"]
            self.clearLayout(self.layout)
            self.scroll_area = qt.QScrollArea(self)
            self.scroll_area.setWidgetResizable(True)
            self.layout.addWidget(self.scroll_area)

            b_con = qt.QFrame()
            self.b_lay = qt.QVBoxLayout(b_con)
            for t in temp:
                b = qt.QLabel(t)
                self.b_lay.addWidget(b)
            self.scroll_area.setWidget(b_con)
        else:
            print("Empty Query!")

    def run(self):
        return self
    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        #return self





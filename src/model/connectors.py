import os
import io
import subprocess
import sys
import traceback
from model.OS.dbEngine import *
from model.Module import *
from model.wiki import *
try:
    import PyQt5.QtWidgets as qt
    import PyQt5.QtCore as qCore
    import PyQt5.QtGui as qGui
except ImportError:
    print("PyQt5 not found. Using pip to install")
    subprocess.check_call([sys,executable,"-m","pip","install","PyQt5"])


class connectors(App):
    def __init__(self,name,kern):
        super().__init__(name,kern)
        print("Connector Manager App")
        self.kern = kern

        # Needed layouts
        self.grid = qt.QGridLayout()
        self.layout = qt.QVBoxLayout()

        self.curCon = ""
        self.getHome()

    def getHome(self):
        self.getDash()
        
        
        scroll = qt.QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(self.height()//2)
        self.grid.addWidget(scroll,1,1,1,2)

        b_con = qt.QFrame()
        self.b_lay = qt.QVBoxLayout(b_con)
        temp = self.getConnectors()#["Hi","Hey!","M8"]
        for con in temp:
            b = qt.QPushButton(con)
            b.clicked.connect(lambda checked=False,e=con: self.showConnector(e))
            self.b_lay.addWidget(b)
        scroll.setWidget(b_con)

        # Add new connector
        new = qt.QPushButton("+")
        new.clicked.connect(self.addConnector)
        self.grid.addWidget(new,2,1)

        # Edit connectors
        edit = qt.QPushButton("-")
        self.grid.addWidget(edit,2,2)

        # Scroll to see current connectors


        home = qt.QWidget()
        home.setLayout(self.grid)

        

        self.layout.addWidget(home)
        self.setLayout(self.layout)

    def showConnector(self,connector):

        data = ""
        try:
            data = self.getConnectorData(connector)
        except Exception as e:
            print("Error. Cannot find connector type: ",e)
            return

        if data != "":
            self.getDash()

            connector = data.split(";")[1].split(":")[1].strip()
            name = data.split(";")[0].split(":")[1].strip()
            print("The Name: ",name)
            widget = self.kern.run_application(connector,name,self.kern)

            #widget.setLayout(self.grid)
            #self.grid.addWidget(widget,1,1,1,2)
            self.layout.addWidget(widget)
            self.addGrid()
            #self.set



    def getConnectors(self):
        Connectors = []
        #if self.kern.get_current_user()!=self.kern.get_file_system().get_root():
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        self.kern.get_file_system().change_directory("Modules")
        self.kern.get_file_system().change_directory("Connectors")
        files = self.kern.get_file_system().list_contents()["files"]
        for file in files:
            Connectors.append(file)
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        return Connectors

    def getConnectorData(self,connector):
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        self.kern.get_file_system().change_directory("Modules")
        self.kern.get_file_system().change_directory("Connectors")
        return self.kern.get_file_system().open_file(connector)
        

    def setConnector(self,name,conType):
        #if self.kern.get_current_user() != self.kern.get_file_system().get_root():
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        self.kern.get_file_system().change_directory("Modules")
        self.kern.get_file_system().change_directory("Connectors")

        files = self.kern.get_file_system().list_contents()["files"]
        if name not in files:
            data = "Name: "+name+"; Type: "+conType+"; URL: None; Used: False;"
            self.kern.get_file_system().create_file(name,data)
            #if conType == "wiki":
            #self.kern.register_application(name,wiki)
            #print("Figure Out what needs to happen here")



    def addConnector(self):
        print("Adding a connector!")
        
        self.getDash()

        # The Connector Name
        newNameLabel = qt.QLabel("Connector Name: ")
        self.grid.addWidget(newNameLabel,1,1)
        newName = qt.QLineEdit(self)
        newName.setPlaceholderText("Name...")
        self.grid.addWidget(newName,1,2)
        
        #  The List of Connectors
        connectorLabel = qt.QLabel("Connectors: ")
        connectorLabel.setAlignment(qCore.Qt.AlignCenter)
        self.grid.addWidget(connectorLabel,2,1,1,2)
        scroll = qt.QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(self.height()//2)
        self.grid.addWidget(scroll,3,1,1,2)

        b_con = qt.QFrame()
        b_lay = qt.QVBoxLayout(b_con)
        temp = ["wiki","apple","worldBank","youtube"]
        button_group = qt.QButtonGroup(scroll)
        for con in temp:
            b = qt.QCheckBox(con)#qt.QPushButton(con)
            b.stateChanged.connect(self.setCurrentConnector)
            b_lay.addWidget(b)
            button_group.addButton(b)
        scroll.setWidget(b_con)

        # Submit the Connector to add for user
        submit = qt.QPushButton("Submit")
        submit.clicked.connect(lambda checked=False,e=(newName,b_con): self.addConnectorValidate(e))
        self.grid.addWidget(submit,4,1,1,2)
        
        # Have the widget added to the layout
        addPage = qt.QWidget()
        addPage.setLayout(self.grid)
        self.layout.addWidget(addPage)

    def addConnectorValidate(self, widgets):
        name = widgets[0].text()

        if self.curCon != "" and len(name) > 0:
            conType = self.curCon
            self.setConnector(name,conType)
            self.getHome()
        elif self.curCon == "":
            widgets[1].setStyleSheet("border: 2px solid red")
        elif len(name) <= 0:
            widgets[0].setStyleSheet("border: 2px solid red")
        else:
            print("ERROR!!")



    def setCurrentConnector(self, state):
        cur = self.sender()#.text()
        if state == 2:
            self.curCon = cur.text()#,"!!!!")
    
    def addCon(self,widget):
        found = False
        for i in range(self.b_lay.count()):
            if self.b_lay.itemAt(i).widget()==widget:
                name = widget.text()


    def getDash(self):
        self.clearLayout(self.grid)
        self.clearLayout(self.layout)
        self.backButton = qt.QPushButton("<")
        self.backButton.clicked.connect(self.getHome)
        self.layout.addWidget(self.backButton)
    
    def addGrid(self):
        home = qt.QWidget()
        home.setLayout(self.grid)

        self.layout.addWidget(home)
        self.setLayout(self.layout)


    def clearLayout(self,layout):
        
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

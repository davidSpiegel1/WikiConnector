import os
import subprocess
import sys
from model.OS.dbEngine import *
from model.Module import *
try:
    import PyQt5.QtWidgets as qt
    import PyQt5.QtCore as qCore
    import PyQt5.QtGui as qGui
except ImportError:
    print("PyQt5 not found. Using pip to install")
    subprocess.check_call([sys,executable,"-m","pip","install","PyQt5"])

class terminal(App):
    def __init__(self,name,kern):
        #print("TEST P")
        super().__init__(name,kern)
        print("Terminal App")
        self.kern = kern
        self.dbEng = dbEngine(self.kern)
        curStyle = "background-color: #3b4252; color: #eceff4;"



        title = qt.QLabel("Terminal App")
        
        self.display = qt.QLabel("")
        self.display.setStyleSheet(curStyle)
        
        layout = qt.QVBoxLayout()
        layout.addWidget(title)
        
        self.scroll_area = qt.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)
        #curStyle = "background-color: #3b4252; color: #d8dee9;"

        # Text box
        self.textEdit = qt.QLineEdit()
        self.textEdit.returnPressed.connect(self.runCommand)
        self.textEdit.setStyleSheet(curStyle)
        self.setStyleSheet(curStyle)
        
        # Layout needed
        widget_container = qt.QFrame()
        widget_container.setStyleSheet(curStyle)
        self.widget_layout = qt.QVBoxLayout(widget_container)
        self.widget_layout.addWidget(self.display)
        layout.addWidget(self.textEdit)
        
        self.scroll_area.setWidget(widget_container)
        #vert = self.scroll_area.verticalScrollBar()
        #vert.setValue(vert.maximum())
        #self.wid = qt.QWidget()
        self.setLayout(layout)

    def runCommand(self):
        print("running terminal command!")
        command = self.textEdit.text()
        hist = self.display.text()
        t = hist+"\n"+command
        try:
            self.dbEng.scan(command)
            self.dbEng.parse()
            t = t+"\n"+str(self.dbEng.getFlist())
        except Exception as e:
            t = t+"\n"+"Error."+str(e)
        t = t+"\n"
        vert = self.scroll_area.verticalScrollBar()
        vert.setValue(vert.maximum())
        self.display.setText(t)
        self.textEdit.setText("")
        


    def run(self):
        print("Run Test Program...")
        return self



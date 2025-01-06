import os
import subprocess
import sys
import traceback
from model.OS.dbEngine import *
from model.Module import *
try:
    import PyQt5.QtWidgets as qt
    import PyQt5.QtCore as qCore
    import PyQt5.QtGui as qGui
except ImportError:
    print("PyQt5 not found. Using pip to install")
    subprocess.check_call([sys,executable,"-m","pip","install","PyQt5"])


class fileManager(App):
    def __init__(self,name,kern):
        super().__init__(name,kern)
        print("File Manager App")
        self.kern = kern

        #self.grid = qt.QGridLayout()
        self.layout = qt.QHBoxLayout()

        self.overView = qt.QWidget()
        self.listView = qt.QWidget()
        
        
        self.layout.addWidget(self.overView)
        self.layout.addWidget(self.listView)
        self.buildOverView()
        self.buildCurView()
        self.setLayout(self.layout)

    def buildOverView(self):
        home = qt.QPushButton("Now")
        home2 = qt.QPushButton("Now2")

        self.overList = qt.QVBoxLayout()
        self.overList.addWidget(home)
        self.overList.addWidget(home2)

        self.overView.setLayout(self.overList)

    def buildCurView(self):

        home = qt.QLabel("Label")
        self.curList = qt.QVBoxLayout()

        scroll_area = qt.QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        button_container = qt.QFrame()
        button_layout = qt.QVBoxLayout(button_container)

        curNodes = ["F1","F2","F3","F4","F5","F6","F7"]

        #scroll_area.setFixedHeight(self.height()//2)

        for name in curNodes:
            b = qt.QPushButton(name)
            button_layout.addWidget(b)

        scroll_area.setWidget(button_container)


        self.curList.addWidget(home)
        self.curList.addWidget(scroll_area)
        
        self.listView.setLayout(self.curList)
        #self.overList.addWidget(self.overList)
        

    def run(self):
        print("Run File Manager Program...")
        return self

        

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
        #self.buildCurView()
        self.setLayout(self.layout)

    def buildOverView(self,dirName=None):
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        mainVals = self.kern.get_file_system().list_contents()
        dirs = mainVals['directories']
        self.overList = qt.QVBoxLayout()

        for val in dirs:
            b = qt.QPushButton(val)
            b.clicked.connect(lambda checked=False,e=val: self.buildCurViewTrans(e))
            if dirName is not None and dirName==val:
                b.setStyleSheet("background-color: #383f4e;")
            self.overList.addWidget(b)
            

        #home = qt.QPushButton("Now")
        #home2 = qt.QPushButton("Now2")

        #self.overList = qt.QVBoxLayout()
        #self.overList.addWidget(home)
        #self.overList.addWidget(home2)
        if dirName is None and len(dirs) > 0:
            self.buildCurView(dirs[0])

        self.overView.setLayout(self.overList)

    def getMain(self,dirName):
        self.clearLayout(self.layout)
        self.overView = qt.QWidget()
        self.listView = qt.QWidget()
        
        
        self.layout.addWidget(self.overView)
        self.layout.addWidget(self.listView)
        self.buildOverView(dirName)

    def clearCurView(self):
        self.clearLayout(self.curList)
        self.listView.deleteLater()
        self.listView = qt.QWidget()
        self.layout.addWidget(self.listView)


    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def buildCurViewTrans(self,dirName):
        #self.kern.get_file_system().
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        self.getMain(dirName)
        self.buildCurView(dirName)

    def buildCurView(self,dirName,goBack=False):

        if goBack:
            self.clearCurView()
        home = qt.QLabel(dirName)
        self.curList = qt.QVBoxLayout()

        scroll_area = qt.QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        button_container = qt.QFrame()
        button_layout = qt.QVBoxLayout(button_container)

        try:
            if not goBack:
                self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
            self.kern.get_file_system().change_directory(dirName)
        except Exception as e:
            raise ValueError("Error. No Dir in fileManager.py")
        curNodes = self.kern.get_file_system().list_contents()#["F1","F2","F3","F4","F5","F6","F7"]

        #scroll_area.setFixedHeight(self.height()//2)


        #for name in curNodes:
        #    b = qt.QPushButton(name)
        #    button_layout.addWidget(b)
        dirs = curNodes['directories']
        for d in dirs:
            b = qt.QPushButton(d)
            b.clicked.connect(lambda checked=False,e=d: self.buildCurView(e,goBack=True))
            button_layout.addWidget(b)

        files = curNodes['files']
        for f in files:
            b = qt.QPushButton(f)
            button_layout.addWidget(b)

        scroll_area.setWidget(button_container)


        self.curList.addWidget(home)
        self.curList.addWidget(scroll_area)
        
        #self.overList.addWidget(self.overList)
        self.listView.setLayout(self.curList)
        

    def run(self):
        print("Run File Manager Program...")
        return self

        

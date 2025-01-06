import os 
import subprocess
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qCore
import PyQt5.QtGui as qGui
from model.OS.Kernel import *


# The Module class gives an abstract overview of the two major data manipulation and viewing objects
class Module(qt.QWidget):
    def __init__(self,name):
        super().__init__()
        self.name = name
        self.theme = None

    # Must get this done soon. Have ability for mass setting of theme.
    def setTheme(self,theme):
        self.theme = theme
    
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
    def __init__(self,name):
        super().__init__(name)
        self.conName = f"{name}"
        self.URL = None
    
    def run(self):
        print("Running Connector...")
        return self





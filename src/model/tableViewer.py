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
    print("PyQt5 not found. Using pip to install.")
    subprocess.check_call([sys,executable,"-m","pip","install","PyQt5"])


class tableViewer(App):
    def __init__(self, name, kern):
        print("Running table viewer")
        self.kern = kern

        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.layout.addWidget(self.table)
    def placeData(data,rowNum,colNum):
        for i in range(rowNum):
            for j in range(colNum):
                self.table.item(i,j,qt.QTableWidgetItem(data[i][j]))

    def run(self):
        print("Running table viewer...")
        return self

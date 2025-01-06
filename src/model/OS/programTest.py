import os
import subprocess
import sys

try:
    import PyQt5.QtWidgets as qt
    import PyQt5.QtCore as qCore
    import PyQt5.QtGui as qGui
except ImportError:
    print("PyQt5 not found. Using pip to install")
    subprocess.check_call([sys,executable,"-m","pip","install","PyQt5"])

class programTest:
    def __init__(self):
        print("TEST P")

        print("TEST PROGRAM!!")
        
        button = qt.QLabel("HELLO!!")

        # Layout needed
        layout = qt.QHBoxLayout()
        layout.addWidget(button)

        self.wid = qt.QWidget()
        self.wid.setLayout(layout)
    def run(self):
        print("Run Test Program...")
        return self.wid



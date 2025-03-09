import os
import io
import subprocess
import sys
import traceback
from model.OS.dbEngine import *
from model.Module import *
import PyQt5.QtWidgets as qt
import PyQt5.QtCore as qCore
import PyQt5.QtGui as qGui

class power(App):
    def __init__(self,name,parent,kern):
        super().__init__(name,kern)
        print("Power App")
        self.kern = kern
        self.parent = parent
        # Needed layouts
        self.hBox = qt.QHBoxLayout()
        self.hLabel = qt.QHBoxLayout()
        self.vBox = qt.QVBoxLayout()
        

        # Go to power home
        self.powerHome()



    def powerHome(self):


        #** Testing parent functionality **
        #self.parent.sayHello()
        self.size = 100
        self.path = "view/assets/"
        #self.setStyleSheet("QToolButton{ border-radius: 5px; border: 1px solid #ccc;} QToolButton:hover{ background-color: #dcdcdc;}")

        # Shutdown button
        self.shutdown = qt.QToolButton()
        self.shutdown.setText("Shutdown")
        #pixMap3 = qGui.QPixmap(self.path+"Power.png")
        #mask3 = pixMap3.createMaskFromColor(qCore.Qt.transparent,qCore.Qt.MaskInColor)
        #coloredP3 = qGui.QPixmap(pixMap3.size())
        #coloredP3.fill(qGui.QColor("#F5F5F5"))
        #coloredP3.setMask(mask3)
        self.shutdown.setIcon(qGui.QIcon(self.path+"Power.png"))
        self.shutdown.setIconSize(qCore.QSize(self.size,self.size))
        self.shutdown.setStyleSheet("QToolButton:hover{"+f"qproperty-icon: url({self.path}Power.png);"+"}")
        self.shutdown.setToolButtonStyle(qCore.Qt.ToolButtonTextUnderIcon)
        self.shutdown.clicked.connect(self.shutDownInstance)
        self.hBox.addWidget(self.shutdown)

        shutdownLabel = qt.QLabel("Shutdown")
        self.hLabel.addWidget(shutdownLabel)

        # Reboot button
        self.reboot = qt.QToolButton()
        self.reboot.setText("Reboot")
        self.reboot.setIcon(qGui.QIcon(self.path+"Reboot.png"))
        self.reboot.setIconSize(qCore.QSize(self.size,self.size))
        self.reboot.setToolButtonStyle(qCore.Qt.ToolButtonTextUnderIcon)
        self.hBox.addWidget(self.reboot)

        rebootLabel = qt.QLabel("Reboot")
        self.hLabel.addWidget(rebootLabel)

        # Lock button
        self.lock = qt.QToolButton()
        self.lock.setText("Lock")
        self.lock.setIcon(qGui.QIcon(self.path+"Lock.png"))
        self.lock.setIconSize(qCore.QSize(self.size,self.size))
        self.lock.setToolButtonStyle(qCore.Qt.ToolButtonTextUnderIcon)
        self.lock.clicked.connect(self.lockUser)
        self.hBox.addWidget(self.lock)

        lockLabel = qt.QLabel("Lock")
        self.hLabel.addWidget(lockLabel)


        # Logout button
        self.logout = qt.QToolButton()
        self.logout.setText("Logout")
        self.logout.setIcon(qGui.QIcon(self.path+"Logout.png"))
        self.logout.clicked.connect(self.logoutUser)
        self.logout.setIconSize(qCore.QSize(self.size,self.size))
        self.logout.setToolButtonStyle(qCore.Qt.ToolButtonTextUnderIcon)
        self.hBox.addWidget(self.logout)

        logoutLabel = qt.QLabel("Logout")
        self.hLabel.addWidget(logoutLabel)

        # Cancel button
        self.cancel = qt.QToolButton()
        self.cancel.setText("Cancel")
        self.cancel.setIcon(qGui.QIcon(self.path+"Cancel.png"))
        self.cancel.setIconSize(qCore.QSize(self.size,self.size))
        self.cancel.setToolButtonStyle(qCore.Qt.ToolButtonTextUnderIcon)
        self.hBox.addWidget(self.cancel)

        cancelLabel = qt.QLabel("Cancel")
        self.hLabel.addWidget(cancelLabel)

        h1 = qt.QWidget()
        h1.setLayout(self.hBox)
        h2 = qt.QWidget()
        h2.setLayout(self.hLabel)

        self.vBox.addWidget(h1)
        # Do this if icon with words fails
        #self.vBox.addWidget(h2)
        self.setLayout(self.vBox)

    def logoutUser(self):
        self.parent.sayHello()
        self.parent.setUnlocked(False)
        self.kern.logout()
        self.parent.revertDefaultStyle()
        self.parent.usersScreen()

    def lockUser(self):
        self.parent.setUnlocked(False)
        #self.kern.logout()
        self.parent.revertDefaultStyle()
        self.parent.loginScreen(self.kern.get_current_user())

    def shutDownInstance(self):
        self.parent.shutDown()


    def run(self):
        #self.parent = parent
        print("Run power program...")
        return self

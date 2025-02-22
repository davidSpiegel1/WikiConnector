# Will be the main program that runs everything else
# We will need imports from controller model and view
import platform
import subprocess
import sys
import os
from install import *
#os_name = platform.system()
install = Install() 
try:
    import PyQt5.QtWidgets as qt
    import PyQt5.QtCore as qCore
    import PyQt5.QtGui as qGui
except ImportError as e:
    print("Error importing PyQt.",e)
    install.installPyQt()

try:
    from PIL import Image, ImageCms
except ImportError:
    print("Error importing PIL")
    install.installPIL()
"""try:
    import screeninfo
except ImportError:
    print("Error importing screeninfo")
    install.installScreenInfo()"""
"""try:
    import tkinter as tk
except ImportError:
    print("Error importing tk")
    install.installTkinter()"""



from model.OS.Kernel import *
from model.OS.dbEngine import *
from model.OS.notVim import *
from model.OS.programTest import *
from model.terminal import *
from model.settings import *


from model.fileManager import *
#from view.view2 import *
from view.View import *
from model.wiki import *
from model.connectors import *

k = Kernel()
dbEng = dbEngine(k)
lib_apps = {"notVim":notVim,"View":View,"programTest":programTest,"terminal":terminal,"settings":settings,"fileManager": fileManager,"wiki":wiki,"connectors":connectors}
k.register_lib_app(lib_apps)
#k.login(k.get_root(),"root")
print(f"Login to a user: {k.get_users()}")
username = input("username: ")
password = input("password: ")
k.login(username,password)
s = input(f"{k.get_current_user()}$ ")
while len(s) > 0:
    dbEng.scan(s)
    dbEng.parse()
    print(">",dbEng.getFlist())
    s = input(f"{k.get_current_user()}$ ")


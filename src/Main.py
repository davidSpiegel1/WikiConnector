# Will be the main program that runs everything else
# We will need imports from controller model and view
"""from controller.controller import *
import sys
sys.path.append("view")
sys.path.append("model")
#from view import * 
import view
import dbEngine 
from model import Entry
from model import dbEngine
#from view import customNotebook



app = view.App()
app.mainloop()"""

from model.OS.Kernel import *
from model.OS.dbEngine import *
from model.OS.notVim import *
from model.OS.programTest import *
from model.terminal import *
from model.settings import *
from model.fileManager import *
#from view.view2 import *
from view.View import *

k = Kernel()
dbEng = dbEngine(k)
lib_apps = {"notVim":notVim,"View":View,"programTest":programTest,"terminal":terminal,"settings":settings,"fileManager": fileManager}
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


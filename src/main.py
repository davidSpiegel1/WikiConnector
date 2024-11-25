# Will be the main program that runs everything else
# We will need imports from controller model and view
from controller.controller import *
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
app.mainloop()

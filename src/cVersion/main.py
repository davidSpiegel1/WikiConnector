# The idea about this file is that it will allow for the python version or the c++ version to be ran
from subprocess import call
import sys
import os


def cppClean():
	call(["make", "-f","myMake","clean"])

def cppMake():
	call(["make","-f","myMake"])

def cppRun():
	call(["./ConnectorApp"])

def pyRun():
	#call(["cd .."])
	path = os.path.abspath(os.getcwd())+"/pythonVersion"
	os.chdir(path)
	os.system("python3 main.py")
def pyRun2():
	call(["python3 pyConnector.py"])

def selectVersion(version):
	sv = ""

	if version.lower() in ("c++","c"):
		sv = "c++"
	elif version.lower() in ("python","py"):
		sv = "py"
	else:
		sv = "NONE"
	return sv
def selectOption(option):
	sv = ""
	if option in ("run","r"):
		sv = "r"
	elif option in ("edit","e"):
		sv = "e"
		
	else:
		sv = "NONE"
	return sv
def printError(arg):
	raise Exception(arg)
	exit(-1)

def run (language):
	if language == "c++":
		print("Running c++ version..")
		cppClean()
		cppMake()
		cppRun()
	if language == "py":
		#pyMove()
		pyRun()
		
#def main():
n = len(sys.argv)
finalStr = ""
firstWord = ""
if n > 1:
	firstWord = sys.argv[1]

for word in range(1,n):
	finalStr += sys.argv[word]
if firstWord == "-v":
	if n > 2:
		version = selectVersion(sys.argv[2])
		if n>3:
			option = selectOption(sys.argv[3])
			print("What the option was: ",option)
			if option == "r":
				print("What is going into run",version)
				run(version)
		else:
			printError("No option selected! Terming Program")
	else:
		printError("version not selected! Terminating Program.")





print("The final string: ",finalStr)
print("The first word: ",firstWord)



print("IDEA: To allow for the python version or the c++ version to be ran!")






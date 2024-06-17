# The idea about this file is that it will allow for the python version or the c++ version to be ran
from subprocess import call
import sys


def cppClean():
	call(["make", "-f","myMake","clean"])

def cppMake():
	call(["make","-f","myMake"])

def cppRun():
	call(["./ConnectorApp"])

#def main():
n = len(sys.argv)
finalStr = ""
for word in range(1,n-1):
	finalStr += sys.argv[word]

print(finalStr)


print("IDEA: To allow for the python version or the c++ version to be ran!")






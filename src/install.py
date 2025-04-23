# A script to install all the needed data.
# This script is called when something goes wrong.
#import platform
import subprocess
import sys
import os
import distro

class Install:
    def __init__(self):
        print("Installing tk for diffrent distros")
        name = distro.id()
try:
    import tk
except ImportError:
    print("Error installing tk")
    if name in ("ubuntu","linuxmint"):
        subprocess.check_call(["sudo","apt","install","python3-tk","-y"])
        print("tk installed on ubuntu")
    if name == "arch":
        subprocess.check_call(["sudo","pacman","-S","tk"])
        print("tk installed on arch")
    if name == "fedora":
        subprocess.check_call(["sudo","dnf","install","python3-tkinter","-y"])
        print("tk installed on linuxmint")
    else:
        print("Not supported yet.")
        #subprocess.check_call(["Python3","-m","pip","install","tk"])
            

            


"""

class Install:
    def __init__(self):

        self.os_name = platform.system()
        self.distro = ""
        if self.os_name=="Linux":
            print("Running on Linux")
            self.distro = self.get_distro()

        elif self.os_name=="Darwin":
            print("Running on MacOS")
        else:
            self.distro = "windows"
    


    

    def installPyQt(self):
        if self.distro=="arch":
            subprocess.check_call(["sudo","pacman","-S","--noconfirm","python-pyqt5"])
            print("PyQt5 installed on arch")
        elif self.os_name=="Darwin":
            subprocess.check_call([sys.executable,"-m","pip","install","PyQt5"])
            print("PyQt5 installed on macOS")

    def installPIL(self):
        if self.distro=="arch":
            subprocess.check_call(["sudo","pacman","-S","--noconfirm","python-pillow"])
            print("PIL installed on arch")
        elif self.os_name=="Darwin":
            subprocess.check_call([sys,executable,"-m","pip","install","PIL"])

    # Finish tmw
    def installScreenInfo(self):
        if self.distro=="arch":
            # import screeninfo
            subprocess.check_call(["sudo","pacman","-S","--noconfirm","python-screeninfo"])
            print("screninfo installed on arch")
        elif self.os_name == "Darwin":
            subprocess.check_call([sys,executable,"-m","pip","install","screeninfo"])

    def installTkinter(self):
        if self.distro=="arch":
            subprocess.check_call(["sudo","pacman","-S","tk"])
            print("tk installed on arch")
        elif self.os_name == "Darwin":
            subprocess.check_call([sys,executable,"-m","pip","install","tk"])
            

    def get_distro(self):
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID="):
                        return line.strip().split("=")[1].strip('"')
                return "unknown linux distro"
        except FileNotFoundError:
            return "Error: os-release not found in linux system."
"""

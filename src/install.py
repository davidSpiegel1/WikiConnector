# A script to install all the needed data.
# This script is called when something goes wrong.
import platform
import subprocess
import sys
import os


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
            subprocess.check_call(["sudo","pacman","-S","--noconfirm","python-pil"])
            print("PIL installed on arch")
        elif self.os_name=="Darwin":
            subprocess.check_call([sys,executable,"-m","pip","install","PIL"])

    # Finish tmw
    def installScreenInfo(self):
        if self.distro=="arch":
            # import screeninfo
            subprocess.check_call(["sudo","pacman","-S","noconfirm","python-screeninfo"])
            print("screninfo installed on arch")
        elif self.os_name == "Darwin":
            subprocess.check_call([sys,executable,"-m","pip","install","screeninfo"])
            

    def get_distro(self):
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID="):
                        return line.strip().split("=")[1].strip('"')
                return "unknown linux distro"
        except FileNotFoundError:
            return "Error: os-release not found in linux system."


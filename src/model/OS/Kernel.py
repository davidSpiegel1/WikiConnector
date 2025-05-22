


# Okay, so the idea here is that we will have a Kernel that does all the 'OS-like' behavior.
# Duties: (1) opening files (2) running applications (3) maintaining the file hiarchy

import os
import pickle
import importlib
import traceback
from model.OS.dbEngine import *
from model.OS.notVim import *
#from model.OS.programTest import *
from model.terminal import *
from model.Module import *
from view.View import *
import tkinter as tk
import getpass
# Class fileSystem to simulate a real os file system
class FileSystem:
    
    # File iNode
    class FileNode:
        def __init__(self,name,data):
            self.name = name
            self.data = data
    # Directory iNode
    class DirectoryNode:
        def __init__(self,name):
            self.name = name
            self.file = {}
            self.subdirectories = {}
            self.parent_directory = None
    # Going to grab a python data file stored in pickle file
    def __init__(self,p="file_system.pkl"):
        self.pickle = p
        if os.path.exists(self.pickle):
            self.load_file_system()
            self.home = self.root.subdirectories['home']
        else:
            self.root = self.DirectoryNode("root")
            self.current_directory = self.root
            self.parent_directory = None
            self.current_directory.parent_directory = None
            #self.save_file_system()
            self.home = None
            self.create_default_dirs()
            self.save_file_system()
    
    # Need to be able to save the file system itself
    def save_file_system(self):
        with open(self.pickle,"wb") as f:
            pickle.dump(self.root,f)

    # Need to be able to load the simulated python object file system
    def load_file_system(self):
        with open(self.pickle,"rb") as f:
            self.root = pickle.load(f)
        self.current_directory = self.root
        self.parent_directory = None

    def get_current_directory(self):
        return self.current_directory

    # Need to create a file as well 
    def create_file(self,name,content):
        self.current_directory.file[name] = self.FileNode(name,content)
        self.save_file_system()

    # Must have the ability to create new directories
    def create_directory(self,name):
        if name not in self.current_directory.subdirectories:
            self.current_directory.subdirectories[name] = self.DirectoryNode(name)
            self.save_file_system()
        else:
            raise ValueError("Error. Directory already exists.")

    # Must be able to delete and create directory nodes and file nodes
    def delete_directory(self, name):
        if name in self.current_directory.subdirectories:
            del self.current_directory.subdirectories[name]
            self.save_file_system()
        else:
            raise ValueError(f"Directory '{name}' is missing")
    def delete_file(self,name):
        if name in self.current_directory.file:
            del self.current_directory.file[name]
            self.save_file_system()
        else:
            raise ValueError(f"File '{name}' is not found")
    def open_file(self,name):
        if name in self.current_directory.file:
            return self.current_directory.file[name].data
        else:
            raise ValueError(f"File '{name}' cannot be opened")
    
    def change_directory(self,name):
        if name == "..":
            if self.parent_directory:
                self.current_directory = self.current_directory.parent_directory
                self.parent_directory = self.current_directory.parent_directory
            else:
                self.current_directory = self.root
        elif name in self.current_directory.subdirectories:
            self.parent_directory = self.current_directory
            self.current_directory = self.current_directory.subdirectories[name]
            self.current_directory.parent_directory = self.parent_directory
        else:
            raise ValueError(f"Dirctory '{name}' Not FOUND!")

    def create_default_dirs(self):

        self.home = self.DirectoryNode("home")
        self.root.subdirectories["home"]= self.home
        self.makeEtcDir(self.root)
        
        # So root can use connectors
        mod = self.DirectoryNode("Modules")
        con = self.DirectoryNode("Connectors")
        mod.subdirectories["Connectors"] = con
        self.root.subdirectories["Modules"] = mod

    def makeEtcDir(self, root):
        # Must make the needed .config things soon!
        etc = self.DirectoryNode("etc")
        etc.file["group"] = self.FileNode("group","admin: root")
        root.subdirectories["etc"] = etc
        

    def create_user_home(self,username):
        if username in self.home.subdirectories:
            print(f"Home directory for user '{username}' already exists")
        else:
            self.home.subdirectories[username] = self.DirectoryNode(username)
            self.home.subdirectories[username].subdirectories["Documents"] = self.DirectoryNode("Documents")
            self.home.subdirectories[username].subdirectories["Downloads"] = self.DirectoryNode("Downloads")
            self.home.subdirectories[username].subdirectories["Modules"] = self.DirectoryNode("Modules")

            # Making needed config data
            self.createConfig(self.home.subdirectories[username].subdirectories["Modules"],username)
            # Making directory for connectors 
            self.home.subdirectories[username].subdirectories["Modules"].subdirectories["Connectors"] = self.DirectoryNode("Connectors")
            self.home.subdirectories[username].subdirectories["Modules"].subdirectories["Connectors"].subdirectories["Data"] = self.DirectoryNode("Data")

            self.save_file_system()

    def createConfig(self,dirs,username):
        config = self.DirectoryNode("Config")
        
        config.file["desktop.config"] = self.FileNode("desktop.config","background-image=None;background-position=center;")
        config.file["theme.config"] = self.FileNode("theme.config","title=None;background=None;foreground=None;")
        config.file["userIcon.config"] = self.FileNode("userIcon.config","url:None;color:black")
        config.file["font.config"] = self.FileNode("font.config","family=None;size=None")
        dirs.subdirectories["Config"] = config
        
        return dirs

    def switch_to_user_home(self,username):
        if username in self.home.subdirectories:
            self.current_directory = self.home.subdirectories[username]
        elif username == self.get_root():
            self.current_directory = self.root
            self.parent_directory = None
        else:
            raise ValueError(f"Home directory '{username}' not found.")
    def get_admin(self):
        #print("What is admin: ",self.root.subdirectories["etc"].file["group"].data.split("admin:")[1].strip().split(","))
        # Must remember to not allow usernames with ':' in title.
        return self.root.subdirectories["etc"].file["group"].data.split("admin:")[1].strip().split(",")

    def mod_admin(self,old_user,new_user):

        if old_user in self.get_admin():
            # Replace with new user
            adminList = self.get_admin()
            adminList[adminList.index(old_user)] = new_user
            print("NEW Admin List: ",adminList)
            #print("New CSV Admin List: ",','.join(adminList))
            newAdminList = '.'.join(adminList)
            print("New CSV Admin List: ",newAdminList)
            # Set admin list
            self.root.subdirectories["etc"].file["group"] = self.FileNode("group","admin: "+newAdminList)
            self.save_file_system()

        else:
            raise ValueError(f"Admin {old_user} not found, yet listed.")


    def get_root(self):
        try:
            return self.get_admin()[0].strip()
        except Exception as e:
            raise IndexError(f"Error finding admin {e}")


    def list_contents(self):
        return {
            "directories": list(self.current_directory.subdirectories.keys()),
            "files" : list(self.current_directory.file.keys()),
                }

    def rename_user_dir(self,oldname,newname):
        if oldname in self.home.subdirectories:
            self.home.subdirectories[newname] = self.home.subdirectories[oldname]
            del self.home.subdirectories[oldname]
            self.save_file_system()
        elif oldname == self.get_root():
            print("Changing root.")
        else:
            raise ValueError(f"Home directory '{username}' not found.")

# Making the final Kernel class
class Kernel:
    def __init__(self):
        self.file_system = FileSystem()
        self.apps = {}
        self.libs = None
        self.users = {"root":"root"}
        #self.load_users()
        self.current_user = None
        self.prog_file = "prog_registry.pkl"
        self.users_file = "user_registry.pkl"
        self.load_users()


        
    def get_file_system(self):
        return self.file_system

    def get_current_user(self):
        return self.current_user

    def get_users(self):
        users = []
        for username in self.users:
            users.append(username)
        return users

    def logout(self):
        print(f"User '{self.current_user}' has been logged out.")
        self.current_user = None
        # May change. Kind of bad for security
        self.file_system.switch_to_user_home(self.file_system.get_root())

    # May delete after doing terminal part
    def trigger_login(self,username):
        potPassword = getpass.getpass(f"Please enter password for '{username}': ")
        try:
            self.login(username,potPassword)
        except Exception as e:
            print(f"Error. Incorrect password.")
            potPassword = input(f"Please enter password for '{username}': ")
            try:
                self.login(username,potPassword.strip())
            except Exception as e:
                print("Error. Incorrect password.")

    def trigger_password_reset(self,username):
        currentPassword = input(f"Current '{username}' password: ")
        try:
            curPassword = self.users[username]
        except Exception as e:
            raise ValueError(f"Error. User '{username}' does not exist.")
        if currentPassword == curPassword:
            newPassword = input(f"Enter new password: ")
            self.set_password(username,currentPassword,newPassword)
        else:
            print(f"Error. Password does not match for '{username}'")

    def trigger_username_change(self,username):
        pw = input(f"Input '{username}' password: ")
        try:
            curPassword = self.users[username]
        except Exception as e:
            raise ValueError(f"Error. User '{username}' does not exist.")
        if pw==curPassword:
            new_username = input(f"Enter new username: ")
            self.set_username(username,pw,new_username)
        else:
            print(f"Error. Password does not match for '{username}'")

    def set_username(self,username,password,new_username):
        try:
            if password == self.users[username]:
                self.users[new_username] = password
                self.file_system.rename_user_dir(username,new_username)
                
                del self.users[username]
                if self.current_user==username:
                    self.current_user=new_username
                if username in self.file_system.get_admin():
                    self.file_system.mod_admin(username,new_username)

                self.save_users()
                print(f"Username set for '{username}'")
            else:
                raise ValueError(f"Error. User '{username}' password wrong.")
        except Exception as e:
            raise ValueError(f"Error. User '{username}' may not exist.")
    

    def set_password(self,username,oldPassword,password):
        try:
            if oldPassword == self.users[username]:
                self.users[username] = password.strip()
                self.save_users()
                print(f"Password for '{username}' set as '{password.strip()}'.")
            else:
                raise ValueError(f"Error. User '{username}' may not exist.")
        except Exception as e:
            raise ValueError(f"Error. User '{username}' does not exist.")


    def login(self,username,password):
        if username in self.users and self.users[username]==password:
            self.current_user = username
            self.file_system.switch_to_user_home(username)
            print(f"User '{username}' logged in.")
            return 0
        else:
            #print("Error. Wrong credentials.")
            print(self.users)
            raise ValueError(f"Error. Login to {username} failed.")
            return 1

    def add_user(self,username, password):
        if self.current_user != self.file_system.get_root():
            print("Error: Must have root permissions")
            return
        if username in self.users:
            print(f"User '{username}' is already an account.")
            return
        self.users[username] = password.strip()
        self.file_system.create_user_home(username)
        self.save_users()
        print(f"User '{username}' has been added")



    def save_users(self):
        with open(self.users_file,"wb") as file:
            pickle.dump(self.users,file)
    
    def load_users(self):
        try:
            with open(self.users_file,"rb") as file:
                self.users = pickle.load(file)
        except (FileNotFoundError,EOFError):
            #print("Loading users file failed.")
            self.users = {"root":"root"}
    
    def register_application(self,name,func):
        #self.apps[name] = func
        module_path = func.__module__
        class_name = func.__name__
        self.apps[name] = (module_path,class_name)
        self.save_prog()


    def run_application(self,name, *args, **kwargs):
        if name in self.apps:

            #app_class = self.apps[name]
            module_path,class_name = self.apps[name]
            module = importlib.import_module(module_path)
            app_class = getattr(module,class_name)
            if callable(app_class):
                app_instance= app_class(*args,**kwargs)
                if hasattr(app_instance,"run"):
                    return app_instance.run()
                else:
                    raise AttributeError(f"Application '{name}' not found")
            else:
                print("Not callable: ",app_class)
        else:
            raise ValueError(f"Application '{name}' not found.")
    def run_query(self,connector,query):
        if connector in self.apps:
            print("Connector in apps!")
        #else:


    def save_prog(self):
        with open(self.prog_file,"wb") as file:
            pickle.dump(self.apps,file)

    def load_prog(self):
        try:
            with open(self.prog_file,"rb") as file:
                self.apps = pickle.load(file)
        except (FileNotFoundError,EOFError):
            self.apps = {}

    def get_apps_name(self):
        names = []
        for name in self.apps:
            print(self.apps[name])
            if name in self.libs:
                if issubclass(self.libs[name],App):
                    names.append(name)
                    
                else:
                    print("Name a lib but not instance",name)
                    print("Instance: ",self.libs[name])
            #names.append(name)
        return names
    def get_apps(self):
        return self.apps

    def register_lib_apps(self):
        if os.path.exists(self.prog_file):
            self.load_prog()
        else:
            try:
                self.register_application("myApp",MyApp)
            except Exception as e:
                print("Error registering my_app",e)
            try:
                self.register_application("guiApp",TkProg)
            except Exception as e:
                print("Error registering guiApp",e)
            try:
                self.register_application("notVim",notVim)
            except Exception as e:
                print("Error registering notvim",e)
            #try:
            #    self.register_application("programTest",programTest)
            #except Exception as e:
            #    print("Error registering programTest",e)

    def register_lib_app(self,libs):
        self.libs = libs
        if os.path.exists(self.prog_file):
            self.load_prog()
        else:
            for name in libs:
                try:
                    self.register_application(name,libs[name])
                except Exception as e:
                    print(f"Error registering '{name}' app")

"""def main():
    k = Kernel()
    dbEng = dbEngine(k)
    k.register_lib_apps()
    k.get_file_system().create_file("HEL.txt","HII MY NAME IS DAVID")
    k.login("root","root")
    s = input(f"{k.get_current_user()}$ ")
    while len(s) > 0:
        dbEng.scan(s)
        dbEng.parse()
        print(">",dbEng.getFlist())
        s = input(f"{k.get_current_user()}$ ")"""
"""try:
        fs = k.get_file_system()
        print(fs.list_contents())
        #fs.delete_file("hello.txt")
        #fs.create_directory("docs")
        k.register_application("my_app",MyApp)
        try:
            k.run_application("my_app",message="HI")
        except Exception as e:
            print(f"ERROR: {e}")

        k.register_application("gui_app",TkProg)
        try:
            k.run_application("gui_app")
        except Exception as e:
            print(f"ERROR: {e}")
        k.register_application("")

        fs.change_directory("docs")
        fs.create_file("hello.py","")
        print(fs.list_contents())
        #print(fs)
        #fs.create_directory("docs")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()"""
#main()
        


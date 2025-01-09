import os 
import io
import subprocess
import sys
import traceback
from model.OS.dbEngine import *
from model.Module import *
try:
    import PyQt5.QtWidgets as qt
    import PyQt5.QtCore as qCore
    import PyQt5.QtGui as qGui
except ImportError:
    print("PyQt5 not found. Using pip to install")
    subprocess.check_call([sys,executable,"-m","pip","install","PyQt5"])

try:
    from PIL import Image, ImageCms
except ImportError:
    print("PIL not found. Using pip to install")
    subprocess.check_call([sys,executable,"-m","pip","install","PIL"])

class settings(App):
    def __init__(self,name,kern):
        super().__init__(name,kern)
        print("Settings App")
        self.kern = kern
        #self.settingsHome()
        
        # Needed layouts
        self.grid = qt.QGridLayout()
        self.layout = qt.QVBoxLayout()
    
        # Needed back button
        #self.backButton = qt.QPushButton("<")
        #self.backButton.clicked.connect(self.settingsHome)
        #self.layout.addWidget(self.backButton)

        #Setting the settings home:
        self.settingsHome()
        

    def settingsHome(self):
        #self.clearLayout(self.grid)
        self.getDash()
        self.userInfo = qt.QPushButton(f'{self.kern.get_current_user()} \nUsername, password')
        self.userInfo.setStyleSheet("font-size: 15px;")
        self.userInfo.clicked.connect(self.userInformation)
        self.grid.addWidget(self.userInfo,1,1,1,2)
        #self.backButton = qt.QPushButton("<")
        #self.backButton.connect(self.
        # Need four things: UserInfo, Desktop and Themes, Font, Sound
        
        # Desktop
        desktop = qt.QPushButton("Desktop")
        desktop.clicked.connect(self.desktopChange)
        self.grid.addWidget(desktop,2,1)

        # Themes 
        themes = qt.QPushButton("Themes")
        themes.clicked.connect(self.themesChange)
        self.grid.addWidget(themes,2,2)

        # Font
        font = qt.QPushButton("Font")
        font.clicked.connect(self.fontChange)
        self.grid.addWidget(font,3,1)

        # Sound
        sound = qt.QPushButton("Sound")
        sound.clicked.connect(self.soundChange)
        self.grid.addWidget(sound,3,2)

        # Users
        users = qt.QPushButton("Users+Groups")
        users.clicked.connect(self.userGroupsChange)
        self.grid.addWidget(users,4,1)

        # Sharing
        sharing = qt.QPushButton("Sharing")
        self.grid.addWidget(sharing,4,2)





        home = qt.QWidget()
        home.setLayout(self.grid)


        #self.layout = qt.QVBoxLayout()
        
        self.layout.addWidget(home)
        self.setLayout(self.layout)


    def desktopChange(self):
        
        self.getDash()
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        if self.kern.get_current_user()!=self.kern.get_file_system().get_root():
            print("Looking at config dir...")
            self.kern.get_file_system().change_directory("Modules")
            self.kern.get_file_system().change_directory("Config")
            data = self.kern.get_file_system().open_file("desktop.config")

            print("gathered 'desktop.config' file")
            splitData = data.strip().split(";")
            # Background image
            backgroundImage = splitData[0].split("=")[1]
            backgroundImageLabel = qt.QLabel("Desktop Image: ")
            self.grid.addWidget(backgroundImageLabel,1,1)
            # Value
            #backgroundImageVal = qt.QLineEdit()
            #backgroundImageVal.setText(backgroundImage)
            #self.grid.addWidget(backgroundImageVal,1,2)
            self.backgroundImageDropdown = qt.QComboBox(self)
            curList = ["None","spaceNord.png","mountainNord.png","bridgeNord.png","waterNord.png","treeNord.png","lakeNord.png","davidNord.png"]
            finalList = [backgroundImage]
            for name in curList:
                if backgroundImage != name:
                    finalList.append(name)
                    
            self.backgroundImageDropdown.addItems(finalList)
            #self.backgroundImageDropdown.currentTextChanged.connect(self.onTextChanged)
            self.grid.addWidget(self.backgroundImageDropdown,1,2)

            self.desktopPage = qt.QWidget()
            # Save
            backgroundImageButton = qt.QPushButton("Save")
            backgroundImageButton.clicked.connect(lambda checked=False,e="background-image=": self.modifyBackgroundImage(self.backgroundImageDropdown.currentText()))

            self.grid.addWidget(backgroundImageButton,1,3)

            self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
            # Background position

        self.desktopPage = qt.QWidget()
        self.desktopPage.setLayout(self.grid)
        self.layout.addWidget(self.desktopPage)

    def onTextChanged(self,text):
        if text != "None":
            path = "view/assets/nordTheme/"+text
            self.setStyleSheet(".QWidget{"+f"border-image: url('{path}') 0 0 0 0 stretch stretch"+";}")
            self.parent().setStyleSheet(".QWidget{"+f"border-image: url('{path}') 0 0 0 0 stretch stretch"+";}")

        else:
            self.setStyleSheet("")



    def modifyBackgroundImage(self,value):
        try:
            if value != "None":
                path = "view/assets/nordTheme/"+value
                self.setObjectName("box")
                #self.setStyleSheet("QWidget#box{"+f"background-image: url('{path}');"+"background-position: center;"+"background-repeat: no-repeat;}")
                #self.convert_to_srgb(path)
                #self.setStyleSheet(".QWidget{"+f"border-image: url('{path}') 0 0 0 0 stretch stretch"+";}")
                self.setStyleSheet(".QWidget{"+f"border-image: url('{path}')"+";}")
                # Must fix performance issue when possible.
                #self.parent().setStyleSheet(".QWidget{"+f"border-image: url('{path}')"+";}")


            else:
                self.setStyleSheet("")
        except Exception as e:
            print("Error loading file for background image. Path:",value)
            print(e)
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        self.kern.get_file_system().change_directory("Modules")
        self.kern.get_file_system().change_directory("Config")
        self.saveFileToSystem("desktop.config","background-image="+value)
        print("Going to switch to user home!")
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())

    def saveFileToSystem(self,file,data):
        try:
            print(f"Saving the file system for data: {data}")
            #print("Current text: ",self.backgroundImageDropdown.currentText())
            self.kern.get_file_system().create_file(file,data)
            #self.kern.get_file_system().save_file_system()
        except Exception as e:
            print(f"Error loading file: '{file}'.")

    def themesChange(self):
        print("Theme change!")
        self.getDash()

        submit = qt.QPushButton("Submit")
        self.grid.addWidget(submit,1,1)

        if self.kern.get_current_user()!=self.kern.get_file_system().get_root():
            print("Looking at config dir...")
            self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())

            self.kern.get_file_system().change_directory("Modules")
            self.kern.get_file_system().change_directory("Config")
            data = self.kern.get_file_system().open_file("theme.config")

            print("gathered 'theme.config' file")
            splitData = data.strip().split(";")

            # Background color
            themeName = splitData[0].split("=")[1]
            


            # Possible themes
            self.themeDropdown = qt.QComboBox(self)
            curList = ["None","Midnight","Day","Dawn"]
            finalList = [themeName]
            for name in curList:
                if themeName != name:
                    finalList.append(name)

            self.themeDropdown.addItems(finalList)
            #self.themeDropdown.currentTextChanged.connect(self.onTextChanged)
            submit.clicked.connect(self.changeTheme)
            self.grid.addWidget(self.themeDropdown,1,2)
        else:
            themeName = ["None"]
            themeDropdown = qt.QComboBox(self)
            themeDropdown.addItems(themeName)
            self.grid.addWidget(themeDropdown,1,2)

        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())


        themePage = qt.QWidget()
        themePage.setLayout(self.grid)
        self.layout.addWidget(themePage)

    def changeTheme(self):
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        self.kern.get_file_system().change_directory("Modules")
        self.kern.get_file_system().change_directory("Config")
        #data = self.kern.get_file_system().open_file("theme.config")

        theme = self.themeDropdown.currentText()
        background = "None"
        foreground = "None"
        if theme == "Midnight":
            background = "#4c566a"
            foreground = "#e5e9f0"
        elif theme=="Day":
            background = "#D08770"
            foreground = "#ebcb8b"
        elif theme=="Dawn":
            background = "#bf616a"
            foreground = "#f2ceeb"
        else:
            background = "#5e81ac"
            foreground = "#e5e9f0"

        #self.setStyleSheet(""+f"background-color: {background}; color: {foreground};"+"")
        self.parent().setStyleSheet(
                        "QWidget{"+ f"color: {foreground}; background-color: {background};"+"}"+
                        "QTabBar:tab{"+f"background: {background};border: 2px solid {foreground};"+"}"+
                        "QTabBar::tab:hover{"+f"background-color: {foreground}; color: {background};"+"}"+
                        "QPushButton:hover{"+f"background-color: {foreground}; color: {background};"+"}"+
                        "QPushButton#close{background: transparent; border: none;}"+
                        "QPushButton#close:hover{color: #bf616a;}")

        data = f"title={theme};background={background};foreground={foreground};"
        self.saveFileToSystem("theme.config",data)
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        print("The current theme: ",theme)

    def userGroupsChange(self):
        print("User Groups change!")

        self.getDash()

        if self.kern.get_current_user()==self.kern.get_file_system().get_root():
            admin = qt.QLabel("Admin: ")
            self.grid.addWidget(admin,1,1)
            root = qt.QLabel(self.kern.get_file_system().get_root())
            self.grid.addWidget(root,1,2)

            users = self.kern.get_users()

            userLabel = qt.QLabel("Users: ")
            self.grid.addWidget(userLabel,2,1)

            scroll = qt.QScrollArea(self)
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(self.height()//4)
            self.grid.addWidget(scroll,2,2)

            b_con = qt.QFrame()
            self.b_lay = qt.QVBoxLayout(b_con)

            for user in users:
                b = qt.QLabel(user)
                self.b_lay.addWidget(b)
            scroll.setWidget(b_con)


            addUser = qt.QPushButton("Add User")
            addUser.clicked.connect(self.newUser)
            self.grid.addWidget(addUser,3,2)


        groupPage = qt.QWidget()
        groupPage.setLayout(self.grid)
        self.layout.addWidget(groupPage)



    def newUser(self):
        print("NEW USER!!")
        newName = qt.QLineEdit(self)
        newName.setPlaceholderText("Name...")
        newName.returnPressed.connect(lambda checked=False,e=newName: self.addUser(e))
        #newName.setVisible(True)
        #newName.resize(200,200)
        #newName.setFixedSize(100,80)
        #self.grid.addWidget(newName)
        self.b_lay.addWidget(newName)

    def addUser(self,widget):
        found = False
        for i in range(self.b_lay.count()):
            if self.b_lay.itemAt(i).widget()==widget:
                name = widget.text()
                if name not in self.kern.get_users():
                    newUser = qt.QLabel(name)
                    self.kern.add_user(name.strip(),'123')
                    self.b_lay.addWidget(newUser)
                    widget.deleteLater()
                    found = True

                else:
                    widget.setPlaceholderText("Must be new name...")
                    widget.setStyleSheet("border: 2px solid red")
                    widget.setText("")
                    found = True
        if not found:
            print("Error. Widget for adding user not found.")

    def fontChange(self):
        print("Font change!")

        
        self.getDash()

        if self.kern.get_current_user()!=self.kern.get_file_system().get_root():
            #self.getDash()
            self.font_list = qt.QComboBox()

            self.grid.addWidget(self.font_list,1,2)

            fFam = [self.parent().font().styleName()]

            for f in qGui.QFontDatabase().families():
                fFam.append(f)

            #fFam = qGui.QFontDatabase.families()
            #fFam = fontDb.families()

            #print(f"f-fam: {fFam}")
            self.font_list.addItems(fFam)
            font_label = qt.QLabel("Fonts: ")
            self.grid.addWidget(font_label,1,1)
            #font_list.currentIndexChanged.connect(lambda checked=False,e=)
            submit = qt.QPushButton("Submit")
            submit.clicked.connect(self.changeFontUsingCurrent)
            self.grid.addWidget(submit,2,1,1,4)

            # Font size
            size_label = qt.QLabel("Font Size: ")
            self.grid.addWidget(size_label,1,3)
            self.font_size = qt.QLineEdit()
            self.font_size.setText("14")
            self.grid.addWidget(self.font_size,1,4)

        fontPage = qt.QWidget()
        fontPage.setLayout(self.grid)
        self.layout.addWidget(fontPage)

    def changeFontUsingCurrent(self,currentFont):
        print("Current Font!!")
        font_name = self.font_list.currentText()
        size = self.font_size.text().strip()
        #font = qGui.QFont(font_name,14)
        #self.setFont(font)
        if len(font_name) > 0 and len(size) > 0:
            try:
                if len(size) == 0:
                    size = '14'
                int_size = int(size)
                self.parent().setStyleSheet("QWidget{"+f"font-family: {font_name}; font-size: {size}px;"+"}")
                self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
                self.kern.get_file_system().change_directory("Modules")
                self.kern.get_file_system().change_directory("Config")
                data = f"family={font_name};size={size}"
                self.saveFileToSystem("font.config",data)
                self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
            except Exception as e:
                print("Error loading font: ",e)
                self.font_size.setStyleSheet("background-color: red;")
        else:
            self.font_size.setStyleSheet("background-color: red;")
            self.font_list.setStyleSheet("border: 2px solid red;")

        

    def soundChange(self):
        print("Sound change!")

    def getDash(self):
        self.clearLayout(self.grid)
        self.clearLayout(self.layout)
        self.backButton = qt.QPushButton("<")
        self.backButton.clicked.connect(self.settingsHome)
        self.layout.addWidget(self.backButton)
        
    def userInformation(self):
        #self.clearLayout(self.grid)
        self.getDash()
        
        userLabel = qt.QLabel(f'Change password for {self.kern.get_current_user()}: ')

        #self.grid.addWidget(userLabel,1,1,1,2)
        self.grid.addWidget(userLabel,1,1)

        newPassword = qt.QLineEdit()
        newPassword.setPlaceholderText("New Password")
        self.grid.addWidget(newPassword,1,2)
        
        #newPassword.setText(self.kern.get
        
        nameLabel = qt.QLabel(f'Change username for {self.kern.get_current_user()}:')
        self.grid.addWidget(nameLabel,2,1)

        newName = qt.QLineEdit()
        newName.setText(self.kern.get_current_user())
        self.grid.addWidget(newName,2,2)

        
        verifyLabel = qt.QLabel("Verify with password: ")
        self.grid.addWidget(verifyLabel,3,1)

        self.verifyPassWord = qt.QLineEdit()
        self.verifyPassWord.setPlaceholderText("password")
        self.grid.addWidget(self.verifyPassWord,3,2)

        submit = qt.QPushButton("Submit")
        submit.clicked.connect(lambda checked=False,e=(newName,newPassword): self.verifyUserInfo(e)) 
        self.grid.addWidget(submit,5,1,1,2)


        passWordPage = qt.QWidget()
        passWordPage.setLayout(self.grid)

        self.layout.addWidget(passWordPage)
        self.setLayout(self.layout)
        #user
        #hLay = qt.QVBoxLayout()
        #hLay.addWidget(buttonPresses)


    def verifyUserInfo(self,tup):
        print("The tup: ",tup)
        username = tup[0].text().strip()
        password = tup[1].text().strip()
        
        try:
            if len(password) > 0:
                self.kern.login(self.kern.get_current_user(),self.verifyPassWord.text())
                self.kern.set_password(self.kern.get_current_user(),self.verifyPassWord.text(),password)
                if self.kern.get_current_user() != username:
                    self.kern.set_username(self.kern.get_current_user(),password,username)#self.verifyPassWord.text(),username)

                # Testing admin lookup
                self.userInformation()
            elif username != self.kern.get_current_user():
                self.kern.login(self.kern.get_current_user(),self.verifyPassWord.text())
                self.kern.set_username(self.kern.get_current_user(),self.verifyPassWord.text(),username)

            else:
                print("Error: No change.")
                tup[0].setStyleSheet("border: 3px solid red;")
                tup[1].setStyleSheet("border: 3px solid red;")
                #self.grid.addWidget(errorLabel,4,1,1,2)
                
        except Exception as e:
            print("Error. Issues loggins in.",e)
            traceback.print_exc()
            self.verifyPassWord.setStyleSheet("border: 3px solid red;")
            self.verifyPassWord.update()

    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def convert_to_srgb(self,file_path):
        """
        Convert PIL image to sRGB color space (if possible)
        and save the converted file.
        """
        img = Image.open(file_path)
        icc = img.info.get('icc_profile', '')
        icc_conv = ''
        if icc:
            io_handle = io.BytesIO(icc)     # virtual file
            src_profile = ImageCms.ImageCmsProfile(io_handle)
            dst_profile = ImageCms.createProfile('sRGB')
            img_conv = ImageCms.profileToProfile(img, src_profile, dst_profile)
            icc_conv = img_conv.info.get('icc_profile','')
        if icc != icc_conv:
            # ICC profile was changed -> save converted file
            img_conv.save(file_path,
                          format = 'JPEG',
                          quality = 50,
                          icc_profile = icc_conv)
    def run(self):
        print("Run settings program...")
        return self

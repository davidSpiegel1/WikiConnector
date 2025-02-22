import os
import subprocess
import sys
import traceback
from controller import controller
from model.Module import *
import io
import tkinter as tk
"""try:
    import screeninfo
except ImportError:
    print("screeninfo not found. Using pip to install")
    subprocess.check_call([sys.executable,"-m","pip","install","screeninfo"])
    import screeninfo"""

try:
    #from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
    import PyQt5.QtWidgets as qt
    import PyQt5.QtCore as qCore
    import PyQt5.QtGui as qGui
    
except ImportError:
    print("PyQt5 not found. Using pip to install")
    subprocess.check_call([sys.executable,"-m","pip","install","PyQt5"])
    #from PyQt5.QtWidgets import QApplication, QMainWindow

try:
    from PIL import Image, ImageCms
except ImportError:
    print("PIL not found. Using pip to install")
    subprocess.check_call([sys,executable,"-m","pip","install","PIL"])

class MainWindow(qt.QWidget):
    def __init__(self,kern,app):
        
        super().__init__()
        self.kern = kern
        self.Controller = controller.Controller(self.kern)
        self.setWindowTitle("Wiki OS")
        #screen = screeninfo.get_monitors()[0]
        screen = app.primaryScreen().size()
        height = (int)(screen.height()*0.70)
        width = (int)(screen.width()*0.60)
        self.setFixedSize(width,height)  # (x, y, width, height)
        self.dock_frame = None


        self.layout = qt.QVBoxLayout()
        self.unlocked = False
        self.searchBar = None
        
        self.connectors = None

        self.usersScreen()

    def usersScreen(self):

        self.clearLayout(self.layout)

        users = self.kern.get_users()
        for user in users:
            print("User: ",user)
            button = qt.QPushButton(user)
            button.setFixedSize(50,50)
            button.clicked.connect(lambda checked=False,e=user: self.loginScreen(e))
            self.layout.addWidget(button)
        self.setLayout(self.layout)

    def loginScreen(self,username):

        self.clearLayout(self.layout)
        self.username = qt.QLabel(str(username))

        # Back button to choose different account
        backBut = qt.QPushButton("<")
        backBut.setFixedSize(30,30)
        backBut.clicked.connect(self.usersScreen)

        #button = qt.QPushButton(">")
        #button.setFixedSize(30,30)
        #button.setObjectName("circularButton")
        #button.clicked.connect(self.validateLogin)
        self.password  = qt.QLineEdit()
        self.password.setEchoMode(qt.QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("Password")
        self.password.setFixedSize(400,30)
        self.password.returnPressed.connect(self.validateLogin)
        
        # Password Layout
        pass_layout = qt.QHBoxLayout()
        pass_layout.addWidget(backBut)
        pass_layout.addWidget(self.password)
        #pass_layout.addWidget(button)

        password_widget = qt.QWidget()
        password_widget.setLayout(pass_layout)
        

        # Reboot options layout

        #Final Layout
        self.layout.addWidget(self.username)
        self.layout.addWidget(password_widget)
        #self.layout.addWidget(self.button,pass_layout)
        #self.layout.addWidget(button)
        self.setLayout(self.layout)

    def validateLogin(self):
        passWord = self.password.text()
        userName = self.username.text()
        print("The passWord: ",passWord)
        print("The userName: ",userName)
        try:
            self.kern.login(userName,passWord)
            self.homeScreen()
        except Exception as e:
            print("Error. Issues logging in.",e)
            print(traceback.format_exc())
            self.password.setObjectName("Error")
            self.password.setStyleSheet("border: 3px solid red;")
            self.password.update()
            print("qss applied:",self.password.styleSheet())

    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def homeScreen(self):
        
        self.clearLayout(self.layout)
        self.mainTab = qt.QTabWidget()
        self.setStyle(self.kern.get_current_user())
        self.unlocked = True
        #self.mainTab = qt.QTabWidget()
        #self.mainTab.setTabsClosable(True)
        self.mainTab.tabCloseRequested.connect(self.close_tab)
        self.plus_tab_index = -1
        self.mainTab.currentChanged.connect(self.handle_tab_change)
        #self.add_tab_button = qt.QPushButton("Add new tab")
        #self.add_tab_button.clicked.connect(self.add_new_tab)
        
        # Dealing with query tab
        self.queryTab = qt.QWidget()
        self.mainTabIndex = self.mainTab.addTab(self.queryTab,"Q")
        self.mainTab.setTabEnabled(self.mainTabIndex,True)
        
        # Search bar
        self.searchBar = qt.QLineEdit(self)
        self.searchBar.setPlaceholderText("Search..")
        self.searchBar.setVisible(True)
        self.searchBar.resize(200,30)
        self.searchBar.returnPressed.connect(lambda checked=False,e=self.searchBar.text(): self.runApp(e,searched=True))

        self.searchBar.move(
                    (self.width() - self.searchBar.width()) // 2,  # Center horizontally
                    (self.height() - self.searchBar.height()) // 2  # Center vertically
        )
        self.searchBar.keyPressEvent = self.keyPressEventSearch

        self.suggestions_list = qt.QListWidget(self)
        self.suggestions_list.setVisible(False)
        self.searchBar.textChanged.connect(self.update_suggestions)
        self.suggestions_list.itemClicked.connect(self.select_suggestion)
        self.suggestions_list.move(
                    self.searchBar.x(),
                    self.searchBar.y() + self.searchBar.height()
        )
        #self.suggestions_list.setParent
        
        # Dealing with plus tab
        self.plus_tab = qt.QWidget()
        self.plus_tab_index = self.mainTab.addTab(self.plus_tab,"+")
        # Making the marketplace tab
        self.MarketPlace(self.plus_tab)
        #self.mainTab.setTabEnabled(self.plus_tab_index,False)

        self.layout.addWidget(self.mainTab)
        #self.layout.addWidget(self.add_tab_button)
        #self.layout.addWidget(self.searchBar,alignment=qCore.Qt.AlignmentFlag.AlignCenter)
        #self.layout.addWidget(self.searchBar)
        self.buildDock()
        
        # The connectors 
        self.connectors = self.loadConnectors()
        print("The connectors: ",self.connectors)

        self.setLayout(self.layout)
       
        # To show the search Bar
        self.suggestions_list.raise_()
        self.suggestions_list.setFocus()
        self.searchBar.raise_()
        self.searchBar.setFocus()

    def setStyle(self,username):

        if username != self.kern.get_file_system().get_root():
            try:
                self.kern.get_file_system().switch_to_user_home(username)
                self.kern.get_file_system().change_directory("Modules")
                self.kern.get_file_system().change_directory("Config")
                data = self.kern.get_file_system().open_file("desktop.config")
                theme = self.kern.get_file_system().open_file("theme.config").strip().split(";")
                font = self.kern.get_file_system().open_file("font.config").strip().split(";")
                #name = theme[0].split("=")[1].strip()
                background = theme[1].split("=")[1].strip()
                foreground = theme[2].split("=")[1].strip()
                color = data.strip().split(";")[0].split("=")[1]

                fontName = font[0].split("=")[1].strip()
                fontSize = font[1].split("=")[1].strip()

                if fontName == "None":
                    fontName = "Arial"
                if fontSize == "None":
                    fontSize = "14"

                if background != "None" and color == "None":
                    self.setStyleSheet("QWidget{"+ f"color: {foreground}; background-color: {background}; font-family: {fontName}; font-size: {fontSize};"+"}"+
                        "QTabBar:tab{"+f"background: {background};border: 2px solid {foreground};"+"}"+
                        "QTabBar::tab:hover{"+f"background-color: {foreground}; color: {background};"+"}"+
                        "QPushButton:hover{"+f"background-color: {foreground}; color: {background};"+"}"+
                        "QPushButton#close{background: transparent; border: none;}"+
                        "QPushButton#close:hover{color: #bf616a;}")
                    #self.searchBar.setStyleSheet(".QTabBar{"+f"background-color: {background}; color: {foreground};"+"}")


                if color != "None":
                    path = "view/assets/nordTheme/"+color
                    self.convert_to_srgb(path)
                    if background != "None":
                        self.setStyleSheet(".QWidget{"+f"border-image: url('{path}');"+"}"+
                                           "QWidget{"+ f"color: {foreground}; background-color: {background}; font-family: {fontName}; font-size: {fontSize};"+"}"+
                        "QTabBar:tab{"+f"background: {background};border: 2px solid {foreground};"+"}"+
                        "QTabBar::tab:hover{"+f"background-color: {foreground}; color: {background};"+"}"+
                        "QPushButton:hover{"+f"background-color: {foreground}; color: {background};"+"}"+
                        "QPushButton#close{background: transparent; border: none;}"+
                        "QPushButton#close:hover{color: #bf616a;}")
                    else:
                        self.setStyleSheet(".QWidget{"+f"border-image: url('{path}');"+f"{self.stylesheet()}"+"}")
                #self.setStyleSheet("background-color: "+color+";")

                #Switching back to user home
                self.kern.get_file_system().switch_to_user_home(username)

            except Exception as e:
                print(f"Error loading style for '{username}'") 
                print(traceback.format_exc())


    def loadConnectors(self):
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        self.kern.get_file_system().change_directory("Modules")
        self.kern.get_file_system().change_directory("Connectors")
        files = self.kern.get_file_system().list_contents()["files"]
        Connectors = []
        for file in files:
            Connectors.append(file)
        # Go back to root dir
        self.kern.get_file_system().switch_to_user_home(self.kern.get_current_user())
        return Connectors



    def buildDock(self):
        # Make the window transparent to mouse events at the bottom
        #self.setMask(qGui.QRegion(0, 0, self.width(), self.height() - 50))
        self.dock_frame = qt.QFrame(self)
        self.dock_frame.setStyleSheet("border: 2px solid gray;")
        self.dock_layout = qt.QHBoxLayout(self.dock_frame)
        
        #for name in {"A","B","C"}:
        # Settings App
        settings_button = qt.QPushButton()
        settings_button.clicked.connect(lambda checked=False,e="settings": self.runApp(e))
        
        size = self.height()//28
        settings_button.setIconSize(qCore.QSize(size,size))
        settings_button.setIcon(qGui.QIcon("view/assets/Settings.png"))
        self.dock_layout.addWidget(settings_button)

        # Files App
        files_button = qt.QPushButton()
        files_button.clicked.connect(lambda checked=False,e="fileManager":self.runApp(e))
        files_button.setIconSize(qCore.QSize(size,size))
        files_button.setIcon(qGui.QIcon("view/assets/Files.png"))
        self.dock_layout.addWidget(files_button)
        # Connectors App
        connector_button = qt.QPushButton()
        connector_button.clicked.connect(lambda checked=False,e="connectors":self.runApp(e))
        connector_button.setIconSize(qCore.QSize(size,size))
        connector_button.setIcon(qGui.QIcon("view/assets/Connector.png"))
        self.dock_layout.addWidget(connector_button)

        self.layout.addWidget(self.dock_frame)
        self.dock_frame.setVisible(False)
        #self.dock_frame.move(
        #            (self.width() - self.searchBar.width()) // 2,  # Center horizontally
        #            (self.height() - self.searchBar.height()) // 2  # Center vertically
        #)
        
        self.dock_frame.raise_()
        self.dock_frame.setFocus()

        #self.installEventFilter(self)
        self.setMouseTracking(True)
        self.mainTab.setMouseTracking(True)
        self.queryTab.setMouseTracking(True)
        for widgets in qt.QApplication.allWidgets():
            widgets.setMouseTracking(True)


    def mouseMoveEvent(self,event):
    #def eventFilter(self,source,event):
        #print("EVENT FILTER")
        if event.type() == qCore.QEvent.Type.MouseMove:
        #if event.type() == qCore.QEvent.Type.HoverMove:
        #if True:
            mouse_y = event.pos().y()
            if self.height()-(self.height()//9) <= mouse_y <= self.height():
                self.dock_frame.setVisible(True)
                self.dock_frame.raise_()
                self.dock_frame.setFocus()
                self.dock_frame.setVisible(True)
                #self.searchBar.raise_()
                #self.searchBar.setFocus()
                #return True

            elif self.dock_frame:
                self.dock_frame.setVisible(False)
        super().mouseMoveEvent(event)
        #return super().eventFilter(source, event)

        #self.layout.addLayout(self.dock_layout)
        #self.layout.addWidget(self.dock_frame)
    def MarketPlace(self,widget):
        #button = qt.QPushButton("HEY")
        #widget.layout().addWidget(button)
        layout = qt.QVBoxLayout()
        
        
        label = qt.QLabel("My Apps: ")
        layout.addWidget(label)

        scroll_area = qt.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Area for the scroll
        button_container = qt.QFrame()
        button_layout = qt.QVBoxLayout(button_container)

        # Populating the current apps
        curApps = self.Controller.getCurApps()
        #curApps = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10"]
        #scroll_area.setFixedHeight(self.height()//3)
        for name in curApps:
            b = qt.QPushButton(name)
            b.clicked.connect(lambda checked=False,e=name: self.runApp(e))
            #layout.addWidget(b)
            button_layout.addWidget(b)
        


        scroll_area.setWidget(button_container)
            


        #layout.addWidget(button)
        widget.setLayout(layout)

    def runApp(self,appName,searched=False):
        if searched:
            print("Searching..")
            widget = self.Controller.runApp(self.searchBar.text())
            self.searchBar.setVisible(False)
            self.suggestions_list.setVisible(False)
            self.mainTab.raise_()
            self.mainTab.setFocus()
            if isinstance(widget,Module):
                self.add_new_tab2(widget,widget.getName())
            else:
                self.add_new_tab2(widget,self.searchBar.text())

        else:
            widget = self.Controller.runApp(appName)
            self.add_new_tab2(widget,appName)

    def add_new_tab2(self,new_tab,tabName):
        tab_count = self.mainTab.count() + 1
        indexVal = self.mainTab.insertTab(self.mainTab.count()-1,new_tab,f"{tabName}({tab_count})")
        self.plus_tab_index += 1
        self.mainTab.setCurrentIndex(indexVal)
        self.setTabClosable(indexVal,True)
    
    def setTabClosable(self,index,closable):
        tab_bar = self.mainTab.tabBar()

        if closable:
            close_button = qt.QPushButton("X")
            close_button.setFixedSize(16,16)
            close_button.clicked.connect(lambda checked=False,e=self.mainTab.tabText(index): self.removeTab(e))
            #close_button.setStyleSheet("background: transparent; border: none;")
            close_button.setObjectName("close")
            tab_bar.setTabButton(index,qt.QTabBar.ButtonPosition.RightSide, close_button)
        else:
            tab_bar.setTabButton(index,qt.QTabBar.ButtonPosition.RightSide,None)
    def removeTab(self,name):
        for index in range(self.mainTab.count()):
            if self.mainTab.tabText(index) == name:
                self.mainTab.removeTab(index)
                print(f"Tab '{name}' removed")
        print(f"Tab '{name}' not found.")


    def add_new_tab(self):
        tab_count = self.mainTab.count() +1
        new_tab = qt.QWidget()
        new_tab.setLayout(qt.QVBoxLayout())
        new_tab.layout().addWidget(qt.QPushButton(str(tab_count)))
        
        #indexVal = self.mainTab.addTab(new_tab,f"Tab {tab_count}")

        indexVal = self.mainTab.insertTab(self.mainTab.count()-1,new_tab,f"Tab {tab_count}")
        self.plus_tab_index += 1
        self.mainTab.setCurrentIndex(indexVal)



    def close_tab(self,index):
        if index != self.plus_tab_index:
            self.mainTab.removeTab(index)
            self.plus_tab_index += -1
            self.mainTab.setCurrentIndex(self.plus_tab_index-1)
    
    def handle_tab_change(self,index):
        print("Not doing this yet")
        #if index == self.plus_tab_index:
        #    self.add_new_tab()
    
    def keyPressEvent(self,event):
        if self.unlocked and event.key() == qCore.Qt.Key.Key_Q and event.modifiers() in (qCore.Qt.KeyboardModifier.ControlModifier,qCore.Qt.KeyboardModifier.AltModifier):
            if not self.searchBar.isVisible():
                self.searchBar.setVisible(True)
                self.searchBar.move(
                    (self.width() - self.searchBar.width()) // 2,  # Center horizontally
                    (self.height() - self.searchBar.height()) // 2  # Center vertically
                )
                self.suggestions_list.move(
                    self.searchBar.x(),
                    self.searchBar.y()+self.searchBar.height()
                )
                self.suggestions_list.raise_()
                self.suggestions_list.setFocus()
                self.searchBar.raise_()
                self.searchBar.setFocus()
        else:
            super().keyPressEvent(event)

    def keyPressEventSearch(self,event):
        curRow = self.suggestions_list.currentRow()
        if event.key() == qCore.Qt.Key_Down:
            if curRow < self.suggestions_list.count()-1:
                self.suggestions_list.setCurrentRow(curRow+1)
        elif event.key() == qCore.Qt.Key_Up:
            if curRow > 0:
                self.suggestions_list.setCurrentRow(curRow-1)
        elif (event.key() in (qCore.Qt.Key_Return,qCore.Qt.Key_Enter)):
            current_item = self.suggestions_list.currentItem()
            if current_item is not None and len(current_item.text()) > 1:
                self.searchBar.setText(current_item.text())
            else:
                self.runApp(self.searchBar.text(),searched=True)

        else:
            qt.QLineEdit.keyPressEvent(self.searchBar,event)

    def mousePressEvent(self,event):
        #if event.button() == qCore.Qt.LeftButton:
        if self.searchBar is not None:
            self.searchBar.setVisible(False)
            self.suggestions_list.setVisible(False)
            self.mainTab.raise_()
            self.mainTab.setFocus()

    def select_suggestion(self,item):
        self.searchBar.setText(item.text())
        self.suggestions_list.setVisible(False)

    def update_suggestions(self,text):
        x = self.Controller.getCurApps()
        # The connectors 
        self.connectors = self.loadConnectors()
        if text:
            filtered_suggestions = [s for s in x if text.lower() in s.lower()]
            if len(self.connectors) > 0:

                for i in self.connectors:
                    t = self.getUsed(i)
                    if t=="True":
                        filtered_suggestions.append(f"Q:({text})-> {i}")
            self.suggestions_list.clear()
            for suggestion in filtered_suggestions:
                qt.QListWidgetItem(suggestion,self.suggestions_list)
            if filtered_suggestions:
                self.suggestions_list.setVisible(True)
                self.suggestions_list.resize(self.searchBar.width(), len(filtered_suggestions) * 20)
            else:
                self.suggestions_list.setVisible(False)

        else:
            self.suggestions_list.setVisible(False)

    def getUsed(self,file):
        print("For file: ",file)
        x = self.Controller.getConnectorData(file)
        #print(x)
        return x.split(";")[3].split(":")[1].strip()
            
    def shake(self):
        print("AT SHAKE")

    def animate(self, parent, duration: int,easingCurve):
        animation = qCore.QPropertyAnimation(parent, b"pos")

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

class View:
    def __init__(self,kern):
        self.kern = kern
    def run(self):
        app = qt.QApplication(sys.argv)  # Create the application
        try:
            with open("view/assets/styles.qss","r") as file:
                stylesheet = file.read()
            app.setStyleSheet(stylesheet)
        except Exception as e:
            print("Error: Touble opening style file")
        try:
            window = MainWindow(self.kern,app)         # Create the main window
            window.show()                 # Show the window
            sys.exit(app.exec())          # Execute the application loop
        except Exception as e:
            print(traceback.format_exc())
#m = MainWindow()
#m.run()
#v = View()
#v.run()

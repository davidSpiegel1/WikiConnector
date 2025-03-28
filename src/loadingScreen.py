import sys
import time
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QLabel, QVBoxLayout, QWidget, QProgressBar

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.setGeometry(200, 200, 600, 400)
        label = QLabel("Welcome to the Main Application!", self)
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

        # Simulating a heavy loading process (replace with actual loading logic)
        time.sleep(5)  # Simulating a long load time

class LoadingThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(object)

    def run(self):
        # Simulating a loading process in the background
        for i in range(1, 101, 10):
            time.sleep(0.5)
            self.progress_signal.emit(i)  # Send progress updates

        # Create the main application window after loading is done
        main_app = MainApp()
        self.finished_signal.emit(main_app)

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap())  # Empty pixmap, can be replaced with an image
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 300)

        # Create a container widget for layout
        container = QWidget(self)
        container.setGeometry(0, 0, 400, 300)

        # Layout for splash screen
        layout = QVBoxLayout(container)
        self.label = QLabel("Loading, please wait...", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Progress bar
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        layout.addWidget(self.progress)

        self.show()

    def set_progress(self, value):
        self.progress.setValue(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Show splash screen
    splash = SplashScreen()

    # Create loading thread
    loading_thread = LoadingThread()
    
    # Update progress bar as loading happens
    loading_thread.progress_signal.connect(splash.set_progress)

    # Close splash and show main window when loading is done
    def show_main_app(main_app):
        splash.close()
        main_app.show()

    loading_thread.finished_signal.connect(show_main_app)

    # Start background loading
    loading_thread.start()

    sys.exit(app.exec_())


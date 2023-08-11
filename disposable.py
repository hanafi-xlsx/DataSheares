from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys
import qdarktheme

class ImageDisplayApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Welcome to DataSheares!')
        self.setWindowIcon(QIcon('images/appicon.png'))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.proceed_button = QPushButton('Select .csv file', self)
        self.proceed_button.clicked.connect(self.on_proceed)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.proceed_button)

        self.image_path = 'images/datasheares.png'  # Replace with your image path
        self.image_pixmap = QPixmap(self.image_path).scaled(700,700)
        self.image_label.setPixmap(self.image_pixmap)

    def on_proceed(self):
        self.close()

    def center_window(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 4
        self.move(x, y)

def welcome_window():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    ex = ImageDisplayApp()
    ex.center_window()
    ex.show()
    app.exec_()

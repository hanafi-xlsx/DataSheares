from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from utils import play_audio
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
        proceed_button_stylesheet =  """
                                QPushButton {
                                    background-color: darkgreen; 
                                    color: white; 
                                    font-size: 70px; 
                                    padding: 10px 10px; 
                                }

                                QPushButton:hover {
                                    background-color: #26522d;
                                    font-size: 60px;
                                    border-width: 10px;
                                    border-style: solid;
                                    border-color: #545454;                                    
                                }
                                """
                                
        self.proceed_button.setStyleSheet(proceed_button_stylesheet)
        self.proceed_button.setFixedHeight(150)  # Adjust the height as needed
        self.proceed_button.setCursor(Qt.PointingHandCursor)
        self.proceed_button.clicked.connect(self.on_proceed)
        self.media_player = QMediaPlayer()

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.proceed_button)

        self.image_path = 'images/datasheares.png'  # Replace with your image path
        self.image_pixmap = QPixmap(self.image_path).scaled(700, 700)
        self.image_label.setPixmap(self.image_pixmap)

    def on_proceed(self):
        play_audio("click")
        self.close()

    def center_window(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 8
        self.move(x, y)

def welcome_window():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    ex = ImageDisplayApp()
    ex.center_window()
    ex.setWindowIcon(QIcon("images/appicon.png"))
    ex.setFixedSize(700,850)
    ex.show()
    app.exec_()
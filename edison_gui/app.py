from PyQt5.QtWidgets import *
import sys

class MyWindow(QMainWindow):
    def __init__(self, x, y, width, height):
        super(MyWindow, self).__init__()
        self.setGeometry(x, y, width, height)
        self.setWindowTitle("DataSheares")
        self.initUI()

    def initUI(self):
        self.button1 = QPushButton(self)
        self.button1.setText("Click me")
        self.button1.clicked.connect(self.click)

        self.label = QLabel(self)
        self.label.setText("Welcome to DataSheares!")
        self.update()
        self.label.move(260, 20)

    def click(self):
        self.label.setText("You pressed the button!")
        self.update()

    def update(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = int(screen_resolution.width()), int(screen_resolution.height())
    width, height = 700, 400
    x, y = int((screen_width - width)/2), int((screen_height - height)/2)
    window = MyWindow(x,y,width,height)
    window.show()
    sys.exit(app.exec_())

window()
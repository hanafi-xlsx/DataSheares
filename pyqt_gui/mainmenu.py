from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt
import qdarktheme

class menuWindow(QMainWindow):
    def __init__(self, menu):
        super().__init__()

        self.setWindowTitle("Main Menu")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Select an Option")
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        for ele in menu:
            self.button = QPushButton(ele, self)
            self.button.setFixedWidth(200)
            self.button.clicked.connect(self.on_option_selected)
            self.layout.addWidget(self.button, alignment=Qt.AlignCenter)

    def on_option_selected(self):
        global selected_option
        selected_option = self.sender().text()
        self.close()
        return selected_option

def mainMenu(menu):
    app = QApplication([])
    qdarktheme.setup_theme()
    window = menuWindow(menu)
    window.resize(500,300)
    window.move(700, 250)
    window.show()
    app.exec_()
    print("Selected: ", selected_option)
    return selected_option
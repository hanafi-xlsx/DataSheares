import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        menu = ["View Charts", "Show Statistics", "Quit Program"]

        self.setWindowTitle("PyQt Option Box Example")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Select an Option")
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        for ele in menu:
            self.button = QPushButton(ele, self)
            self.button.setGeometry(100, 50, 100, 50)
            self.button.clicked.connect(lambda: self.on_option_selected(ele))
            self.layout.addWidget(self.button, alignment=Qt.AlignCenter)

        self.display_label = QLabel("Display Area")
        self.layout.addWidget(self.display_label)

    def on_option_selected(self, selection):
        global selected_option
        selected_option = selection
        if selected_option == "Show Statistics":
            self.close()
            return selected_option
        else:
            self.display_label.setText(f"Selected Option: {selected_option}")

def startApp():
    app = QApplication([])
    window = MyWindow()
    window.resize(500,500)
    window.move(250, 250)
    window.show()
    app.exec_()
    print("Hello", selected_option)
    return selected_option

startApp()
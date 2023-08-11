import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtWidgets import QDesktopWidget
import qdarktheme


angle = 0  # Global variable to store the rotation angle

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load the image and create a QLabel to display it
    image_path = 'datasheares.png'
    pixmap = QPixmap(image_path)

    # Resize the image to 500x500
    new_size = QSize(500, 500)
    resized_pixmap = pixmap.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    label = QLabel()
    label.setAlignment(Qt.AlignCenter)
    label.setPixmap(resized_pixmap)

    # Create a main window to contain the QLabel
    window = QWidget()
    window.setWindowTitle('Resized Image')
    window.setGeometry(100, 100, 500, 500)  # Set the window size to 500x500
    layout = QVBoxLayout()
    layout.addWidget(label)
    window.setLayout(layout)

    # Rotate the image using a QTimer
    timer = QTimer()
    
    def rotate_image():
        global angle
        rotated_pixmap = resized_pixmap.transformed(QTransform().rotate(angle))
        label.setPixmap(rotated_pixmap)
        angle += 10  # Adjust the rotation speed

    timer.timeout.connect(rotate_image)
    timer.start(50)  # Adjust the interval as needed
    screen_geometry = QDesktopWidget().screenGeometry()
    x = (screen_geometry.width() - window.width()) // 2
    y = (screen_geometry.height() - window.height()) // 3
    qdarktheme.setup_theme("light")
    window.move(x, y)
    window.show()
    sys.exit(app.exec_())

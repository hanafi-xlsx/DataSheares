from time import sleep
from utils import play_audio
import sys

def quit_program():
    play_audio("click")
    print("Quitting program...")
    sleep(1)
    print("Thanks for using DataSheares!")
    data_shearing()
    sleep(1.5)
    sys.exit()

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QPixmap, QTransform
import sys
import random

items = []

class MovingItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setFlag(QGraphicsPixmapItem.ItemIsMovable)

    def collides_with(self, item):
        return self.collidesWithItem(item, Qt.IntersectsItemBoundingRect)

class ImageMovingApp(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.setWindowTitle("DataShearing")
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.man = MovingItem(QPixmap("images/sheares.png").scaled(200, 200))
        self.sheep = MovingItem(QPixmap("images/sheep.png").scaled(160, 160))
        self.wool_items = []
        self.white_wool = None
        self.scene.addItem(self.man)
        self.scene.addItem(self.sheep)
        items.append(self.man)
        items.append(self.sheep)

        self.man.setPos(100, 100)
        self.sheep.setPos(300, 300)

        self.movement_data = {}  # Store movement data for each item
        self.sheares_wooled = False
        self.sheares_sheared = False
        self.sheep_sheared = False  # Flag to track sheep shearing
        self.sheares_wooled_timer = QTime()
        self.sheep_sheared_timer = QTime()

        for item in items:
            # Set initial direction_x to -1 to make them move towards the left
            self.movement_data[item] = {
                'direction_x': -1,
                'direction_y': random.choice([1, -1]),
                'speed': random.randint(4, 8)
            }

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_positions)
        self.timer.start(30)  # Update every 30 ms

    def update_positions(self):
        for item in items:
            movement = self.movement_data[item]
            item.moveBy(movement['direction_x'] * movement['speed'], movement['direction_y'] * movement['speed'])
            x, y = item.scenePos().x(), item.scenePos().y()

            if x < 0 or x > self.width() - item.boundingRect().width():
                movement['direction_x'] *= -1

                # Flip the image horizontally
                item.setPixmap(item.pixmap().transformed(QTransform().scale(-1, 1)))

            if y < 0 or y > self.height() - item.boundingRect().height():
                movement['direction_y'] *= -1

        self.check_collisions()

    def check_collisions(self):
        if not self.sheep_sheared and self.man.collides_with(self.sheep):
            play_audio("shear")
            x, y = self.sheep.pos().x(), self.sheep.pos().y()
            self.spawn_wool(x, y)
            self.sheares_sheared = True
            self.sheep_sheared = True
            self.sheep_sheared_timer.start()
            self.man.setPixmap(QPixmap("images/sheares_empty.png").scaled(250, 250))
            self.sheep.setPixmap(QPixmap("images/sheared_sheep.png").scaled(160, 160))

        if self.sheep_sheared and self.sheep_sheared_timer.elapsed() >= 3000:
            play_audio("sheep")
            self.sheep.setPixmap(QPixmap("images/sheep.png").scaled(160, 160))
            self.man.setPixmap(QPixmap("images/sheares.png").scaled(200, 200))
            self.sheares_sheared = False
            self.sheep_sheared = False

        if not self.sheares_sheared and not self.sheares_wooled:
            collided_wool = None
            for wool_item in self.wool_items:
                if self.man.collides_with(wool_item):
                    collided_wool = wool_item 
                    break
            if collided_wool:
                self.count+=1
                self.setWindowTitle("DataShearing ("+str(self.count)+")")
                play_audio("pop")
                self.wool_items.remove(collided_wool)
                self.scene.removeItem(collided_wool)
                del collided_wool

    def spawn_wool(self, x, y):
        random_number = random.randint(1, 3)
        for i in range(random_number):
            play_audio("pop")
            self.white_wool = MovingItem(QPixmap("images/white_wool.png").scaled(80, 80))
            self.scene.addItem(self.white_wool)
            items.append(self.white_wool)
            self.wool_items.append(self.white_wool)
            self.white_wool.setPos(x, y)
            self.movement_data[self.white_wool] = {
                'direction_x': random.choice([1, -1]),
                'direction_y': random.choice([1, -1]),
                'speed': random.randint(4, 8)
            }

def data_shearing():
    app = QApplication(sys.argv)
    window = ImageMovingApp()
    window.show()
    window.setFixedSize(800, 700)
    app.exec_()

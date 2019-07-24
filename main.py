"""Basado en ejemplo de Mr.Patiwi de 2016-1"""
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap
import sys
import time
import numpy as np
from enemy import Skeleton
from player import Player
from events import MovePlayerEvent


class MainWindow(QMainWindow):
    movePlayerTrigger = pyqtSignal(MovePlayerEvent)

    def __init__(self):
        super().__init__()
        self.enemies = [Skeleton(self, 130, 40)]
        self.player = Player(self, 180, 40)

        self.setGeometry(500, 500, 400, 300)
        self.show()

        # conecto el trigger de mover jugador al controlador del jugador
        self.movePlayerTrigger.connect(self.player.controller.move)

    @staticmethod
    def actualizar_imagen(myImageEvent):
        label = myImageEvent.image
        label.move(myImageEvent.x, myImageEvent.y)

    def comprobar_choque(self, chocarEvent):
        for enemy in self.enemies:
            if enemy.collideBox.intersect(chocarEvent.mono):
                chocarEvent.mono.damage(enemy)
                enemy.atacar(chocarEvent.mono)

    def enemyOrientation(self, getOrientationEvent):
        dx = self.player.position[0] - getOrientationEvent.enemy.position[0]
        dy = self.player.position[1] - getOrientationEvent.enemy.position[1]
        orientation = np.arctan2(dx, dy)
        getOrientationEvent.enemy.orientation = orientation

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Right:
            self.movePlayerTrigger.emit(MovePlayerEvent('right'))
        if event.key() == Qt.Key_Up:
            self.movePlayerTrigger.emit(MovePlayerEvent('up'))
        if event.key() == Qt.Key_Left:
            self.movePlayerTrigger.emit(MovePlayerEvent('left'))
        if event.key() == Qt.Key_Down:
            self.movePlayerTrigger.emit(MovePlayerEvent('down'))

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.movePlayerTrigger.emit(MovePlayerEvent('stop_right'))
        if event.key() == Qt.Key_Up:
            self.movePlayerTrigger.emit(MovePlayerEvent('stop_up'))
        if event.key() == Qt.Key_Left:
            self.movePlayerTrigger.emit(MovePlayerEvent('stop_left'))
        if event.key() == Qt.Key_Down:
            self.movePlayerTrigger.emit(MovePlayerEvent('stop_down'))

    def run(self):
        for enemy in self.enemies:
            enemy.start()
        self.player.start()
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication([])
    ex = MainWindow()
    ex.run()

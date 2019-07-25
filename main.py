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
from PyQt5 import uic

ventanaInicio = uic.loadUiType("ventana_inicio.ui")
ventanaJuego = uic.loadUiType("ventana_juego.ui")


class MainWindow(ventanaInicio[0], ventanaInicio[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.botonJugar.clicked.connect(self.jugar)
        self.botonSalir.clicked.connect(self.salir)
        self.ventanaJuego = GameWindow(self)
        self.show()

    def jugar(self):
        self.ventanaJuego.run()
        self.close()

    def salir(self):
        self.close()


class GameWindow(ventanaJuego[0], ventanaJuego[1]):
    movePlayerTrigger = pyqtSignal(MovePlayerEvent)

    def __init__(self, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.enemies = [Skeleton(self, 130, 40)]
        self.player = Player(self, 240, 40)
        self.barraSalud.setValue(100)
        # conecto el trigger de mover jugador al controlador del jugador
        self.movePlayerTrigger.connect(self.player.controller.move)
        self.mainWindow = mainWindow

    @staticmethod
    def actualizar_imagen(myImageEvent):
        label = myImageEvent.image
        label.move(myImageEvent.x, myImageEvent.y)

    def comprobar_choque(self, chocarEvent):
        for enemy in self.enemies:
            if enemy.collideBox.intersect(chocarEvent.mono):
                chocarEvent.mono.damage(enemy)
                enemy.atacar(chocarEvent.mono)
                self.barraSalud.setValue(chocarEvent.mono.salud)

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

    def gameOver(self):
        for enemy in self.enemies:
            enemy.terminate()
        self.player.terminate()
        self.mainWindow.show()
        self.close()

    def run(self):
        self.barraSalud.setValue(100)
        self.show()
        for enemy in self.enemies:
            enemy.start()
        self.player.start()


if __name__ == '__main__':
    app = QApplication([])
    main = MainWindow()
    sys.exit(app.exec_())

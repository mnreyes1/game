"""Basado en ejemplo de Mr.Patiwi de 2016-1"""
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap
import sys
import time
import numpy as np
from events import MoveImageEvent, getOrientationEvent


class Skeleton(QThread):
    triggerImage = pyqtSignal(MoveImageEvent)
    triggerGetOrientation = pyqtSignal(getOrientationEvent)

    def __init__(self, parent, x, y):
        super().__init__()

        self.width = 32
        self.height = 32

        # Se crea el label en el cual se pondra la imagen
        self.image = QLabel(parent)
        # Se ajusta la geometria (xpos, ypos, width, height)
        self.image.setGeometry(0, 0, 32, 32)
        # Se le setea la imagen 0
        self.image.setPixmap(QPixmap("Assets/skeleton/0"))
        self.image.show()
        self.image.setVisible(True)

        # Conectamos el triggerImage a la funcion de la ventana principal de actualizar imagen
        self.triggerImage.connect(parent.actualizar_imagen)
        self.triggerGetOrientation.connect(parent.enemyOrientation)

        self.collideBox = CollideBox(self, x, y)
        self.__position = (0, 0)
        self.position = (x, y)  # este es una property
        self.attack = 55
        self.orientation = 0
        self.speed = 0.5

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        # muevo la caja de colisiones
        self.collideBox.move(value)
        # El triggerImage emite su señal a la ventana principal cuando cambiamos la posición
        self.triggerImage.emit(MoveImageEvent(
            self.image, self.position[0], self.position[1]
        ))

    def atacar(self, player):
        # define cuanto empuja el player hacia atras en el eje x
        dx = (player.position[0] - self.position[0])//2
        # define cuanto empuja el player hacia atras en el eje y
        dy = (player.position[1] - self.position[1])//2
        # mueve al personaje hacia atras
        self.position = (self.position[0] - dx, self.position[1] - dy)

    def run(self):
        while True:
            time.sleep(0.04)

            self.triggerGetOrientation.emit(getOrientationEvent(self))

            # si llega al borde de abajo lo tira para arriba
            if self.position[1] <= 300:
                self.position = (self.position[0], self.position[1])
            else:
                self.position = (self.position[0], 0)

            self.position = (self.position[0]+self.speed*np.sin(
                self.orientation), self.position[1]+self.speed*np.cos(self.orientation))


class CollideBox:
    def __init__(self, parent, x, y):
        self.position = (x, y)
        self.width = parent.width
        self.height = parent.height

    def move(self, newpos):
        self.position = newpos

    # funcion que detecta colisiones
    def intersect(self, otherBox):
        if abs(otherBox.position[0]-self.position[0]) < self.width and abs(otherBox.position[1]-self.position[1]) < self.height:
            return True

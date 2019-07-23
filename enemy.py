"""Basado en ejemplo de Mr.Patiwi de 2016-1"""
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap
import sys
import time
from events import MoveImageEvent


class Skeleton(QThread):
    trigger = pyqtSignal(MoveImageEvent)
    # pyqtSignal recibe *args que le indican
    # cuales son los tipos de argumentos que seran enviados
    # en este caso, solo se enviara un argumento:
    #   objeto clase MoveImageEv

    def __init__(self, parent, x, y):
        """
        Un Player es un QThread que movera una imagen
        en una ventana. El __init__ recibe los parametros:
            parent: ventana
            x e y: posicion inicial en la ventana

        """
        super().__init__()
        # Timer para la animacion del player
        self.animationTimer = QTimer()  # no esta hecha la animacion

        self.parent = parent

        self.width = 32
        self.height = 32

        # Se crea el label en el cual se pondra la imagen
        self.image = QLabel(parent)
        # Se ajusta la geometria (xpos, ypos, width, height)
        self.image.setGeometry(0, 0, 32, 32)
        # Se le setea la imagen 0
        self.image.setPixmap(QPixmap("Assets/skeleton/0"))
        # Se muestra la imagen
        self.image.show()
        # Se hace visible
        self.image.setVisible(True)

        # Conectamos el trigger a la funcion de la ventana principal de actualizar imagen
        self.trigger.connect(parent.actualizar_imagen)

        self.collideBox = CollideBox(self, x, y)

        # se setea la posicion inicial
        self.__position = (0, 0)
        self.position = (x, y)  # este es una property

    @property
    def position(self):
        # property de posicion
        return self.__position

    @position.setter
    def position(self, value):
        # lo que se hace cuando se modifica la property
        self.__position = value
        self.collideBox.move(value)
        # El trigger emite su señal a la ventana principal cuando cambiamos la posición
        self.trigger.emit(MoveImageEvent(
            self.image, self.position[0], self.position[1]
        ))

    def run(self):
        while True:
            # mueve la imagen constantemente cada 0.05
            time.sleep(0.05)
            # si llega al borde de abajo lo tira para arriba
            if self.position[1] <= 300:
                self.position = (self.position[0], self.position[1])
            else:
                self.position = (self.position[0], 0)


class CollideBox:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.position = (x, y)
        self.width = parent.width
        self.height = parent.height

    def move(self, newpos):
        self.position = newpos

    def intersect(self, otherBox):
        if abs(otherBox.position[0]-self.position[0]) < self.width and abs(otherBox.position[1]-self.position[1]) < self.height:
            return True

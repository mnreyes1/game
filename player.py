"""Basado en ejemplo de Mr.Patiwi de 2016-1"""
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap
import sys
import time
from events import MoveImageEvent, ChocarEnemigoEvent
import random


class Player(QThread):
    # triggers para mover imagen y comprobar choque
    moveImageTrigger = pyqtSignal(MoveImageEvent)
    chocarEnemigoTrigger = pyqtSignal(ChocarEnemigoEvent)
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
        timer = QTimer(self)
        # lo conecto al update_frame
        timer.timeout.connect(self.update_frame)
        # inicio timer
        timer.start(100)

        # alto y ancho
        self.width = 32
        self.height = 32

        # creo el controlador de movimientos
        self.controller = Controller(self)

        # Se crea el label en el cual se pondra la imagen y su path
        self.imagePath = "Assets/witch_right/0"
        self.image = QLabel(parent)
        # Se ajusta la geometria (xpos, ypos, width, height)
        self.image.setGeometry(0, 0, self.width, self.height)
        # Se le setea la imagen 0
        self.image.setPixmap(QPixmap(self.imagePath))
        # Se muestra la imagen
        self.image.show()
        # Se hace visible
        self.image.setVisible(True)

        # Conectamos el moveImageTrigger a la funcion de la ventana principal de actualizar imagen
        self.moveImageTrigger.connect(parent.actualizar_imagen)
        self.chocarEnemigoTrigger.connect(parent.comprobar_choque)

        self.collideBox = CollideBox(self, x, y)

        # se setea la posicion inicial
        self.__position = (0, 0)
        self.position = (x, y)  # este es una property

        # para saber la orientacion del personaje
        self.__direction = "right"
        # para mover al personaje
        self.velocity = [0, 0]

        # salud
        self.__salud = 100

    @property
    def position(self):
        # property de posicion
        return self.__position

    @position.setter
    def position(self, value):
        # lo que se hace cuando se modifica la property
        self.__position = value
        # movemos la caja que detecta colisiones
        self.collideBox.move(value)
        # El moveImageTrigger emite su señal a la ventana principal cuando cambiamos la posición
        self.moveImageTrigger.emit(MoveImageEvent(
            self.image, self.position[0], self.position[1]
        ))

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        # si el path tiene la palabra right o left la cambia por el value
        self.imagePath = self.imagePath.replace("right", value)
        self.imagePath = self.imagePath.replace("left", value)

    @property
    def salud(self):
        return self.__salud

    @salud.setter
    def salud(self, value):
        if value < 0:
            self.__salud = 0
            self.die()
        else:
            self.__salud = value

    def die(self):
        # funcion para saber que pasa cuando muere el player
        pass

    def update_frame(self):
        # obtengo el numero de la imagen
        number = int(self.imagePath[-1])
        # Quito la ultima letra del path
        self.imagePath = self.imagePath[:len(self.imagePath) - 1]
        # como los numeros de las imagenes llegan a 3...
        if number < 3:
            number += 1
        else:
            number = 0
        # Agrego la ultima letra del path
        self.imagePath = self.imagePath + str(number)
        # actualizo la imagen
        self.image.setPixmap(QPixmap(self.imagePath))
        # El moveImageTrigger emite su señal a la ventana principal cuando cambiamos la imagen
        self.moveImageTrigger.emit(MoveImageEvent(
            self.image, self.position[0], self.position[1]))

    def damage(self, enemy):
        # funcion que hace daño al jugador
        self.salud -= enemy.attack
        print(self.salud)
        # define cuanto empuja el enemigo hacia atras en el eje x
        dx = enemy.position[0] - self.position[0]
        # define cuanto empuja el enemigo hacia atras en el eje y
        dy = enemy.position[1] - self.position[1]
        # mueve al personaje hacia atras
        self.position = (self.position[0] - dx, self.position[1] - dy)

    def run(self):
        while True:
            # mueve la imagen constantemente cada 0.02
            time.sleep(0.02)
            # cambia la posicion de acuerdo a la velocidad
            self.position = (
                self.position[0]+self.velocity[0], self.position[1]+self.velocity[1])

            # emito señal para ver si choco enemigo
            self.chocarEnemigoTrigger.emit(ChocarEnemigoEvent(self))


class Controller:
    # controla los botones presionados
    def __init__(self, parent):
        # parent es Player
        self.parent = parent

    # funcion para mover al jugador
    def move(self, movePlayerEvent):
        # setea velocidad 2 a la derecha y orientacion a la derecha
        if movePlayerEvent.direction == "right":
            self.parent.direction = "right"
            self.parent.velocity[0] = 2
        # si no se mueve a la izquierda setea velocidad a 0
        if movePlayerEvent.direction == "stop_right":
            if self.parent.velocity[0] != -2:
                self.parent.velocity[0] = 0
        if movePlayerEvent.direction == "up":
            self.parent.velocity[1] = -2
        if movePlayerEvent.direction == "stop_up":
            if self.parent.velocity[1] != 2:
                self.parent.velocity[1] = 0
        if movePlayerEvent.direction == "left":
            self.parent.direction = "left"
            self.parent.velocity[0] = -2
        if movePlayerEvent.direction == "stop_left":
            if self.parent.velocity[0] != 2:
                self.parent.velocity[0] = 0
        if movePlayerEvent.direction == "down":
            self.parent.velocity[1] = 2
        if movePlayerEvent.direction == "stop_down":
            if self.parent.velocity[1] != -2:
                self.parent.velocity[1] = 0


class CollideBox:
    # caja que detecta colisiones
    def __init__(self, parent, x, y):
        self.parent = parent
        self.position = (x, y)
        self.width = parent.width
        self.height = parent.height

    # funcion para mover la caja
    def move(self, newpos):
        self.position = newpos

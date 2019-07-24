"""Basado en ejemplo de Mr.Patiwi de 2016-1"""
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap
import sys
import time
from enemy import Skeleton
from player import Player
from events import MovePlayerEvent


class MainWindow(QMainWindow):
    # ventana del juego principal
    # trigger que emite señales para mover al jugador
    movePlayerTrigger = pyqtSignal(MovePlayerEvent)

    def __init__(self):
        super().__init__()
        # esqueleto enemigo
        self.enemy = Skeleton(self, 130, 40)
        # jugador
        self.player = Player(self, 180, 40)

        # seteo el titulo y otras propiedades de la ventana
        self.titulo = QLabel(self)
        self.titulo.setText("Ejemplo")
        self.titulo.move(160, 10)
        self.titulo.show()
        self.setGeometry(500, 500, 400, 300)
        self.show()

        # conecto el trigger de mover jugador al contorlador del jugador
        self.movePlayerTrigger.connect(self.player.controller.move)

    @staticmethod
    def actualizar_imagen(myImageEvent):
        # metodo estatico que actualiza una imagen
        label = myImageEvent.image
        label.move(myImageEvent.x, myImageEvent.y)

    def keyPressEvent(self, event):
        # cuando se apreta una tecla entro aca
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
        # cuando se suelta una tecla entro aca
        if event.key() == Qt.Key_Right:
            self.movePlayerTrigger.emit(MovePlayerEvent('stop_right'))
        if event.key() == Qt.Key_Up:
            self.movePlayerTrigger.emit(MovePlayerEvent('stop_up'))
        if event.key() == Qt.Key_Left:
            self.movePlayerTrigger.emit(MovePlayerEvent('stop_left'))
        if event.key() == Qt.Key_Down:
            self.movePlayerTrigger.emit(MovePlayerEvent('stop_down'))

    def run(self):
        # inicio el thread de los enemigos
        self.enemy.start()
        # inicio el thread del jugador
        self.player.start()
        # mato todo
        sys.exit(app.exec_())


if __name__ == '__main__':
    # creo la app
    app = QApplication([])
    # inicio el thrad de la ventana de juego
    ex = MainWindow()
    ex.run()

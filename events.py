class MoveImageEvent:
    """
    Las instancias de esta clase
    contienen la informacion necesaria
    para que la ventana actualice
    la posicion de la imagen
    """

    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y


class MovePlayerEvent:
    # clase para emitir señal de mover la jugador
    def __init__(self, direction):
        self.direction = direction


class ChocarEnemigoEvent:
    # clase para emitir señal y comprobar si estoy chocando y que hacer
    def __init__(self, mono):
        self.mono = mono

class MoveImageEvent:
    # clase para emitir señal de mover imagenes
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y


class MovePlayerEvent:
    # clase para emitir señal de mover la jugador
    def __init__(self, direction):
        self.direction = direction


class ChocarEnemigoEvent:
    # clase para emitir señal y comprobar si estoy chocando
    def __init__(self, mono):
        self.mono = mono


class getOrientationEvent:
    # clase para orientar a los enemigos
    def __init__(self, enemy):
        self.enemy = enemy

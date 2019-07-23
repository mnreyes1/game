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
    def __init__(self, direction):
        self.direction = direction

from GUI import bloque


class Tanque:
    # cada Tanque, al crearse se le asociará un objeto Cuadrado (el cual lo representará en el mapa)
    def __init__(self, pantalla, ancho, alto, color):
        self.x = None
        self.y = None
        self.bloque = bloque.Bloque(pantalla, ancho, alto, color, self.x, self.y)
        self.color = color

    # funcion que definirá las posiciones x e y del tanque
    def posicionar(self, x, y):
        self.x = x
        self.y = y

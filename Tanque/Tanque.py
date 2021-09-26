from GUI.bloque import Bloque


class Tanque:
    # cada Tanque, al crearse se le asociará un objeto Cuadrado (el cual lo representará en el mapa)
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.x = None
        self.y = None
        self.bloque = None
        self.color = None

    # funcion que definirá las posiciones x e y del tanque y construirá su bloque
    def construirBloques(self, x, y,color):
        self.x = x
        self.y = y
        self.color=color
        self.bloque = Bloque(self.pantalla, 40, 40, self.color, self.x, self.y)

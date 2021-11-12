from Mapa.bloque import Bloque


class Tanque:
    # cada Tanque, al crearse se le asociará un objeto Cuadrado (el cual lo representará en el mapa)
    def __init__(self, pantalla, imagen):
        self.pantalla = pantalla
        self.x = None
        self.y = None
        self.bloque = None
        self.imagen = imagen
        self.velocidad = 100
        self.angulo = 100
        self.vida = 100
        self.proyectilActual = None
        self.listaProyectiles = []

    # funcion que definirá las posiciones x e y del tanque y construirá su bloque
    def construirBloques(self, x, y):
        self.x = x
        self.y = y
        self.bloque = Bloque(self.pantalla, 40, 40, self.imagen, self.x, self.y)

    def restablecerVelAng(self):
        self.velocidad = 100
        self.angulo = 100

    def cambiarArma(self, numArma):
        self.proyectilActual = self.listaProyectiles[numArma]

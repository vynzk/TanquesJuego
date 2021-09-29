from GUI.bloque import Bloque


class Tanque:
    # cada Tanque, al crearse se le asociará un objeto Cuadrado (el cual lo representará en el mapa)
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.x = None
        self.y = None
        self.bloque = None
        self.color = None
        self.velocidad = 100
        self.angulo = 100
        self.vida = 100
        self.proyectilActual = None
        self.listaProyectiles = []

    # funcion que definirá las posiciones x e y del tanque y construirá su bloque
    def construirBloques(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.bloque = Bloque(self.pantalla, 40, 40, self.color, self.x, self.y)

    def restablecerVelAng(self):
        self.velocidad = 100
        self.angulo = 100

    def cambiarProyectil(self):
        print("###### MOCHILA DE ARMAS ####")
        for proyectil in self.listaProyectiles:
            print(
                f'Arma: {proyectil.__class__.name}; balas restantes: {proyectil.stock} ; daño: {proyectil.daño}')  # debug
            decision = int("Ingresa 1 si deseas cambiar, en caso contrario ingresa cualquier otro número: ")
            if decision == 1:
                print(f'Tu arma {self.proyectilActual} se cambiará por {proyectil.__class__.name}')  # debug
                self.proyectilActual = proyectil
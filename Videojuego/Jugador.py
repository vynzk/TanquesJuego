class Jugador:
    def __init__(self, nombre, tanque):
        self.nombre = nombre
        self.tanque = tanque
        self.victorias = 0

    def sumarVictoria(self):
        self.victorias += 1
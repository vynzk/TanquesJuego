class Jugador():
    def __init__(self, nombre, tanque):
        self.nombre = nombre
        self.tanque = tanque
        self.victorias = 0

    def sumarVictoria(self):
        self.victorias += 1

    def mostrarInformacion(self):
        print("Nombre: ", self.nombre, " ; victorias ", self.victorias)

    def getNombre(self):
        return self.nombre

    def getVictorias(self):
        return self.victorias

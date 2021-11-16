class Jugador:
    def __init__(self, nombre, tanque, esIA):
        self.nombre = nombre
        self.tanque = tanque
        self.victorias = 0
        self.participoTurno = False
        self.oponentesDestruidos = 0
        self.esIA = esIA # Requisito 4: es un boleano al que accederemos más tarde

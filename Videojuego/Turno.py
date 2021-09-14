class Turno:
    def __init__(self,partida):
        self.jugador=None
        self.partida=None

    def permitirDisparar(self):
        # si el disparo del jugador colisiona con un jugador:
        if(self.partida.efectuarDisparo(self.jugador.tanque)):
            pass
        # no colisiona con un tanque.
        else:
            pass


    # se va pasando de turno
    def asignarTurno(self,partida,jugador):
        self.partida=partida
        self.jugador=jugador

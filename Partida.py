class Partida():
    def __init__(self,listasJugadores):
        self.jugadoresActivos=listasJugadores

    def mostrarInformacion(self):
        print("### INFORMACION PARTIDA ###")
        print("estado partida: "+str(self.estadoPartida))
        print("jugadores activos: "+str(self.jugadoresActivos))
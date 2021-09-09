class Partida():
    def __init__(self, id, escenaJuego):
        self.id = id
        self.estado = False
        self.jugadorGanador = None
        self.jugadoresActivos = []
        self.escena=escenaJuego

    # funcion que agrega jugadores a su lista de jugadores activos
    def agregarJugadores(self, jugador):
        self.jugadoresActivos.append(jugador)

    # función debug, muestra los nombres y objetos de los jugadores activos
    def mostrarJugadoresActivos(self):
        listaNombresActivos = []
        for jugador in self.jugadoresActivos:
            listaNombresActivos.append(jugador.nombre)

        print(" JUGADORES ACTIVOS")
        print("     Nombres: " + str(listaNombresActivos))
        print("     Objetos: " + str(self.jugadoresActivos))

    # funcion debug, que muestra toda la información de la partida
    def mostrarInformacion(self):
        print("\nPartida " + str(self.id))
        self.mostrarJugadoresActivos()
        print(" Estado: " + str(self.estado))
        print(" Objeto escena: "+str(self.escena))
        print(" Ganador: " + str(self.jugadorGanador))

    # funcion que termina la partida cuando queda sólo un jugador activo dentro de ella
    def terminarPartida(self):
        self.estado = True
        self.jugadorGanador = self.jugadoresActivos[0]
        self.jugadorGanador.sumarVictoria()
        print("\n!!!! El/la jugador/a ", self.jugadorGanador.getNombre(), " ganó la partida !!!!")

    # funcion que brinda la posibilidad de eliminar jugadores al jugadorAtacante 
    def eliminarJugador(self, jugadorAtacante):
        print("\nELIMINAR JUGADOR [Debug]")
        self.mostrarJugadoresActivos()
        opcionEliminar = int(input("  Ingrese la posicion del jugador que desea eliminar: "))
        try:
            jugadorEliminado = self.jugadoresActivos[opcionEliminar]
            self.jugadoresActivos.pop(opcionEliminar)  # << lo eliminamos
            print("\n>>ACCION: Jugador/a ", jugadorEliminado.getNombre(), " ha sido eliminado por ",
            jugadorAtacante.getNombre())
        except:
            print(" ERROR: fuera de rango")

    def getId(self):
        return self.id

    def getGanador(self):
        return self.jugadorGanador

    # función que retorna el objeto escena en concreto de esa partida, la cual se modifican al disparar
    # eliminar tanques, etc (visualmente)
    def getEscena(self):
        return self.escena 
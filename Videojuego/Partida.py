# en el momento que sólo queda un jugador activo en la partida, se invoca el metodo terminar y pasa a la otra partida
# partida debe ir eliminando a los jugadoras activos cuyo tanque es alcanzado
# partida debe llamar la función "pasarTurno" del jugadorActual (otrogrado por el TurnoActual) al momento de que un proyectil colisione (con un tanque o con el piso)

class Partida:
    def __init__(self, id, pantalla):
        self.id = id
        self.estado = False
        self.pantalla = pantalla  # pantalla que le pasa el director)
        self.jugadorGanador = None
        self.jugadoresActivos = []
        self.contadorJugador = 0

    # funcion que agrega jugadores a su lista de jugadores activos
    def agregarJugadores(self, jugador):
        self.jugadoresActivos.append(jugador)

    # funcion que termina la partida cuando queda sólo un jugador activo dentro de ella
    def terminar(self):
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
            # partida.PasarTurno |  aca pasariamos de turno <<<<<<<<<<<<<<<<<<<<
        except:
            print(" ERROR: fuera de rango")

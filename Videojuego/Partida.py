# en el momento que sólo queda un jugador activo en la partida, se invoca el metodo terminar y pasa a la otra partida
# partida debe ir eliminando a los jugadoras activos cuyo tanque es alcanzado
# partida debe llamar la función "pasarTurno" del jugadorActual (otrogrado por el TurnoActual) al momento de que un proyectil colisione (con un tanque o con el piso)

class Partida:
    def __init__(self, id, pantalla, mapa):
        self.id = id
        self.estado = False
        self.pantalla = pantalla  # pantalla que le pasa el director)
        self.jugadorGanador = None
        self.jugadoresActivos = []
        self.contadorJugador = 0
        self.mapa = mapa

    # funcion que agrega jugadores a su lista de jugadores activos
    def agregarJugadores(self, jugador):
        self.jugadoresActivos.append(jugador)

    # funcion que termina la partida cuando queda sólo un jugador activo dentro de ella
    def terminar(self):
        self.estado = True
        self.jugadorGanador = self.jugadoresActivos[0]
        self.jugadorGanador.victorias += 1

    # funcion que brinda la posibilidad de eliminar jugadores al jugadorAtacante 
    def eliminarJugador(self, jugadorEliminado):
        self.jugadoresActivos.remove(jugadorEliminado)

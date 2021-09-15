from Videojuego.Jugador import *
from Videojuego.Partida import *
from Tanque.Tanque import *


class Juego:
    def __init__(self, cantidadJugadores, cantidadPartidas):
        self.cantidadJugadores = cantidadJugadores
        self.listaJugadores = []
        self.cantidadPartidas = cantidadPartidas
        self.listaPartidas = []
        self.listaTanquesDisponibles = [Tanque]  # acá iran los objetos tanques disponibles para elegir inicialmente
        self.jugadorGanador = None

    def agregarJugador(self, i, pantalla):
        # colores de los tanques
        colores = [(255, 0, 0), (0, 0, 255)]
        nombre = str(input("Ingrese su nombre: "))
        posiciones = [(20, 520), (1200, 420)]
        # debe tener Tanque(self.director.pantalla, 20,20, (color), x,y)
        # >> el x,y debe ser random
        tanque = Tanque(pantalla, 20, 20, colores[i - 1], posiciones[i - 1][0], posiciones[i - 1][1])
        self.listaJugadores.append(Jugador(nombre, tanque))  # << agrega un nuevo Jugador con su nombre y su tanque

    # función que se encargará de llenar la lista de jugadores, registrará tantos jugadores
    # como lo indique la cantidad de jugadores (que debe tener el constructor de esta clase)
    def registroJugadores(self, director):
        print("\n### REGISTRO DE JUGADORES ###")
        for i in range(1, self.cantidadJugadores + 1):
            self.agregarJugador(i, director.pantalla)
        return True  # termina con exito el registro

    # función que agregará una partida a la lista de partidas, cada partida agregará como jugadores activos a la
    # totalidad de jugadores que participan en el juego
    def agregarPartida(self, i, director):
        partida = Partida(i, director)
        # va agregando los jugadores a la nueva partida
        for jugador in self.listaJugadores:
            partida.agregarJugadores(jugador)
        return partida

    # función que llenara la lista de partidas (atributo) con cada partida creada
    def registroPartidas(self, director):
        for i in range(1, self.cantidadPartidas + 1):
            self.listaPartidas.append(self.agregarPartida(i, director))
        return True  # termina con exito el registro

    def mostrarRanking(self):
        print("\n### R A N K I N G ###")
        for jugador in self.listaJugadores:
            jugador.mostrarInformacion()

    # TODO: falta definir el empate
    def definirGanador(self):
        contador = 0
        while contador < self.cantidadJugadores:
            if contador == 0:
                ganadorAux = self.listaJugadores[contador]
            else:
                jugadorActual = self.listaJugadores[contador]
                if jugadorActual.getVictorias() > ganadorAux.getVictorias():
                    ganadorAux = jugadorActual

            contador += 1
        self.jugadorGanador = ganadorAux  # << se guarda en el atributo ganador

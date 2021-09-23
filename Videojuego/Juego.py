from Videojuego.Jugador import *
from Videojuego.Partida import *
from Tanque.Tanque import *
import random


class Juego:
    def __init__(self, cantidadJugadores, cantidadPartidas):
        self.cantidadJugadores = cantidadJugadores
        self.listaJugadores = []
        self.cantidadPartidas = cantidadPartidas
        self.listaPartidas = []
        self.jugadorGanador = None
        self.juegoTerminado=False

    def agregarJugador(self, i, pantalla):
        # colores de los tanques

        # posiciones posibles del primer tanque 
        posiciones1 = [(0, 520), (20, 520), (40, 520), (60, 520), (80, 520), (100, 520), 
        (120, 500), (140, 500), (160, 480), (180, 460), (200, 440), (220, 440), (240, 440),
        (260, 440), (280, 440), (300, 460), (320, 480), (340, 520), (360, 520), (380, 520)]

        # posiciones posibles del segundo tanque
        posiciones2 = [(660, 460), (680, 440), (700, 460), (720, 480), (740, 500), (760, 560), 
        (780, 560),(800, 540), (820, 520), (840, 520), (860, 520), (880, 520), (900, 520), (920, 500),
        (940, 500), (960, 500), (980, 480), (1000, 460), (1020, 460), (1040, 440)]

        # randomizado por separado de la posicion de los tanques
        delta = random.randint(1, 20)

        if i == 1:
            posiciones = posiciones1[delta-1]
        if i == 2:
            posiciones = posiciones2[delta-1]

        colores = [(255, 0, 0), (0, 0, 255)]
        posiciones = [(20, 520), (1200, 420)]
        nombre = str(input("Ingrese su nombre: "))
        tanque = Tanque(pantalla, 20, 20, colores[i - 1], posiciones[0], posiciones[1])
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

     # TODO: falta definir el empate
    def definirGanador(self):
        contador = 0
        while contador < self.cantidadJugadores:
            if contador == 0:
                ganadorAux = self.listaJugadores[contador]
            else:
                jugadorActual = self.listaJugadores[contador]
                if jugadorActual.victorias > ganadorAux.victorias:
                    ganadorAux = jugadorActual

            contador += 1
        self.jugadorGanador = ganadorAux  # << se guarda en el atributo ganador
        self.juegoTerminado=True

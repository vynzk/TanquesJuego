from GUI.escenaJuego import EscenaJuego
from Videojuego.Jugador import *
from Videojuego.Partida import *
from Tanque.Tanque import *

class Juego():
    def __init__(self, cantidadJugadores, cantidadPartidas):
        self.cantidadJugadores = cantidadJugadores
        self.listaJugadores = []
        self.cantidadPartidas = cantidadPartidas
        self.listaPartidas = []
        self.listaTanquesDisponibles = [Tanque]  # acá iran los objetos tanques disponibles para elegir inicialmente
        self.jugadorGanador = None

    def agregarJugador(self):
        nombre = str(input("Ingrese su nombre: "))
        tanque = Tanque("Default")
        self.listaJugadores.append(Jugador(nombre, tanque))  # << agrega un nuevo Jugador con su nombre y su tanque

    # función que se encargará de llenar la lista de jugadores, registrará tantos jugadores
    # como lo indique la cantidad de jugadores (que debe tener el constructor de esta clase)
    def registroJugadores(self):
        print("\n### REGISTRO DE JUGADORES ###")
        for i in range(1, self.cantidadJugadores + 1):
            self.agregarJugador()

    # función que agregará una partida a la lista de partidas, cada partida agregará como jugadores activos a la
    # totalidad de jugadores que participan en el juego
    def agregarPartida(self, i,director):
        escenaJuego=EscenaJuego(director)
        partida = Partida(i,escenaJuego)
        # va agregando los jugadores a la nueva partida
        for jugador in self.listaJugadores:
            partida.agregarJugadores(jugador)
        return partida

    # función que llenara la lista de partidas (atributo) con cada partida creada
    def registroPartidas(self,director):
        for i in range(1, self.cantidadPartidas + 1):
            self.listaPartidas.append(self.agregarPartida(i,director))

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

    
    def getListaPartidas(self):
        return self.listaPartidas

    def getJugadorGanador(self):
        return self.jugadorGanador

    # metodo debug, para mostrar las caracteristicas de la partida
    def mostrarCaracteristicas(self):
        print("\n### CARACTERISTICAS DEL JUEGO ####")
        print("Cantidad jugadores: " + str(self.cantidadJugadores))
        print("Cantidad partidas: " + str(self.cantidadPartidas))
        print("Tanques disponibles: " + str(self.listaTanquesDisponibles))
        for partida in self.listaPartidas:
            partida.mostrarInformacion()
        print("#######################################")

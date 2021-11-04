import random
from Videojuego.Jugador import *
from Videojuego.Partida import *
from Tanque.Tanque import *
from Mapa.Mapa import *
from Mapa.listaMapas import *


class Juego:
    def __init__(self, cantidadJugadores, cantidadPartidas):
        self.cantidadJugadores = cantidadJugadores
        self.listaJugadores = []
        self.cantidadPartidas = cantidadPartidas
        self.listaPartidas = []
        self.jugadorGanador = None
        self.juegoTerminado = False
        self.aceleracionVertical = 10
        self.aceleracionHorizontal = 0
        self.redefinirClima()
        self.redefinirGravedad()

    """Requisito 4: Se adapta para esta unidad de modo que al invocar la funcion agregarJugador, se 
    pasa el booleano de acuerdo al boton seleccionada al menu (es o no ia)."""

    def agregarJugador(self, i, pantalla, imagenTanqueAleatoria, datosJugador):
        # ahora el nombre no se define aquí, ya que se le pasa el arreglo que contiene los nombres
        tanque = Tanque(pantalla, imagenTanqueAleatoria)
        # datosJugador = (nombre,esIa)
        self.listaJugadores.append(Jugador(datosJugador[0], tanque, datosJugador[1]))

    """Requisito 2 y Requisito 4: Función que se adapta para registrar los jugadores en el juego, recibe
    los datos de los jugadores que es una lista de pares (nombreJug: str,esIa : boolean), para que los
    objetos jugadores se creen y se agregen al atributo listaJugadores del juego"""

    def registroJugadores(self, director, datosJugadores):
        listaImagenesTanque = ["imagenes/bloque/tanqueGris.png", "imagenes/bloque/tanqueAmarillo.png",
                               "imagenes/bloque/tanqueCeleste.png", "imagenes/bloque/tanqueRojo.png",
                               "imagenes/bloque/tanqueVerde.png", "imagenes/bloque/tanqueCafe.png"]
        # print("\n### REGISTRO DE JUGADORES ###")
        for i in range(0,self.cantidadJugadores):
            numAleatorio=random.randint(0,len(listaImagenesTanque)-1)
            imagenTanqueAleatoria=listaImagenesTanque[numAleatorio]
            listaImagenesTanque.remove(imagenTanqueAleatoria)
            self.agregarJugador(i+1,director.pantalla,imagenTanqueAleatoria,datosJugadores[i])
        return True  # termina con exito el registro

    # función que agregará una partida a la lista de partidas, cada partida agregará como jugadores activos a la
    # totalidad de jugadores que participan en el juego
    def agregarPartida(self, i, director):
        listaMapas = (mapa1, mapa2, mapa3)
        numeroRandom = random.randint(0, len(listaMapas) - 1)
        mapaRandom = listaMapas[numeroRandom]
        mapa = Mapa(mapaRandom)
        # mapa = Mapa(mapa1)
        mapa.generarMatriz(director.pantalla)
        partida = Partida(i, director, mapa)
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
        self.juegoTerminado = True

    def redefinirGravedad(self):
        self.aceleracionVertical = random.randint(5,20)
    
    def redefinirClima(self):
        self.aceleracionHorizontal = random.randint(-10,10)
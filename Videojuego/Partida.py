import random
from utilidades.colores import *
from Tanque.Proyectil import Proyectil

"""
from Tanque.Proyectil105 import *
from Tanque.ProyectilPerforante import *
from Tanque.Proyectil60 import *
"""


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

    """
    # funcion que termina la partida cuando queda sólo un jugador activo dentro de ella
    def terminar(self):
        self.estado = True
        #self.jugadorGanador = self.jugadoresActivos[0] # << antes, cuando ganaba el que quedaba en pie
        self.jugadorGanador.victorias += 1

    """

    def terminar(self, listaJugadores):
        empate = False
        ganadorAux = None
        print(f'--> OPONENTES DESTRUIDO PARTIDA {self.id} <--')
        # se recorre la lista de jugadores, contando sus oponentes destruidos
        for jugador in listaJugadores:
            print(f'jugador: {jugador.nombre} ==> op dest: { jugador.oponentesDestruidos}')
            if ganadorAux is None:
                ganadorAux = jugador
            else:
                if ganadorAux.oponentesDestruidos == jugador.oponentesDestruidos:
                    empate = True
                elif ganadorAux.oponentesDestruidos < jugador.oponentesDestruidos:
                    ganadorAux = jugador
                    empate = False
        if empate is True:
            self.jugadorGanador = None
        else:
            self.jugadorGanador = ganadorAux
            self.jugadorGanador.victorias += 1  # << para que sume una victora en la persepctiva de juego

    # funcion que brinda la posibilidad de eliminar jugadores al jugadorAtacante 
    def eliminarJugador(self, jugadorEliminado):
        self.jugadoresActivos.remove(jugadorEliminado)

    def generarPosicionesJug(self):
        cantDivisiones=2*len(self.jugadoresActivos)-1
        espacios=int(len(self.mapa.posPosiblesJug)/cantDivisiones)
        contador=0
        for jugador in self.jugadoresActivos:
            posAleatoria=self.mapa.posPosiblesJug[random.randint(contador,contador+espacios)]
            # ahora pos aleatoria es un par ordenado (x,y), por tanto:
            jugador.tanque.construirBloques(posAleatoria[0],posAleatoria[1])
            contador+=espacios*2

    def equiparArmasIniciales(self):
        for jugador in self.jugadoresActivos:
            proyectil105 = Proyectil("Proyectil 105", 3, 50, "imagenes/armas/proyectil105.png", ROJO)
            proyectilPerforante = Proyectil("Proyectil Perforante", 10, 40, "imagenes/armas/proyectilPerforante.png",
                                            NARANJA)
            proyectil60 = Proyectil("Proyectil 60", 3, 30, "imagenes/armas/proyectil60.png", AMARILLO)

            """
            antes del refactor
            proyectil105 = Proyectil105(50, 3)
            proyectilPerforante = ProyectilPerforante(40,10)
            proyectil60 = Proyectil60(30,3)
            """
            jugador.tanque.listaProyectiles.append(proyectil105)
            jugador.tanque.listaProyectiles.append(proyectilPerforante)
            jugador.tanque.listaProyectiles.append(proyectil60)
            jugador.tanque.proyectilActual = jugador.tanque.listaProyectiles[0]  # << la primera arma se equipa

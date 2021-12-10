import random
from utilidades.colores import *
from Tanque.Proyectil import Proyectil

"""
from Tanque.Proyectil105 import *
from Tanque.ProyectilPerforante import *
from Tanque.Proyectil60 import *
"""


class Partida:
    def __init__(self, id, director, mapa):
        self.id = id
        self.estado = False
        self.director=director
        self.pantalla = director.pantalla  # pantalla que le pasa el director)
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
        ganadorActual = None
        if(self.director.debug):
            print(f'\n---------------\n--> OPONENTES DESTRUIDO PARTIDA {self.id} <--')
        # se recorre la lista de jugadores, contando sus oponentes destruidos
        for jugador in listaJugadores:
            if(self.director.debug):
                print(f'jugador: {jugador.nombre} ==> op dest: { jugador.oponentesDestruidos}')
            if ganadorActual is None:
                ganadorActual = jugador
            else:
                if ganadorActual.oponentesDestruidos == jugador.oponentesDestruidos:
                    empate = True
                elif ganadorActual.oponentesDestruidos < jugador.oponentesDestruidos:
                    ganadorActual = jugador
                    empate = False
        if empate is True:
            self.jugadorGanador = None
        else:
            self.jugadorGanador = ganadorActual
            self.jugadorGanador.victorias += 1  # << para que sume una victora en la persepctiva de juego

    # funcion que brinda la posibilidad de eliminar jugadores al jugadorAtacante 
    def eliminarJugador(self, jugadorEliminado):
        self.jugadoresActivos.remove(jugadorEliminado)

    def generarPosicionesJug(self):
        """
        Ejemplo para 6 jugadores
        ------------------------

        j1 |----| j2 |---| j3 |---| j4 |---| j5 |---| j6

        |-----------------------------------------------|
            5 separaciones, 6 espacios utilizados por 6 jugadores

        (cantColumnas-cantJugadores)//(cantJugadores-1)= cantidad Bloques Separacion
        (cantColumnas-cantJugadores)%(cantJugadores-1)= margen de aleatoridad

        por ejemplo, 800x800 con bloques de 40, tiene 20 columnas de donde
        - 6 usarán jugadores (en caso de que juegen 6)
        - (20-6)/5 = 16/5 espacios, es decir, 3 bloques de espacio
        - 16%5 = 1 =>bloques aleatoridad

        es decir

        | | |<--->j2<--->j3<--->j4<--->j5<--->j6
        |---|
        aleatoridad
        jugador 1

        si sale c2 como pos inicial del jugador 1, se tiene:

        c2<--->c6<--->c10<--->c14<--->c18 <---> c22
        (j1)  (j2)    (j3)   (j4)     (j5)     (j6)
        """
        # posicion aleatoria
        cantidadColumnas=self.director.ancho/40
        cantidadJugadores=len(self.jugadoresActivos)
        delta=random.randint(0,int(cantidadColumnas/2 -1))
        if(cantidadJugadores != 2):
            columnasSeparacion=int((cantidadColumnas-cantidadJugadores)/(cantidadJugadores-1))
        else:
            columnasSeparacion=int((cantidadColumnas-cantidadJugadores)/(cantidadJugadores-1))-delta
        margenAleatorio=(cantidadColumnas-cantidadJugadores)%(cantidadJugadores-1)
        separacion=0
        contador=0
        while(contador<len(self.jugadoresActivos)):
              # para el primer jugador
              if(contador==0):
                columnaAleatoria=random.randint(0,margenAleatorio)
                # debug
                #print(f'Margen aleatorio: 0-{margenAleatorio}') # < debug aleatoridad
                #print(f'columnas separacion: {columnasSeparacion}') # < debug aleatoridad
                #print(f'contador {contador} => col al: {columnaAleatoria}') # < debug aleatoridad

                posAleatoria=self.mapa.posPosiblesJug[columnaAleatoria]
                self.jugadoresActivos[contador].tanque.construirBloques(posAleatoria[0],posAleatoria[1])
              else:
                separacion+=columnasSeparacion+1
                #print(f'contador {contador} => col al: {columnaAleatoria+separacion+1}') # < debug aleatoridad
                posAleatoria=self.mapa.posPosiblesJug[columnaAleatoria+separacion]
                self.jugadoresActivos[contador].tanque.construirBloques(posAleatoria[0],posAleatoria[1])
              # print(f'  separacion: {separacion}') # < debug aleatoridad
              contador+=1

    def equiparArmasIniciales(self, municionPerforante, municion105, municion60):
        for jugador in self.jugadoresActivos:
            """
            cambiar daño armas
            en este orden:
            50
            40
            30
            """
            proyectil105 = Proyectil("Proyectil 105", municion105, 50, "imagenes/armas/proyectil105.png", ROJO)
            proyectilPerforante = Proyectil("Proyectil Perforante", municionPerforante, 40, "imagenes/armas/proyectilPerforante.png",
                                            NARANJA)
            proyectil60 = Proyectil("Proyectil 60", municion60, 30, "imagenes/armas/proyectil60.png", AMARILLO)

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

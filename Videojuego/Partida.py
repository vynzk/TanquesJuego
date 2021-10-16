import random
from GUI.colores import *
from Tanque.Proyectil105 import *
from Tanque.ProyectilPerforante import *
from Tanque.Proyectil60 import *

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

    def generarPosicionesJug(self):
        listaColores = colores = [ROJO, VERDE, ORO, AZUL]
        cantidadJug = len(self.jugadoresActivos)
        cantEspacios = cantidadJug - 1
        espacio = int(len(self.mapa.posPosiblesJug) / (2 * cantidadJug - 1))
        contador = 0

        #debug
        #print(
        #    f'DEBUG: cant jug: {cantidadJug}, cant espacios: {cantEspacios}, cant posibles espacios: {len(self.mapa.posPosiblesJug)}, rango espacios: {espacio}')
        
        for jugador in self.jugadoresActivos:
            # ---- parametros aleatorios------------------------------
            numAle = random.randint(contador, contador + espacio -1)
            ubicacionRandom = self.mapa.posPosiblesJug[numAle]
            colorRandom = random.choice(listaColores)
            listaColores.remove(colorRandom)  # para no repetir el color
            
            # debug:
            #print(
            #    f'DEBUG: >>jugador: {jugador.nombre}, rango aleatorio ({contador},{contador + espacio}), numAleatorio: {numAle} , posRandom: {ubicacionRandom}, color: {colorRandom}')
            
            # se ubica el tanque y se crea su bloque
            jugador.tanque.construirBloques(ubicacionRandom[0], ubicacionRandom[1], colorRandom)
            contador += 2 * espacio

    def equiparArmasIniciales(self):
        for jugador in self.jugadoresActivos:
            proyectil105 = Proyectil105(50, 3)
            proyectilPerforante = ProyectilPerforante(40,10)
            proyectil60 = Proyectil60(30,3)
            jugador.tanque.listaProyectiles.append(proyectil105)
            jugador.tanque.listaProyectiles.append(proyectilPerforante)
            jugador.tanque.listaProyectiles.append(proyectil60)
            jugador.tanque.proyectilActual = jugador.tanque.listaProyectiles[0]  # << la primera arma se equipa

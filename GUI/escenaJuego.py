#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from GUI import plantillaEscena
from GUI import bloque
from Mapa import Mapa
from Tanque import Tanque
from Videojuego.AdministradorTurnos import AdministradorTurnos

class EscenaJuego(plantillaEscena.Escena):

    def __init__(self, director, AdministradorTurnos):  # constructor
        plantillaEscena.Escena.__init__(self, director) 
        self.fondo = pygame.image.load("GUI/imagenes/fondo.jpg") # se asigna un fondo a la escena juego
        self.mousex, self.mousey = 0, 0  # para movimiento del mouse
        self.partidas = self.director.game.listaPartidas # la escena juego tiene todas las partidas anteriormente creadas
        
        # ELEMENTOS DE LA ESCENA #
        #self.cuadrado = bloque.Bloque(self.director.pantalla, 100, 100, (222, 34, 221), 0, 0)  # cuadrado rosa movible
        self.piso = bloque.Bloque(self.director.pantalla, 1280, 100, (9,15,38), 0, 620)  # piso de limite
        self.mapa = Mapa.Mapa() # se ponen los bloques de tierra en el mapa
        self.AdministradorTurnos=AdministradorTurnos
        #self.partirPrimeraPartida() # << comienza el primer turno
        #self.partida1=self.director.game.listaPartidas[0] # << asignamos una variable a la primer partida
        #self.partida1.setTurno(Turno(self.partida1.jugadoresActivos[0],self.director.pantalla)) 
        # --MARTIN--esto es provisional, pero lo hice para mostrar los tanques en la pantalla
        #self.tanque = Tanque.Tanque(self.director.pantalla, 20, 20, (255, 0, 0), 20, 520) # temporal
        #self.tanque2 = Tanque.Tanque(self.director.pantalla, 20, 20, (0, 0, 255), 1200, 420) # temporal

        # sobreescritura de los metodos de plantilla escena

    """
    def partirPrimeraPartida(self):
        print("Partidas:",str(self.partidas))
        print("Turno partida1: ",str(self.partidas[0].turnoActual))
        self.partidas.iniciaTurno()
        # como la linea anterior no tiene turno, le asigno uno
        #self.partidas[0].setTurno(Turno.__init__(self.partidas[0].jugadoresActivos[0],self.director.pantalla))
        #self.partidas[0].setTurno(Turno(self.partidas[0].jugadoresActivos[0],self.director.pantalla))
        # ahora debería tener
        print("Turno partida1 asignado: ",str(self.partidas[0].turnoActual))
        print("Lista jugadores: ",str(self.partidas[0].jugadoresActivos))
    """
    def on_update(self): # <<<<<<<<<<<<<<<<<<<<< ACA QUEDA LA CAGÁ
        pygame.display.set_caption("EL JUEGO DE LOS TANQUES IMPLEMENTADO EN PYTHON SIN NOMBRE AUN")
        # va a crear un objeto turno, con la partidaActual la única partida que existe
        #turno=Turno(self.partidas[0]) # crea el objeto encargado de pasar los turnos a cada jugador.
        # se le asigna el turno a esa partida

        # BUCLE, que pasa el turno hasta que quede un jugador en pie

        # bucle controlado
        #print(self.partidas[0].turnoActual.jugadorActual)
        #self.partidas[0].PasarTurno() # < aqui pasa el turno y asigna el jugadorActual, aquí le tocaría al Jugador1


    def on_event(self, event):
        # prueba
        self.mousex, self.mousey = pygame.mouse.get_pos()  # capta el movimiento del mouse

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""
    
    def on_draw(self, pantalla):
        #pantalla.fill((0,0,0)) #relleno de pantalla importante en el bucle.
        iteradorBala=(self.director.iterador)*10 # fijo, no sacar
        pantalla.blit(self.fondo,(0,0))
        self.piso.dibujar()
        # cuadrado de debuggeo: no sacar hasta entrega final
        #self.cuadrado.definir_limite(self.mousex, self.mousey)
        # self.cuadrado.dibujar()

        # ELEMENTOS EN PANTALLA #
        """Aquí puedes hacer tus pruebas de interfaz, cuidado con el código de arriba"""
        self.mapa.dibujar(self.director.pantalla)
        # Se dibujan los bloques de los tanques de todos los jugadores activos de la partida
        self.dibujarTanques()
        """"
        self.tanque.bloque.dibujar() # temporal
        self.tanque2.bloque.dibujar() # temporal
        trayectoria=self.tanque.disparar(self.director.pantalla)
        CoordenadaTrayectoriaActual=trayectoria[iteradorBala] #
        self.tanque.bala.sigueTrayectoria(CoordenadaTrayectoriaActual)
        """

# --- metodos propios de escena juego ----#

    # dibujar los tanques de los jugadores en la pantalla
    def dibujarTanques(self):
       for jugador in self.partidas[0].jugadoresActivos:
           jugador.tanque.bloque.dibujar()
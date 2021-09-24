#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Videojuego.Partida import Partida
import pygame
import math
from GUI import plantillaEscena
from GUI import bloque
from Mapa import Mapa
from Mapa.listaMapas import *
import time
from GUI.colores import *



class EscenaJuego(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.fondo = pygame.image.load("GUI/imagenes/fondo.jpg")  # se asigna un fondo a la escena juego
        self.partidas = self.director.game.listaPartidas
        # para esta entrega hay solo una partida y 2 jugadores, por tanto:
        # la partida inicial será la primera partida (De momento es la única)
        self.partidaActual = self.partidas[0]
        # como tambien, el jugador inicial será el primer jugador activo de la primera partida
        self.jugadorActual = self.partidaActual.jugadoresActivos[0]
        self.trayectoria = []
        self.angulo = 40
        self.potencia = 114
        self.contador = 0
        self.flag = False
        self.jugadorEliminadoTurno = None
        self.xMaxDisparo = 0
        self.yMaxDisparo = 0

    def on_update(self):
        pygame.display.set_caption("EL JUEGO DE LOS TANQUES IMPLEMENTADO EN PYTHON SIN NOMBRE AUN")
        self.director.pantalla.blit(self.fondo, (0, 0))
        self.muestreoTurnoVelocidadAngulo()
        pygame.draw.rect(self.director.pantalla, COLOR_BINFERIOR, (0, 620, 1280, 100))  # bloque inferior
        self.partidaActual.mapa.dibujarMapa(self.director.pantalla)
        self.muestreoRastreoBala()
        self.dibujarTanques()

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.potencia -= 1
                # print("potencia: ", self.potencia, "; left: potencia --") # debug
            if event.key == pygame.K_RIGHT:
                self.potencia += 1
                # print("potencia: ", self.potencia, "; right: potencia ++") # debug
            if event.key == pygame.K_UP:
                self.angulo += 1
                # print("angulo: ", self.angulo, "; up: angulo ++") # debug
            if event.key == pygame.K_DOWN:
                self.angulo -= 1
                # print("angulo: ", self.angulo, "; down: angulo --") # debug
            if event.key == pygame.K_SPACE:
                self.flag = True
                print("\n>>> jugador/a ", self.jugadorActual.nombre, " disparó")

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        if self.director.game.juegoTerminado is not True:
            # si tiene más de un jugador activo la partida, sigue la partida jugandose
            if len(self.partidaActual.jugadoresActivos) > 1:
                if self.flag:
                    if self.trayectoria == []:
                        self.efectuarDisparo()
                    else:
                        if self.contador < len(self.trayectoria):
                            self.dibujarBala()
                        else:
                            self.jugadorEliminadoTurno = None  # << se limpia
                            self.contador = 0  # << el contador debe estar limpio para un nuevo jugador
                            self.trayectoria = []  # << la trayectoria debe estar limpio para un nuevo jugador
                            self.flag = False  # << debe apretar enter nuevamente el jugador para disparar
                            self.xMaxDisparo = 0
                            self.yMaxDisparo = 0
                            self.cambiarJugador()
                            self.mensajeTurno()
            else:
                self.partidaActual.terminar()
                self.mensajeFinPartida()  # como es una partida de momento, si gana la partida gana el juego
                self.director.game.definirGanador()  # << invocamos que defina un ganador del juego
                # Nota: el metodo anterior cambia el estado de juegoTerminado a True, por tanto, rompe el gameLoop
                # en el director.
        else:
            self.mensajeFinJuego()
            self.director.running = False  # rompe el gameloop para terminar el juego

    # ------------------------------FUNCIONES QUE REPRESENTAN ACCIONES DENTRO DEL JUEGO-----------------------------
    #Toma las posiciones de la bala y va viendo los posibles escenarios para buscar los valores maximos.
    def rastreoBala(self, xDisparo, yDisparo):
        if(self.xMaxDisparo>xDisparo and self.yMaxDisparo>yDisparo):
            return {self.xMaxDisparo, self.yMaxDisparo}
        elif(self.xMaxDisparo>xDisparo and self.yMaxDisparo<yDisparo):
            self.yMaxDisparo = yDisparo
        elif(self.xMaxDisparo<xDisparo and self.yMaxDisparo>yDisparo):
            self.xMaxDisparo = xDisparo
            return {self.xMaxDisparo, self.yMaxDisparo}
        else:
            self.xMaxDisparo = xDisparo
            self.yMaxDisparo = yDisparo
            return {self.xMaxDisparo, self.yMaxDisparo}

    def efectuarDisparo(self):
        delta = 0
        xJugador = self.jugadorActual.tanque.bloque.x
        yJugador = self.jugadorActual.tanque.bloque.y
        while True:
            xDisparo = xJugador + 10 + delta * self.potencia * math.cos(self.angulo * 3.1416 / 180)
            yDisparo = yJugador - 1 - (
                    delta * self.potencia * math.sin(self.angulo * 3.1416 / 180) - (9.81 * delta * delta) / 2)
            delta += 0.5  # si quieres que hayan más puntitos en la parabola, modifica esto
            self.rastreoBala(xDisparo, yDisparo)
            self.trayectoria.append((xDisparo, yDisparo))
            # ----------------------------------VERIFICAR SI TOCA BLOQUES-----------------------------------------------
            jugadorImpactado = self.colisionTanque(xDisparo, yDisparo)
            if jugadorImpactado is not None:  # si impacta con un tanque, se detiene la parabola (bala)
                # print("toqué un tanque") # debug
                self.jugadorEliminadoTurno = jugadorImpactado
                break

            elif self.colisionTierra(xDisparo, yDisparo):
                # print("toqué tierra") # debug
                break

            elif self.saleLimites(xDisparo, yDisparo):  # si impacta con un borde, se detiene la parabola (bala)
                # print("salí rango") # debug
                break

    def cambiarJugador(self):
        listaJugadoresActuales = self.partidaActual.jugadoresActivos
        if self.jugadorActual == listaJugadoresActuales[0]:
            self.angulo = 140
            self.potencia = 103
            self.jugadorActual = listaJugadoresActuales[1]
        else:
            self.angulo = 40
            self.potencia = 114
            self.jugadorActual = listaJugadoresActuales[0]

    # ----------------------------------FUNCIONES QUE VERIFICAN COLISIÓN---------------------------------------------
    # verifica si un bloque de tierra fue impactado, si lo fue retorna true, en caso contrario false
    def colisionTierra(self, xDisparo, yDisparo):
        bloquesTierra = self.partidaActual.mapa.listaBloques
        for bloque in bloquesTierra:
            if bloque.colision(xDisparo, yDisparo):
                return True  # toca tierra y para el impacto
        return False  # permanece en el rango correcto

    # verifica si un borde del mapa fue impactado, si lo fue retorna true, en caso contrario false
    def saleLimites(self, xDisparo, yDisparo):
        if xDisparo >= 1280 or yDisparo >= 730 or xDisparo <= 0 or yDisparo <= 0:
            return True  # sale del rango
        return False  # dentro del rango

    # verifica si un tanque fue impactado, retorna true si lo fue, en caso contrario false (aun no elimina al tanque)
    # ni menos lo saca del juego, sólo detecta el impacto
    def colisionTanque(self, xDisparo, yDisparo):
        for jugador in self.partidaActual.jugadoresActivos:
            bloqueTanque = jugador.tanque.bloque
            if bloqueTanque.colision(xDisparo, yDisparo):
                return jugador  # si el tanque fue impactado
        return None  # si ningun tanque de un jugador fue impactado

    # ---------------------------------FUNCIONES QUE DIBUJAN EN LA ESCENA------------------------------------------
    def dibujarTanques(self):
        for jugador in self.partidas[0].jugadoresActivos:
            jugador.tanque.bloque.dibujar()

    def dibujarBala(self):
        coord = self.trayectoria[self.contador]
        pygame.draw.circle(self.director.pantalla, VERDE, (int(coord[0]), int(coord[1])), 3)
        self.contador += 1
        if self.contador == len(self.trayectoria):
            if self.jugadorEliminadoTurno is not None:
                print("<<< el jugador/a ", self.jugadorEliminadoTurno.nombre, " ha sido impactado por ",
                      self.jugadorActual.nombre)
                self.partidaActual.eliminarJugador(self.jugadorEliminadoTurno)  # elimina al jugador
        pygame.time.wait(125)

    # ----------------------------------METODOS QUE MUESTRAN TEXTO-------------------------------------------------
    def mensajeTurno(self):
        fuente = pygame.font.SysFont("arial", 30)
        text = "TURNO: " + str.upper(self.jugadorActual.nombre)
        colorTanque = self.jugadorActual.tanque.color
        mensaje = fuente.render(text, 1, colorTanque)
        self.director.pantalla.blit(mensaje, (450, 300))
        pygame.display.update()
        time.sleep(2)

    def mensajeFinPartida(self):
        fuente = pygame.font.SysFont("arial", 30)
        jugadorGanador = self.partidaActual.jugadorGanador
        colorTanque = jugadorGanador.tanque.color
        text = "FIN DE PARTIDA ; GANADOR: " + str.upper(jugadorGanador.nombre)
        mensaje = fuente.render(text, 1, colorTanque)
        self.director.pantalla.blit(mensaje, (450, 300))
        pygame.display.update()
        time.sleep(1)

    def mensajeFinJuego(self):
        fuente = pygame.font.SysFont("arial", 30)
        jugadorGanador = self.director.game.jugadorGanador
        colorTanque = jugadorGanador.tanque.color
        text = "FIN DEL JUEGO ; GANADOR: " + str.upper(jugadorGanador.nombre)
        mensaje = fuente.render(text, 1, colorTanque)
        self.director.pantalla.blit(mensaje, (450, 400))
        pygame.display.update()
        time.sleep(3)

    def muestreoTurnoVelocidadAngulo(self):
        fuente = pygame.font.SysFont("arial", 20)
        text = "Turno: %s ; angulo: %d ° ; velocidad: %d (m/s)" % (
            self.jugadorActual.nombre, self.angulo, self.potencia)
        mensaje = fuente.render(text, 1, BLANCO)
        self.director.pantalla.blit(mensaje, (15, 5))

    #Define el mensaje a mostrar en pantalla junto a sus caracteristicas.
    def muestreoRastreoBala(self):
        fuente = pygame.font.SysFont("arial", 20)
        # se pasan a int ya que son numeros decimales y luego ello se pasa a str para concatenar en un sólo string
        text = "Estado disparo: "+str(self.flag)+"; Distancia máxima: "+str(int(self.xMaxDisparo))\
               +" [px] ; Altura máxima: "+str(int(self.yMaxDisparo))
        mensaje = fuente.render(text, 1, BLANCO)
        self.director.pantalla.blit(mensaje, (15, 30))
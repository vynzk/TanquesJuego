#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import math
from GUI import plantillaEscena
from GUI import bloque
from Mapa import Mapa


class EscenaJuego(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.fondo = pygame.image.load("GUI/imagenes/fondo.jpg")  # se asigna un fondo a la escena juego
        self.mousex, self.mousey = 0, 0  # para movimiento del mouse
        self.partidas = self.director.game.listaPartidas  # la escena juego tiene todas las partidas anteriormente creadas
        self.piso = bloque.Bloque(self.director.pantalla, 1280, 100, (9, 15, 38), 0, 620)  # piso de limite
        self.mapa = Mapa.Mapa()  # se ponen los bloques de tierra en el mapa
        self.jugadorActual = self.director.game.listaPartidas[0].jugadoresActivos[0]
        self.partidaActual = self.director.game.listaPartidas[0]

    def on_update(self):  # <<<<<<<<<<<<<<<<<<<<< ACA QUEDA LA CAGÁ
        pygame.display.set_caption("EL JUEGO DE LOS TANQUES IMPLEMENTADO EN PYTHON SIN NOMBRE AUN")

    def on_event(self, event):
        self.mousex, self.mousey = pygame.mouse.get_pos()  # capta el movimiento del mouse

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        # pantalla.fill((0,0,0)) #relleno de pantalla importante en el bucle.
        iteradorBala = self.director.iterador * 10  # fijo, no sacar
        pantalla.blit(self.fondo, (0, 0))
        self.piso.dibujar()
        self.mapa.dibujar(self.director.pantalla)
        self.dibujarTanques()
        self.efectuarDisparo()
        enter = str(input("Apreta enter para pasar de turno y refrescar pantalla"))

    # de luis para kekes: sabes que dispara peeeeeeeeero no se muestra en la pantalla, me sigue preguntando el
    # angulo y potencia pero no logro ver la trayectoria
    def efectuarDisparo(self):
        print("---------------------------------------------------------------")
        print("Turno jugador: ",self.jugadorActual.nombre)
        delta = 0
        angulo = int(input("Ingrese su angulo: "))
        velocidad = int(input("Ingrese su potencia: "))
        cuadradoJugador = self.jugadorActual.tanque.bloque
        while delta <= 20:
            xDisparo = cuadradoJugador.x + delta * velocidad * math.cos(angulo * 3.1416 / 180)
            yDisparo = cuadradoJugador.y - (delta * velocidad * math.sin(angulo * 3.1416 / 180) - (9.81 * delta * delta) / 2)
            delta += 0.01
            # hay que transformarlos a int
            xDisparo = int(xDisparo)
            yDisparo = int(yDisparo)
            pygame.draw.circle(self.director.pantalla, (0, 255, 0), (xDisparo, yDisparo),1)
            print("debería dibujar una pelota en: (", xDisparo, ",", yDisparo, ")")  # debug

    def dibujarTanques(self):
        for jugador in self.partidas[0].jugadoresActivos:
            jugador.tanque.bloque.dibujar()

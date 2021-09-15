#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
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

    def dibujarTanques(self):
        for jugador in self.partidas[0].jugadoresActivos:
            jugador.tanque.bloque.dibujar()

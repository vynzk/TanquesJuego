#!/usr/bin/env python
# -*- coding: utf-8 -*-
from GUI.escenaRegistro import EscenaRegistro
import pygame
from GUI import plantillaEscena
from GUI.Boton import Boton


class EscenaHome(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
       #self.guardarPartida()
        self.boton_play = None
        self.fondo= pygame.image.load("GUI/imagenes/fondoHome.png")
        self.cambiaDePartida()

    def on_update(self):
        pygame.display.set_caption("Home")  # no cambies esto aun... es para debuggueo
        

    def on_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_play):
                self.cambiaDePartida()

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        pantalla.blit(self.fondo, (0,0))
        botonJugar= pygame.image.load("GUI/imagenes/botones/botonJugar.png")
        self.boton_play = Boton(pantalla, "play", 560, 500,botonJugar)
        self.boton_play.dibujaBoton()

    def cambiaDePartida(self):
        self.director.cambiarEscena(EscenaRegistro(self.director))

    #def guardarPartida(self):
    #    juegoEscena2 = EscenaRegistro(self.director)
    #    self.director.guardarEscena(juegoEscena2)
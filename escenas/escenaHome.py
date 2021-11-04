#!/usr/bin/env python
# -*- coding: utf-8 -*-
from escenas.escenaRegistro import EscenaRegistro
from escenas.escenaConfig import EscenaConfig
import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton


class EscenaHome(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.boton_play = None
        self.boton_config= None
        self.fondo= pygame.image.load("imagenes/fondoHome.png")
        self.cambiaDePartida()

    def on_update(self):
        pygame.display.set_caption("Home")  # no cambies esto aun... es para debuggueo
        

    def on_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_play):
                self.cambiaDePartida()
            if self.director.checaBoton(self.director.mousePos, self.boton_config):
                self.cambiaConfiguracion()

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        pantalla.blit(self.fondo, (0,0))
        botonJugar= pygame.image.load("imagenes/botones/botonJugar.png")
        self.boton_play = Boton(pantalla, "play", 540, 420,botonJugar,127,40)
        self.boton_play.dibujaBoton()
        self.boton_config = Boton(pantalla, "configuracion", 540, 470,botonJugar,127,40)
        self.boton_config.dibujaBoton()

    def cambiaDePartida(self):
        self.director.cambiarEscena(EscenaRegistro(self.director))
    def cambiaConfiguracion(self):
        self.director.cambiarEscena(EscenaConfig(self.director))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from GUI.escenaRegistro import EscenaRegistro
import pygame
from GUI import plantillaEscena
from GUI.Boton import Boton

class EscenaCambioArma(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.botonVolver = None
        

    def on_update(self):
        pygame.display.set_caption("Cambio de armas")  # no cambies esto aun... es para debuggueo
        

    def on_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            #if self.director.checaBoton(self.director.mousePos, self.boton_play):
                #self.cambiaDePartida()

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        #self.boton_play = Boton(pantalla, "play", 540, 320)
        pantalla.fill((0,0,0))
        
        

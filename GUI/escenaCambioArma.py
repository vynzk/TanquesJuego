#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from GUI import plantillaEscena
from GUI.Boton import Boton

class EscenaCambioArma(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.botonVolver = None
        self.botonAplicar = None
        self.jugadorActual = director.listaEscenas[0].jugadorActual #pos 0 siempre debe corresponder a escena juego 
        # -- imagenes -- #
        self.fondo= pygame.image.load("GUI/imagenes/fondoNublado.png") #por ahora
        self.panel= pygame.image.load("GUI/imagenes/panelArmas.png")
        self.redimensionarPanel(500,500)
        #---------------- #

    def on_update(self):
        pygame.display.set_caption("Cambio de armas")  # no cambies esto aun... es para debuggueo
        

    def on_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.botonVolver):
                print("funciona boton de volver")
                self.vuelveJuego()
            if self.director.checaBoton(self.director.mousePos, self.botonAplicar):
                print("funciona boton de aplicar")

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        pantalla.blit(self.fondo, (0,0))
        pantalla.blit(self.panel, (390, 100))
        # imagenes -- botones
        volver= pygame.image.load("GUI/imagenes/botones/botonVolver.png")
        aplicar= pygame.image.load("GUI/imagenes/botones/botonAplicar.png")
        
        self.botonVolver = Boton(pantalla, "volver", 750,650,volver)
        self.botonVolver.dibujaBoton()
        self.botonAplicar = Boton(pantalla, "aplicar", 400,650,aplicar)
        self.botonAplicar.dibujaBoton()
    def redimensionarPanel(self, x,y):
        self.panel= pygame.transform.scale(self.panel, (x,y) )
    def vuelveJuego(self):
        juegoActual= self.director.listaEscenas[0]
        self.director.cambiarEscena(juegoActual)

        
    


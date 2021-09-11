#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from GUI import plantillaEscena
from GUI.Boton import Boton
from GUI.escenaJuego import EscenaJuego




class EscenaRegistro(plantillaEscena.Escena):
        
        def __init__(self, director): #constructor
            plantillaEscena.Escena.__init__(self, director)
            #self.mousex,self.mousey= 0,0 #para movimiento del mouse
            self.boton_registrar= None #botón para cambiar a escenaJuego en la versión final
            self.cambioEscenaJuego()
            
        
        def on_update(self):
            pass
        def on_event(self,evento):
            if evento.type == pygame.MOUSEBUTTONDOWN:
                self.director.mousePos= pygame.mouse.get_pos() #arreglar: usar una sola funcion de coordenadas mouse... CUIDADO
                if (self.director.checaBoton(self.director.mousePos,self.boton_registrar)) == True:
                    print("miau")
                    self.cambioEscenaJuego()
                    
                    

        
        """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""
        def on_draw(self, pantalla):
            self.boton_registrar= Boton(pantalla,"comenzar")
            self.boton_registrar.dibujaBoton()
            
        def cambioEscenaJuego(self):
            self.director.cambiarEscena(EscenaJuego(self.director)) #proximamente... la escena juego tendrá sus atributos personalizables. 
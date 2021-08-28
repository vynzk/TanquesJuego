#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import plantillaEscena

class EscenaHome(plantillaEscena.Escena):
        
        def __init__(self, director): #constructor
            plantillaEscena.Escena.__init__(self, director)
        
        #sobreescritura de los metodos de plantilla escena
        def on_update(self):
            pass
        def on_event(self):
            pass
        
        """Esta función corresponde a lo mostrado en pantalla"""
        def on_draw(self, screen):
            #prueba 
            pygame.draw.line(screen, (255,0,0), [10, 10], [650, 470], 2)

#------ pruebas de la escena -----#
def main():
	pass

if __name__ == '__main__':
	main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import plantillaEscena

class EscenaJuego(plantillaEscena.Escena):
        
        def __init__(self, director): #constructor
            plantillaEscena.Escena.__init__(self, director)

        
        #sobreescritura de los metodos de plantilla escena
        def on_update(self):
            pass
        def on_event(self):
            #prueba
            self.mousex, self.mousey = pygame.mouse.get_pos()
        
        """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""
        def on_draw(self, pantalla):
            #prueba
            pantalla.fill((0,0,0))#relleno de pantalla importante en el bucle.
            pygame.draw.rect(pantalla, (0,255,0) , (self.mousex,self.mousey,100,100))


#------ pruebas de la escena -----#
def main():
	pass

if __name__ == '__main__':
	main()
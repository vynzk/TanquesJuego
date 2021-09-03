#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import plantillaEscena
from GUI import bloque


class EscenaJuego(plantillaEscena.Escena):
        
        def __init__(self, director): #constructor
            plantillaEscena.Escena.__init__(self, director)
            self.mousex,self.mousey= 0,0
            self.cuadrado = bloque.Bloque(self.director.pantalla, 100, 100, (222, 34, 221), 0, 0)
            self.piso = bloque.Bloque(self.director.pantalla, 1280, 100, (115, 45, 20), 0, 620)

        
        #sobreescritura de los metodos de plantilla escena
        def on_update(self):
            pass
        def on_event(self):
            #prueba
            self.mousex, self.mousey = pygame.mouse.get_pos() #capta el movimiento del mouse
        
        """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""
        def on_draw(self, pantalla):
            #prueba
            pantalla.fill((0,0,0))#relleno de pantalla importante en el bucle.
            self.piso.dibujar() #arreglar: debería usar el atributo x,y...
            self.cuadrado.definir_limite(self.mousex,self.mousey)
            self.cuadrado.dibujar()

            


#------ pruebas de la escena -----#
def main():
	pass

if __name__ == '__main__':
	main()
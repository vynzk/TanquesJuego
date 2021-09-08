# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 00:15:42 2021

@author: pc
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 22:58:45 2021

@author: toña
"""

import pygame
from pygame.locals import *

pygame.init()

class Mapa:
    
    def __init__(self):
        #medidas
        self.ancho = 1280
        self.alto = 720
        self.pixel_y = 30
        self.pixel_x =30
    
        #colores
        self.blanco=(255, 255, 255)
        self.negro=(0, 0, 0)
        self.rojo=(255, 0, 0)
        self.verde=(0, 255, 0)
        self.azul=(0, 0, 255)
        self.marron=(150, 70, 10)
        
        #mapa
        self.mapa = [
          "                                           ",
          "                                           ",
          "                                           ",
          "                                           ",
          "                                           ",
          "                                           ",
          "                                           ",
          "                                           ",
          "                                           ",
          "         XXXXX                   X         ",
          "        XXXXXXX                 XXX        ",
          "       XXXXXXXXX              XXXXXX       ",
          "     XXXXXXXXXXX             XXXXXXXX      ",
          "XXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXX   XXX",
          "XXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXX  XXXX",
          "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
          "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
          "                                           ",
          "                                           ",
          "                                           ",
          "                                           ",
          "                                           ",
          "                                           ",
          "                                           "]
      

 
    def construir_mapa(self):   
      muros = []
      x = 0
      y = 0
      for fila in self.mapa:
          for muro in fila:
              if muro == "X":
                  muros.append(pygame.Rect(x, y, self.pixel_x, self.pixel_y))
              x += self.pixel_x
          x = 0
          y += self.pixel_y
      return muros
    
    def dibujar_mapa(self, superficie, muros):
        for muro in muros:
            self.dibujar_muros(superficie, muro)
            
            
    def dibujar_muros(self, superficie, rectangulo):
      pygame.draw.rect(superficie, self.marron, rectangulo)
      pygame.draw.circle(superficie, self.marron, (125, 390), 50)
      pygame.draw.circle(superficie, self.marron, (600, 410), 50)
      pygame.draw.circle(superficie, self.marron, (350, 270), 50)
      
             
            
    def iniciar_construccion(self,pantalla):
        muros = self.construir_mapa()  
        self.dibujar_mapa(pantalla, muros)
          
    
    
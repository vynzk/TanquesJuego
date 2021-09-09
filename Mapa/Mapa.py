import pygame
from pygame.locals import *

pygame.init()

class Mapa:
    
    def __init__(self):
        #medidas
        self.ancho = 1280
        self.alto = 730
        self.pixel_y = 20
        self.pixel_x = 20
        self.listaMuros = [] #bloques de la matriz
    
        #colores
        self.blanco=(255, 255, 255)
        self.negro=(0, 0, 0)
        self.rojo=(255, 0, 0)
        self.verde=(0, 255, 0)
        self.azul=(0, 0, 255)
        self.marron=(150, 70, 10)
        
        #mapa
        self.mapa = [
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                               ",
          "                                                       XXXXXXXX",
          "         XXXXX                   X                 XXXXXXXXXXXX",
          "        XXXXXXX                 XXX              XXXXXXXXXXXXXX",
          "       XXXXXXXXX              XXXXXX            XXXXXXXXXXXXXXX",
          "     XXXXXXXXXXX             XXXXXXXX        XXXXXXXXXXXXXXXXXX",
          "XXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXX",
          "XXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXX",
          "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
          "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",]
          
      

 
    def construir_mapa(self):   #define la matriz de cuadrados
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

             
            
    def iniciar_construccion(self,pantalla):
        muros = self.construir_mapa()  #matriz
        self.dibujar_mapa(pantalla, muros)
          
    
    
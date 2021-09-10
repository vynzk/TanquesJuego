from Mapa.cuadrado import Cuadrado
from GUI.bloque import Bloque
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
        self.listaCuadrados=[]
    
        #colores
        self.blanco=(255, 255, 255)
        self.negro=(0, 0, 0)
        self.rojo=(255, 0, 0)
        self.verde=(0, 255, 0)
        self.azul=(0, 0, 255)
        self.marron=(150, 70, 10)
        
        #mapa
        self.mapa = [
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                                ",
          "                                                       XXXXXXXXX",
          "         XXXXX                   X                 XXXXXXXXXXXXX",
          "        XXXXXXX                 XXX              XXXXXXXXXXXXXXX",
          "       XXXXXXXXX              XXXXXX            XXXXXXXXXXXXXXXX",
          "     XXXXXXXXXXX             XXXXXXXX        XXXXXXXXXXXXXXXXXXX",
          "XXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXX",
          "XXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXX",
          "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
          "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",]
          
      

 
    def dibujar(self,pantalla):   #define la matriz de cuadrados
      muros = []
      x = 0
      y = 0
      for fila in self.mapa:
          for muro in fila:
              if muro == "X":
                  cuadrado=Cuadrado(pantalla,self.pixel_x,self.pixel_y,(128,64,0),x,y)
                  self.listaCuadrados.append(cuadrado)
                  cuadrado.dibujar()
              x += self.pixel_x
          x = 0
          y += self.pixel_y
      return muros
    
    
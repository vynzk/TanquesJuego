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
        self.ancho= 1280
        self.alto= 720
    
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
                  muros.append(pygame.Rect(x, y, 30, 30))
              x += 30
          x = 0
          y += 30
      return muros
    
    def dibujar_mapa(self, superficie, muros):
        for muro in muros:
            self.dibujar_muros(superficie, muro)
            
            
    def dibujar_muros(self, superficie, rectangulo):
      pygame.draw.rect(superficie, self.marron, rectangulo)
      pygame.draw.circle(superficie, self.marron, (125, 390), 50)
      pygame.draw.circle(superficie, self.marron, (600, 410), 50)
      pygame.draw.circle(superficie, self.marron, (350, 270), 50)
      
             
            
    def iniciar_construccion(self):
        
        
        #Ventana
        ventana= pygame.display.set_mode((self.ancho, self.alto), pygame.RESIZABLE)
        reloj = pygame.time.Clock()
        
        #DATOS
        muros = self.construir_mapa()
        
        
        #bucle principal
        jugando = True
        while jugando:
        
          reloj.tick(60)
        
          #evento
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
              jugando = False
            if event.type == VIDEORESIZE:
                if not FULLSCREEN:
                    ventana = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_ESCAPE:
                jugando = False
        
          #dibujo
          ventana.fill(self.negro)
          
          self.dibujar_mapa(ventana, muros)
        
          pygame.display.update()
          
              
            
mapa = Mapa()
mapa.iniciar_construccion()

pygame.quit()
    
    
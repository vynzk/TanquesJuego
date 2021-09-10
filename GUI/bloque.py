
import pygame
"""esta clase corresponde a la clase padre de los elementos que se interrelacionan
    dentro del juego. 
    
    importancia: recalca en las coordenadas de posición y tamaño del objeto dentro de la pantalla"""
class Bloque:
    def __init__(self, pantalla , ancho, alto, color, x, y):
        self.ancho=ancho
        self.alto=alto
        self.limiteX=1280-self.ancho
        self.limiteY=520
        self.x=x
        self.y=y
        self.color= color
        self.pantalla = pantalla
    def dibujar(self):
        pygame.draw.rect(self.pantalla, self.color , (self.x,self.y,self.ancho,self.alto))
    def definir_limite(self, x, y): # importancia: suelo.
        self.x=x
        self.y=y
        if self.x >= self.limiteX:
            self.x= self.limiteX
        if self.y >= self.limiteY:
            self.y=self.limiteY

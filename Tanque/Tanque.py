import pygame
import math
import random
from GUI.bloque import Bloque
class Tanque:

    def __init__(self,pantalla,ancho,alto,color,x,y):
        Bloque.__init__(self,pantalla,ancho,alto,color,x,y)
        self.modelo = "Default"
        self.posx = self.x
        self.posy = self.y

    #def dibujar_tanques(self, pantalla):
        #self.tanque = bloque.Bloque(pantalla, 20, 20, (0, 255, 0), self.posx, self.posy)
    #def dibujar(self):
        #pygame.draw.rect(self.pantalla, self.color , (self.x,self.y),(self.ancho,self.alto))


    def disparar(self, pantalla):
        delta = 0
        velocidad = 60
        angulo = 60

        while delta<=100:
            self.posx = self.posx+50 + delta*velocidad*math.cos(angulo*3.1416/180)
            self.posy = self.posy+14 - (delta*velocidad*math.sin(angulo*3.1416/180) - (9.81*delta*delta)/2)
            #self.posx = x
            #self.posy = y
            delta+=0.25   

            pygame.draw.rect(pantalla, 10, 10, (255,0,0), self.posx, self.posy)

    def mostrarInformacion(self):
        return "modelo: " + str(self.modelo)
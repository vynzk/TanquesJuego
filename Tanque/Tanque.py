import pygame
import math
import random
from GUI import bloque

class Tanque:


    def __init__(self,modelo,color,vida):
        self.vivo = True
        self.modelo = "Default"
        self.color = color


    def dibujar_tanques(self):
        pygame.draw.rect(ventana, (0, 255, 0), 20, 520, 20, 20)

    def dibujar_tanque(self, director):
        self.tanque = bloque.Bloque(self.director.pantalla, 20, 20, (0, 255, 0), 20, 520)
        self.tanque.dibujar()

        self.tanque2 = bloque.Bloque(self.director.pantalla, 20, 20, (0, 0, 255), 1200, 420)
        self.tanque2.dibujar()

    def mostrarInformacion(self):
        return "vivo:"+str(self.vivo)+" | modelo: "+str(self.modelo)





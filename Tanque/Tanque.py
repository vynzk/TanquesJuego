import pygame
import math
import random

class Tanque:

    def __init__(self, modelo):
        self.modelo = "Default"
        self.posx = posx
        self.posy = posy

    def dibujar_tanques(self, pantalla):
        self.tanque = bloque.Bloque(pantalla, 20, 20, (0, 255, 0), self.posx, self.posy)

    def disparar(self, pantalla):
        delta = 0
        velocidad = 60
        angulo = 60

        while delta<=100:
            x = 20+50 + delta*velocidad*math.cos(angulo*3.1416/180)
            y = 520+14 - (delta*velocidad*math.sin(angulo*3.1416/180) - (9.81*delta*delta)/2)
            #self.posx = x
            #self.posy = y
            delta+=0.25   

            pygame.draw.rect(ventana, 10, 10, (255,0,0), proyectil_size, x, y)

    def mostrarInformacion(self):
        return "modelo: " + str(self.modelo)
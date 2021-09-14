import pygame
import math
import random
from Mapa.cuadrado import Cuadrado


class Tanque():
    # cada Tanque, al crearse se le asociará un objeto Cuadrado (el cual lo representará en el mapa)
    def __init__(self, pantalla, ancho, alto, color, x, y):
        self.cuadrado = Cuadrado(pantalla, ancho, alto, color, x, y)
        self.modelo = "Default"

    # def dibujar_tanques(self, pantalla):
    # self.tanque = bloque.Bloque(pantalla, 20, 20, (0, 255, 0), self.posx, self.posy)
    # def dibujar(self):
    # pygame.draw.rect(self.pantalla, self.color , (self.x,self.y),(self.ancho,self.alto))

    # al disparar se usan las coordenadas que representa el cuadrado del tanque en el mapa como inicio del disparo
    """
    def disparar(self, pantalla):
        delta = 0
        velocidad = 70
        angulo = 60
        
        while delta <= 500:
            xDisparo = self.cuadrado.getX() + delta * velocidad * math.cos(angulo * 3.1416 / 180)
            yDisparo = self.cuadrado.getY() - (delta * velocidad * math.sin(angulo * 3.1416 / 180) - (9.81 * delta * delta) / 2)
            delta += 0.01
            pygame.draw.circle(pantalla, (0, 255, 0), (xDisparo, yDisparo),1)
    """

    def getCuadrado(self):
        return getCuadrado()
        
    def mostrarInformacion(self):
        return "modelo: " + str(self.modelo)

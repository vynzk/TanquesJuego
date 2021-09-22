import pygame
import math
from GUI import bloque




class Tanque:
    # cada Tanque, al crearse se le asociará un objeto Cuadrado (el cual lo representará en el mapa)
    def __init__(self, pantalla, ancho, alto, color, x, y):
        self.x = x
        self.y = y
        self.bloque = bloque.Bloque(pantalla, ancho, alto, color, self.x, self.y)
        self.modelo = "Default"
        self.color = color
        self.disparoTrayectoria = []

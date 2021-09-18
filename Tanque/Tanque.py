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


    # al disparar se usan las coordenadas que representa el cuadrado del tanque en el mapa como inicio del disparo
    def disparar(self, pantalla):  # retorna trayectoria
        delta = 0
        velocidad = 70
        angulo = 60


        disparoTrayectoria = []
        while delta <= 20:
            xDisparo = self.bloque.x + delta * velocidad * math.cos(angulo * 3.1416 / 180)
            yDisparo = self.bloque.y - (
                    delta * velocidad * math.sin(angulo * 3.1416 / 180) - (9.81 * delta * delta) / 2)
            disparoTrayectoria.append((xDisparo, yDisparo))
            delta += 0.01
            # descomentar si quieren debuguear la trayectoria
            pygame.draw.circle(pantalla, (0, 255, 0), (xDisparo, yDisparo), 1)
        return disparoTrayectoria

    def mostrarInformacion(self):
        return "modelo: " + str(self.modelo)

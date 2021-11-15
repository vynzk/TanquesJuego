from Mapa.bloque import Bloque
import pygame
from Mapa.listasEscenarios import *
import random

pygame.init()


class Mapa:
    def __init__(self):
        # medidas
        self.pixel_y = 40
        self.pixel_x = 40
        self.listaBloques = []
        self.posPosiblesJug = []
        self.bloquePos = []
        self.imagenCemento = bloquesLista[random.randint(0,len(bloquesLista)-1)]

    def dibujarMapa(self, pantalla):
        for bloque in self.listaBloques:
            bloque.dibujar()

    def generarMapa(self,pantalla,ancho,alto):
        matriz=[]



    
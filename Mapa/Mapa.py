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
        cantidadColumnas=int(ancho/40)
        cantidadBloquesColumna=int(alto/40)

        for i in range(0,cantidadColumnas):
            """ genera el mapa con 0 y 1, 0: cielo, 1: tierra"""
            columna=[]
            for j in range(0,cantidadBloquesColumna):
                """ si es menor a la mitad, añadirá solo 0 == cielo """
                if(j<cantidadBloquesColumna/2):
                    columna.append(0)
                else:
                        columna.append(1)
            matriz.append(columna) 

        numColumna=0
        for columna in matriz:
            numFila=0
            generoPosiblePos=False
            try:
                while(numFila<=cantidadBloquesColumna):
                    if(columna[numFila+1]==1 and generoPosiblePos==False):
                        self.posPosiblesJug.append([numColumna * self.pixel_x, numFila * self.pixel_y])
                        generoPosiblePos=True
                    if(columna[numFila]==1 and generoPosiblePos==True):
                        bloque = Bloque(pantalla, self.pixel_x, self.pixel_y, self.imagenCemento, numColumna * self.pixel_x,numFila * self.pixel_y)
                        self.listaBloques.append(bloque)
                    numFila+=1
            except:
                pass
            numColumna+=1



    
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

    def generarAlturasColumnas(self,cantColumnas,cantBloquesColumna):
        alturaActual=cantBloquesColumna/2
        listaAlturas=[]

        listaVariante=[]
        variante=random.randint(1,3)
        contador=0
        caso=0;
        if(variante==1):
            while(contador<cantColumnas//3):
                if caso==0:
                    listaVariante.append(1)
                    caso=1
                    contador+=1
                elif caso==1:
                    listaVariante.append(-1)
                    caso=2
                    contador+=1
                elif caso==2:
                    listaVariante.append(0)
                    caso=0
                    contador+=1
        elif(variante==2):
            while(contador<cantColumnas//3):
                if caso==0:
                    listaVariante.append(-1)
                    caso=1
                    contador+=1
                elif caso==1:
                    listaVariante.append(1)
                    caso=2
                    contador+=1
                elif caso==2:
                    listaVariante.append(0)
                    caso=0
                    contador+=1
        elif(variante==3):
            while(contador<cantColumnas//3):
                if caso==0:
                    listaVariante.append(0)
                    caso=1
                    contador+=1
                elif caso==1:
                    listaVariante.append(-1)
                    caso=2
                    contador+=1
                elif caso==2:
                    listaVariante.append(1)
                    caso=0
                    contador+=1


        for variante in listaVariante:
            if(variante==0):
                for i in range(0,3):
                    listaAlturas.append(alturaActual)
            elif(variante==1):
                for i in range(0,3):
                    alturaActual-=1
                    listaAlturas.append(alturaActual)
            else:
                for i in range(0,3):
                    alturaActual+=1
                    listaAlturas.append(alturaActual)

        bloquesSinArmar=cantColumnas%3
        """Sin esto, para casos por ejemplo con 22 columnas, al dividir por 3 generará
        7 variantes de subida, bajada o mantenerse, sobrando 1 bloque por rellenar, esto
        se encargará de completar el mapa"""
        if(bloquesSinArmar>0):
            contador=0
            while(contador<bloquesSinArmar):
                listaAlturas.append(alturaActual)
                contador+=1

        return listaAlturas

    def generarMapa(self,pantalla,ancho,alto):
        matriz=[]
        cantidadColumnas=int(ancho/40)
        # se resta 200 porque ese espacio lo usará la barra
        cantidadBloquesColumna=int((alto-160)/40)
        lista= self.generarAlturasColumnas(cantidadColumnas,cantidadBloquesColumna)
        for altura in lista:
            columna=[]
            for i in range(0,cantidadBloquesColumna):
                if i<altura:
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


    
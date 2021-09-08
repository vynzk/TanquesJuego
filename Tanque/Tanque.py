import pygame
import sys
import math
import random
from Tanque.Proyectil import *

class Tanque():


    def __init__(self,modelo,color,vida):
        self.vivo = True
        self.modelo = "Default"
        self.color = color

        self.jugador_size = 50
        self.jugador_pos = [random.randint(0,426), 470]

        self.enemigo_size = 50
        self.enemigo_pos = [random.randint(800,1230), 470]


    def mostrarInformacion(self):
        return "vivo:"+str(self.vivo)+" | modelo: "+str(self.modelo)





import pygame
from utilidades.Boton import Boton

class CajaTexto(Boton):
    def __init__(self,pantalla, texto, posX, posY,imagenBoton, x,y):
        Boton.__init__(self,pantalla, texto, posX, posY,imagenBoton, x,y)
        self.flag = False
        self.texto = ""


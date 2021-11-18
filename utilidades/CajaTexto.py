import pygame
from utilidades.Boton import Boton

class CajaTexto(Boton):
    def __init__(self,pantalla, texto, posX, posY,imagenBoton, x,y):
        Boton.__init__(self,pantalla, texto, posX, posY,imagenBoton, x,y)
        self.flag = False
        self.texto = ""

    def acapturaTexto(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:

                self.textoC = self.texto[:-1]
            else:
                tecla = event.unicode
                self.concadena(tecla)
                print('texto'+ self.textoC)
    def aflag(self, booleano):
        self.flagEscritura = booleano

    def aconcadena(self, tecla):
        self.textoC.join(tecla)
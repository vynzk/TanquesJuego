import pygame,sys
from pygame.locals import *
import pygame.font

FONDO = (32, 30, 32)
BLANCO = (255, 255, 255)
COLOR_TEXTO = (50, 60, 80)

class Boton:
    def __init__(self, pantalla,texto):
        self.pantalla = pantalla
        self.pantalla_rect= self.pantalla.get_rect()
        self.x, self.y = 200, 50
        self.color = (255,0,0)
        self.textoColor=(255,255,255)

        self.fuente= pygame.font.SysFont("arial",30)

        self.rect= pygame.Rect(0,0 ,self.x,self.y)
        self.rect.center= self.pantalla_rect.center

        self.preparaTexto(texto)

    def preparaTexto(self, texto):
        self.texto_image= self.fuente.render(texto,True, self.textoColor, self.color)
        self.texto_image_rect = self.texto_image.get_rect()
        self.texto_image_rect.center= self.rect.center
    def dibujaBoton(self):
        self.pantalla.fill(self.color,self.rect)
        self.pantalla.blit(self.texto_image,self.texto_image_rect)



#demostración: no borrar metodo por debug...

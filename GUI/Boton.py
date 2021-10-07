import pygame
import pygame.font
from GUI.colores import *

class Boton:
    def __init__(self, pantalla, texto, posX, posY):
        self.pantalla = pantalla
        self.pantalla_rect = self.pantalla.get_rect()
        self.imagenBase= pygame.image.load("GUI/imagenes/botones/botonVacio.png") #debe volverse atributo de entrada
        
        self.x, self.y = 120, 40
        self.posX = posX
        self.posY = posY
        #self.rect = imagen.get_rect()
        self.rect = pygame.Rect(self.posX, self.posY, self.x, self.y)
        
        self.color = ROJO
        self.redimensionarBoton()
        #self.textoColor = COLOR_TEXTO
        #self.fuente = pygame.font.SysFont("arial", 30)
        
        #self.rect.center = self.pantalla_rect.center
        #self.preparaTexto(texto, posX, posY)
    """
    def preparaTexto(self, texto, posX, posY):
        self.texto_image = self.fuente.render(texto, True, self.textoColor, self.color)
        self.texto_image_rect = posX, posY
        #self.texto_image_rect.center = self.rect.center
    """
    def dibujaBoton(self):
        #self.pantalla.fill(self.color, self.rect)
        #self.pantalla.blit(self.texto_image, self.texto_image_rect)
        self.pantalla.blit(self.imagenBase, self.rect)
    def redimensionarBoton(self):
        self.imagenBase=pygame.transform.scale(self.imagenBase, (self.x,self.y))


# -*- encoding: utf-8 -*-
import pygame
import time

class Escena:
    """Clase abstracta para construir las escenas del video juego"""

    def __init__(self, director):
        self.director = director
        #---para tener un fondo transparente en cualquier escena que sea hija---
        self.fondoTransparente = pygame.Surface((1280, 720)) # En el futuro  pygame.Surface((800, 800))
        self.fondoTransparente = self.fondoTransparente.convert_alpha()
        self.fondoTransparente.fill((0, 0, 0, 0))
    
    def on_update(self):
        "Actualización lógica que se llama automáticamente desde el director."
        raise NotImplemented("Tiene que implementar el método on_update.")

    def on_event(self, event):
        "Se llama cuando llega un evento especifico al bucle."
        raise NotImplemented("Tiene que implementar el método on_event.")

    def on_draw(self, screen):
        "Se llama cuando se quiere dibujar la pantalla."
        raise NotImplemented("Tiene que implementar el método on_draw.")

    def textoEnPantalla(self,texto,tamañoLetra,color,posicion,deseaPausa):
        fuente= pygame.font.Font("fuentes/font_pixel.ttf",tamañoLetra-5,bold=True)
        mensaje= fuente.render(texto,1,color)
        self.director.pantalla.blit(mensaje, (posicion[0],posicion[1]))
        # bug
        if deseaPausa is True:
            pygame.display.update()
            pygame.time.wait(250)

    def mostrarImagenEnPos(self,pathImagen,tamaño,posicion):
        imagen= pygame.transform.scale(pygame.image.load(pathImagen), (tamaño[0],tamaño[1]))
        self.director.pantalla.blit(imagen,(posicion[0],posicion[1]))

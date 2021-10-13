import pygame
from GUI import plantillaEscena
from GUI.Boton import Boton
#from GUI.director import Director
#from GUI.escenaHome import EscenaHome

class EscenaSeguro(plantillaEscena.Escena):
    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.boton_seguro = None

    def on_update(self):
        pygame.display.set_caption("Seguro que quieres reiniciar el juego?")

    def on_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_seguro):
                self.director.cambiarEscena(self.director.listaEscenas[1])

    def on_draw(self, pantalla):
        self.boton_seguro = Boton(pantalla, "cambiar", 540, 320)
        self.boton_seguro.dibujaBoton()
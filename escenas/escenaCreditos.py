import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton


class EscenaCreditos(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.director.listaEscenas["escenaCreditos"]=self;

        self.boton_salir = None
        self.fondo=  pygame.image.load("imagenes/fondoCreditos.png")
        

    def on_update(self):
        pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Creditos")
        

    def on_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_salir):
                print('(escenaCreditos) PRESIONA BOTON: presionaste el boton volver, te llevará a escenaJuego')
                self.vuelveJuego()

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):

        pantalla.blit(self.fondo, (0,0))
        botonSalir= pygame.image.load("imagenes/botones/botonVolver.png")
        self.boton_salir = Boton(pantalla, "volver", 1000, 620,botonSalir,127,40)
        self.boton_salir.dibujaBoton()


    def vuelveJuego(self):
        self.director.cambiarEscena(self.director.listaEscenas["escenaJuego"])
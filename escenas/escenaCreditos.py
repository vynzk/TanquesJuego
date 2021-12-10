import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton


class EscenaCreditos(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.director.listaEscenas["escenaCreditos"]=self;

        self.boton_salir = None
        self.fondo=  pygame.transform.scale(pygame.image.load("imagenes/fondoCreditos.png"),(self.director.ancho,self.director.alto))
        

    def on_update(self):
        pygame.display.set_mode((self.director.ancho,self.director.alto))
        pygame.display.set_caption("Creditos")  # no cambies esto aun... es para debuggueo
        

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
        self.boton_salir = Boton(pantalla, "volver", self.director.ancho/2 -50, self.director.alto/2+300,botonSalir,127,40)
        self.boton_salir.dibujaBoton()


    def vuelveJuego(self):
        self.director.cambiarEscena(self.director.listaEscenas["escenaJuego"])
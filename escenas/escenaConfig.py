import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton
from utilidades.colores import *

class EscenaConfig(plantillaEscena.Escena):

    def __init__(self, director):
        plantillaEscena.Escena.__init__(self, director)
        self.director = director
        self.fondo= pygame.image.load("imagenes/fondoHome.png")
        # botones
        self.boton_aplicar = None
        self.boton_restablecer = None
        self.boton_numJugadores = None
        self.boton_numIa = None
        self.boton_afectosEntorno = None
        self.boton_dimensionPantalla = None
            #cant muiniciones
        self.boton_perforante = None
        self.boton_105mm = None
        self.boton_60mm = None

    
    def on_update(self):
        pygame.display.set_caption("configuraciones")

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_aplicar):
                print('ok')
            if self.director.checaBoton(self.director.mousePos, self.boton_restablecer):
                print('ok')       
        

    def on_draw(self, pantalla):
        botonVacio= pygame.image.load("imagenes/botones/botonVacio.png")

        pantalla.blit(self.fondo, (0,0))
        
        
        self.boton_aplicar = Boton(pantalla, "play", 64, 420,botonVacio,40,40)
        self.boton_aplicar.dibujaBoton()

        self.boton_restablecer = Boton(pantalla, "play", 1200, 420,botonVacio,40,40)
        self.boton_restablecer.dibujaBoton()

        self.textoEnPantalla(f' cantidad de jugadores',15,BLANCO,(114,150),False)
        self.boton_numJugadores= Boton(pantalla, "play", 64, 150,botonVacio,40,40)
        self.boton_numJugadores.dibujaBoton()

        self.textoEnPantalla(f' cantidad de jugadores IA',15,BLANCO,(114,200),False)
        self.boton_numIa = Boton(pantalla, "play", 64, 200,botonVacio,40,40)
        self.boton_numIa.dibujaBoton()

        self.textoEnPantalla(f' efectos de entorno?',15,BLANCO,(114,250),False)
        self.boton_afectosEntorno = Boton(pantalla, "play", 64, 250,botonVacio,40,40)
        self.boton_afectosEntorno.dibujaBoton()

        self.textoEnPantalla(f' dimension de pantalla',15,BLANCO,(214,300),False)
        self.boton_dimensionPantalla = Boton(pantalla, "play", 64, 300,botonVacio,127,40)
        self.boton_dimensionPantalla.dibujaBoton()
        #municion
        self.textoEnPantalla(f' Proyectil Perforante',15,BLANCO,(950,150),False)
        self.boton_perforante = Boton(pantalla, "play", 900, 150,botonVacio,40,40)
        self.boton_perforante.dibujaBoton()   

        self.boton_105mm = Boton(pantalla, "play", 900, 200,botonVacio,40,40)
        self.boton_105mm.dibujaBoton()  

        self.boton_60mm = Boton(pantalla, "play", 900, 250,botonVacio,40,40)
        self.boton_60mm.dibujaBoton()       

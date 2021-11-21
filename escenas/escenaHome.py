from Videojuego.Juego import Juego
from escenas.escenaRegistro import EscenaRegistro
from escenas.escenaConfig import EscenaConfig
import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton
from utilidades.colores import *
from escenas.escenaConfig import *
from escenas.escenaJuego import *
import escenas.escenaHome

class EscenaHome(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.director.listaEscenas["escenaHome"]=self;

        self.boton_play = None
        self.boton_config = None
        self.fondo = pygame.image.load("imagenes/fondoHome.png")

        # valores predeterminados
        self.numJugadores= 2
        self.afectosEntorno = 'no'
        self.dimensionPantalla = (800,800)
        self.perforante = 10
        self.p105mm= 10
        self.p60mm= 10

            #los efectos de entorno
        self.viento = 0
        self.gravedad = 9.8
        self.viento_o_no = False


    def on_update(self):
        pygame.display.set_caption("Home")  # no cambies esto aun... es para debuggueo


    def on_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_play):
                self.cambiaDePartida()
            # verifica si el boton de configuración fue seleccionado
            if self.director.checaBoton(self.director.mousePos, self.boton_config): 
                self.cambiaConfiguracion() 


    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        botonJugar = pygame.image.load("imagenes/botones/botonJugar.png")
        botonAjustes = pygame.image.load("imagenes/botones/botonAjustes.png")
        self.boton_play = Boton(pantalla, "play", self.director.ancho/2, self.director.alto/2, botonJugar, 127, 40)
        self.boton_play.dibujaBoton()
        self.boton_config = Boton(pantalla, "configuracion", self.director.ancho/2, self.director.alto/2+50,botonAjustes,127,40)
        self.boton_config.dibujaBoton() 

    def cambiaDePartida(self):
        game=Juego(self.numJugadores,1)
        self.director.game=game
        self.director.cambiarEscena(EscenaRegistro(self.director))

    def cambiaConfiguracion(self): 
        self.director.cambiarEscena(EscenaConfig(self.director)) 


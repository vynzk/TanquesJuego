import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton
from utilidades.CajaTexto import CajaTexto
from utilidades.colores import *
import random

class EscenaConfig(plantillaEscena.Escena):

    def __init__(self, director):
        plantillaEscena.Escena.__init__(self, director)
        self.director = director
        self.fondo= pygame.image.load("imagenes/fondoHome.png")
        # botones
        self.boton_aplicar = None
        self.boton_restablecer = None
        self.boton_numJugadores = None
        self.boton_afectosEntorno = None
        self.boton_dimensionPantalla = None
            #cant muiniciones
        self.boton_perforante = None
        self.boton_105mm = None
        self.boton_60mm = None

        # valores predeterminados
        self.numJugadores= 2
        self.afectosEntorno = 'no'
        self.dimensionPantalla = (800,800)
        self.perforante = 10
        self.p105mm= 10
        self.p60mm= 10
            #parametros que almacenan los efectos de entorno
        self.viento = 0
        self.viento_o_no = False
        self.indicarClima = "Desactivado"

    
    def on_update(self):
        pygame.display.set_caption("configuraciones")

    def on_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_aplicar):
                self.registrar()
                self.cambiarEscenaHome()
                print('presiona aplicado')
            if self.director.checaBoton(self.director.mousePos, self.boton_restablecer):
                self.restablecer()
                print('presiona restablecer predeterminado')
            if self.director.checaBoton(self.director.mousePos, self.boton_numJugadores):
                if(self.numJugadores >= 6 or self.numJugadores <=1):
                    self.numJugadores = 2
                else:
                    self.numJugadores += 1
            if self.director.checaBoton(self.director.mousePos, self.boton_afectosEntorno):
                if(self.afectosEntorno=='no'):
                    self.afectosEntorno = 'si'
                else:
                    self.afectosEntorno = 'no'
            if self.director.checaBoton(self.director.mousePos, self.boton_perforante):
                if(self.perforante == 30):
                    self.p60mm = 10
                else:
                    self.perforante += 1
            if self.director.checaBoton(self.director.mousePos, self.boton_105mm):
                if(self.p105mm == 30):
                    self.p105mm = 10
                else:
                    self.p105mm += 1
            if self.director.checaBoton(self.director.mousePos, self.boton_60mm):
                if(self.p60mm == 30):
                    self.p60mm = 10
                else:
                    self.p60mm += 1

        
        """
        # al escribir, solo se toman en cuenta los números (intenté hacerlo enn un solo if, pero no me funcionó de ninguna forma)
        if event.type == pygame.KEYDOWN:
            #if event.key == (pygame.K_0) or (pygame.K_1) or (pygame.K_2) or (pygame.K_3) or (pygame.K_4) or (pygame.K_5) or (pygame.K_6) or (pygame.K_7) or (pygame.K_8) or (pygame.K_9)=):
            if event.key == pygame.K_0:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_1:
                self.texto_usuario += event.unicode
            
            elif event.key == pygame.K_2:
                self.texto_usuario += event.unicode
            
            elif event.key == pygame.K_3:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_4:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_5:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_6:
                self.texto_usuario += event.unicode
            
            elif event.key == pygame.K_7:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_8:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_9:
                self.texto_usuario += event.unicode
            
            elif event.key == pygame.K_BACKSPACE:
                self.texto_usuario = self.texto_usuario[:-1]   
        """

    def on_draw(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        self.textoEnPantalla(f'click derecho ++     click izquierdo --', 15, ROJO, (500, 650), False)
        #BotonesImagenes
        botonVacio= pygame.image.load("imagenes/botones/botonVacio.png")
        botonRegistrar = pygame.image.load("imagenes/botones/botonRegistrar.png")
        botonRestablecer = pygame.image.load("imagenes/botones/botonReiniciar.png")

        #botones implementados
        self.boton_aplicar = Boton(pantalla, "play", 64, 420,botonRegistrar,127,40)
        self.boton_aplicar.dibujaBoton()


        self.boton_restablecer = Boton(pantalla, "play", 1200, 420,botonRestablecer,40,40)
        self.boton_restablecer.dibujaBoton()

        self.textoEnPantalla(f' cantidad de jugadores',15,BLANCO,(114,150),False)
        self.boton_numJugadores= Boton(pantalla, "play", 64, 150,botonVacio,40,40)
        self.boton_numJugadores.dibujaBoton()
        self.textoEnPantalla(f'{self.numJugadores}', 15, NEGRO, (80, 150), False)
        """
        self.textoEnPantalla(f' cantidad de jugadores IA',15,BLANCO,(114,200),False)
        self.boton_numIa = Boton(pantalla, "play", 64, 200,botonVacio,40,40)
        self.boton_numIa.dibujaBoton()
        self.textoEnPantalla(f'{self.numIa}', 15, NEGRO, (80, 200), False)
        """
        self.textoEnPantalla(f' efectos de entorno?',15,BLANCO,(114,200),False)
        self.boton_afectosEntorno = Boton(pantalla, "play", 64, 200,botonVacio,40,40)
        self.boton_afectosEntorno.dibujaBoton()
        self.textoEnPantalla(f'{self.afectosEntorno}', 15, NEGRO, (80, 200), False)

        self.textoEnPantalla(f' dimension de pantalla',15,BLANCO,(214,250),False)
        self.boton_dimensionPantalla = Boton(pantalla, "play", 64, 250,botonVacio,127,40)
        self.boton_dimensionPantalla.dibujaBoton()
        self.textoEnPantalla(f'{self.dimensionPantalla[0]} x {self.dimensionPantalla[1]} ', 15, NEGRO, (80, 250), False)
        #municion
        self.textoEnPantalla(f' Proyectil Perforante',15,BLANCO,(950,150),False)
        self.boton_perforante = Boton(pantalla, "play", 900, 150,botonVacio,40,40)
        self.boton_perforante.dibujaBoton()
        self.textoEnPantalla(f'{self.perforante}', 15, NEGRO, (915, 150), False)

        self.textoEnPantalla(f' Proyectil 105mm',15,BLANCO,(950,200),False)
        self.boton_105mm = Boton(pantalla, "play", 900, 200,botonVacio,40,40)
        self.boton_105mm.dibujaBoton()
        self.textoEnPantalla(f'{self.p105mm}', 15, NEGRO, (915, 200), False)

        self.textoEnPantalla(f' Proyectil 60mm',15,BLANCO,(950,250),False)
        self.boton_60mm = Boton(pantalla, "play", 900, 250,botonVacio,40,40)
        self.boton_60mm.dibujaBoton()
        self.textoEnPantalla(f'{self.p60mm}', 15, NEGRO, (915, 250), False)


    def registrar(self):
        # valores predeterminados
        self.director.listaEscenas["escenaHome"].numJugadores=  self.numJugadores
        self.director.listaEscenas["escenaHome"].afectosEntorno = self.afectosEntorno
        self.director.listaEscenas["escenaHome"].dimensionPantalla = self.dimensionPantalla
        self.director.listaEscenas["escenaHome"].perforante = self.perforante
        self.director.listaEscenas["escenaHome"].p105mm=self.p105mm
        self.director.listaEscenas["escenaHome"].p60mm=self.p60mm
            #parametros que almacenan los efectos de entorno
        self.director.listaEscenas["escenaHome"].viento = self.viento
        self.director.listaEscenas["escenaHome"].viento_o_no = self.viento_o_no
        self.director.listaEscenas["escenaHome"].indicarClima = self.indicarClima

        #provisional
        self.director.cambiarResolucion(self.dimensionPantalla[0],self.dimensionPantalla[1])
    def redefinirViento(self):
        if self.viento_o_no == False:
            self.viento = random.randint(-10,10)
            self.viento_o_no = True
            self.indicarClima = "Activado"

        elif self.viento_o_no == True:
            self.viento = 0
            self.viento_o_no = False
            self.indicarClima = "Desactivado"

        self.director.listaEscenas["escenaHome"].viento_o_no = self.viento_o_no
        self.director.listaEscenas["escenaHome"].viento = self.viento
        print("viento:",self.viento)
    def restablecer(self):
        self.viento = 0
        #cuando se presiona el botón de reestablecer se restablece el viento (por ahora)
        self.director.listaEscenas["escenaHome"].viento = self.viento
        self.viento_o_no = False
        print("viento:",self.viento)
        self.indicarClima = "Desactivado"

        # valores predeterminados
        self.numJugadores= 2
        self.afectosEntorno = 'no'
        self.dimensionPantalla = (1280,720)
        self.perforante = 10
        self.p105mm= 10
        self.p60mm= 10


            
            #elif event.key == pygame.K_PERIOD:
            #    self.texto_usuario += event.unicode
    def cambiarEscenaHome(self):
        self.director.cambiarEscena(self.director.listaEscenas["escenaHome"])
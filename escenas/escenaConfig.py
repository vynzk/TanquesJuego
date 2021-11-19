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

        # cajas: corresponden a las cajas de introduccion de texto
        self.cajaDimensionX = CajaTexto(self.director.pantalla,"caja",60,250, cajaImagen, 60,40)
        self.cajaDimensionX_valor = 1280
        self.cajaDimensionY = CajaTexto(self.director.pantalla,"caja",150,250, cajaImagen, 60,40)
        self.cajaDimensionY_valor = 720
        self.cajaPerforante = CajaTexto(self.director.pantalla,"caja",900,150, cajaImagen, 40,40)
        self.cajaPerforante_valor = 10
        self.caja100mm = CajaTexto(self.director.pantalla,"caja",900,200, cajaImagen, 40,40)
        self.caja100mm_valor = 10
        self.caja60mm = CajaTexto(self.director.pantalla,"caja",900,250, cajaImagen, 40,40)
        self.caja60mm_valor = 10

        # botones
        self.boton_aplicar = None
        self.boton_restablecer = None
        self.boton_numJugadores = None
        self.boton_afectosEntorno = None

        # valores predeterminados
        self.numJugadores= 2
        self.afectosEntorno = 'no'
        self.dimensionPantalla = (self.cajaDimensionX_valor,self.cajaDimensionY_valor)
        self.perforante = self.cajaPerforante_valor
        self.p105mm= self.caja100mm_valor
        self.p60mm= self.caja60mm_valor
            #parametros que almacenan los efectos de entorno
        self.viento = 0
        self.viento_o_no = False
        self.indicarClima = "Desactivado"

    
    def on_update(self):
        self.director.pantalla.blit(self.fondo, (0, 0))
        pygame.display.set_caption("configuraciones")


    def on_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_aplicar):
                if self.compruebaValores():
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

            if self.director.checaBoton(self.director.mousePos, self.caja):
                self.cajaDimensionX.flag = False
                self.cajaDimensionY.flag = False
                self.caja.flag = True
                self.cajaPerforante.flag = False
                self.caja100mm.flag = False
                self.caja60mm.flag = False
            if self.director.checaBoton(self.director.mousePos, self.cajaDimensionX):
                self.caja.flag = False
                self.cajaDimensionY.flag = False
                self.cajaDimensionX.flag = True
                self.cajaPerforante.flag = False
                self.caja100mm.flag = False
                self.caja60mm.flag = False
            if self.director.checaBoton(self.director.mousePos, self.cajaDimensionY):
                self.caja.flag = False
                self.cajaDimensionX.flag = False
                self.cajaDimensionY.flag = True
                self.cajaPerforante.flag = False
                self.caja100mm.flag = False
                self.caja60mm.flag = False
            if self.director.checaBoton(self.director.mousePos, self.cajaPerforante):
                self.caja.flag = False
                self.cajaDimensionX.flag = False
                self.cajaDimensionY.flag = False
                self.cajaPerforante.flag = True
                self.caja100mm.flag = False
                self.caja60mm.flag = False
            if self.director.checaBoton(self.director.mousePos, self.caja100mm):
                self.caja.flag = False
                self.cajaDimensionX.flag = False
                self.cajaDimensionY.flag = False
                self.cajaPerforante.flag = False
                self.caja100mm.flag = True
                self.caja60mm.flag = False
            if self.director.checaBoton(self.director.mousePos, self.caja60mm):
                self.caja.flag = False
                self.cajaDimensionX.flag = False
                self.cajaDimensionY.flag = False
                self.cajaPerforante.flag = False
                self.caja100mm.flag = False
                self.caja60mm.flag = True
        #flags de las cajas: habilitan la escritura de una caja desactivando las otras
        if self.caja.flag:
            try:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.caja.texto = self.caja.texto[:-1]
                    else:
                        self.caja.texto += event.unicode
                        self.caja_valor = int(self.caja.texto)
            except:
                self.caja.texto = self.caja.texto[:-1]
        if self.cajaDimensionX.flag:
            try:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.cajaDimensionX.texto = self.cajaDimensionX.texto[:-1]
                    else:
                        self.cajaDimensionX.texto += event.unicode
                        self.cajaDimensionX_valor = int(self.cajaDimensionX.texto)
            except:
                self.cajaDimensionX.texto = self.cajaDimensionX.texto[:-1]
        if self.cajaDimensionY.flag:
            try:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.cajaDimensionY.texto = self.cajaDimensionY.texto[:-1]
                    else:
                        self.cajaDimensionY.texto += event.unicode
                        self.cajaDimensionY_valor = int(self.cajaDimensionY.texto)
            except:
                self.cajaDimensionY.texto = self.cajaDimensionY.texto[:-1]
        if self.cajaPerforante.flag:
            try:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.cajaPerforante.texto = self.cajaPerforante.texto[:-1]
                    else:
                        self.cajaPerforante.texto += event.unicode
                        self.cajaPerforante_valor = int(self.cajaPerforante.texto)
            except:
                self.cajaDimensionY.texto = self.cajaDimensionY.texto[:-1]
        if self.caja100mm.flag:
            try:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.caja100mm.texto = self.caja100mm.texto[:-1]
                    else:
                        self.caja100mm.texto += event.unicode
                        self.caja100mm_valor = int(self.caja100mm.texto)
            except:
                self.caja100mm.texto = self.caja100mm.texto[:-1]
        if self.caja60mm.flag:
            try:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.caja60mm.texto = self.caja60mm.texto[:-1]
                    else:
                        self.caja60mm.texto += event.unicode
                        self.caja60mm_valor = int(self.caja60mm.texto)
            except:
                self.caja60mm.texto = self.caja60mm.texto[:-1]

    def on_draw(self, pantalla):

        self.textoEnPantalla(f'         click derecho: ++/escribir', 15, ROJO, (500, 650), False)

        self.caja.dibujaBoton()
        self.textoEnPantalla(f'{self.caja.texto}', 15, NEGRO, (self.caja.posX+10, self.caja.posY+10), False)

        self.cajaDimensionX.dibujaBoton()
        self.textoEnPantalla(f'{self.cajaDimensionX.texto}', 15, NEGRO, (self.cajaDimensionX.posX+5, self.cajaDimensionX.posY+5), False)

        self.cajaDimensionY.dibujaBoton()
        self.textoEnPantalla(f'{self.cajaDimensionY.texto}', 15, NEGRO,(self.cajaDimensionY.posX+5, self.cajaDimensionY.posY+5), False)
        self.textoEnPantalla(f'X', 20, BLANCO,(self.cajaDimensionX.posX+67, self.cajaDimensionX.posY), False)
        self.textoEnPantalla(f' dimension de pantalla', 15, BLANCO, (214, 250), False)

        self.cajaPerforante.dibujaBoton()
        self.textoEnPantalla(f'{self.cajaPerforante.texto}', 15, NEGRO, (self.cajaPerforante.posX+5, self.cajaPerforante.posY+5), False)
        self.textoEnPantalla(f' Proyectil Perforante', 15, BLANCO, (950, 150), False)

        self.caja100mm.dibujaBoton()
        self.textoEnPantalla(f'{self.caja100mm.texto}', 15, NEGRO, (self.caja100mm.posX+5, self.caja100mm.posY+5), False)
        self.textoEnPantalla(f' Proyectil 100mm', 15, BLANCO, (950, 200), False)

        self.caja60mm.dibujaBoton()
        self.textoEnPantalla(f'{self.caja60mm.texto}', 15, NEGRO, (self.caja60mm.posX+5, self.caja60mm.posY+5), False)
        self.textoEnPantalla(f' Proyectil 60mm', 15, BLANCO, (950, 250), False)

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

        self.textoEnPantalla(f' efectos de entorno?',15,BLANCO,(114,200),False)
        self.boton_afectosEntorno = Boton(pantalla, "play", 64, 200,botonVacio,40,40)
        self.boton_afectosEntorno.dibujaBoton()
        self.textoEnPantalla(f'{self.afectosEntorno}', 15, NEGRO, (80, 200), False)
    def registrar(self):
        # valores predeterminados
        self.dimensionPantalla = (self.cajaDimensionX_valor,self.cajaDimensionY_valor)
        self.perforante = self.cajaPerforante_valor
        self.p105mm= self.caja100mm_valor
        self.p60mm= self.caja60mm_valor

        # valores
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
        self.cajaDimensionY.texto = "800"
        self.cajaDimensionX.texto = "800"
        self.cajaPerforante.texto = "10"
        self.caja100mm.texto= "10"
        self.caja60mm.texto= "10"

        self.cajaDimensionY_valor = 800
        self.cajaDimensionX_valor = 800
        self.cajaPerforante_valor = 10
        self.caja100mm_valor= 10
        self.caja60m_valoro= 10


        self.dimensionPantalla = (self.cajaDimensionX_valor, self.cajaDimensionY_valor)
        self.perforante =self.cajaPerforante_valor
        self.p105mm=self.caja100mm_valor
        self.p60mm=self.caja60mm_valor


    def cambiarEscenaHome(self):
        self.director.cambiarEscena(self.director.listaEscenas["escenaHome"])
    def compruebaValores(self):
        #sirve para verificar si los datos ingresados estan correctos
        if self.cajaDimensionX_valor > 2000 or self.cajaDimensionY_valor > 2000: #ejemplo de resolucion
            self.textoEnPantalla("Valores ingresados no son correctos",15,AZUL,(500,610),True)
            return False
        if self.cajaPerforante_valor > 100 or self.cajaPerforante_valor < 10:
            self.textoEnPantalla("Valores ingresados no son correctos",15,AZUL,(500,610),True)
            return False
        if self.caja100mm_valor > 30 or self.caja100mm_valor < 10:
            self.textoEnPantalla("Valores ingresados no son correctos",15,AZUL,(500,610),True)
            return False
        if self.caja60mm_valor > 100 or self.caja60mm_valor < 10:
            self.textoEnPantalla("Valores ingresados no son correctos",15,AZUL,(500,610),True)
            return False
        else:
            return True


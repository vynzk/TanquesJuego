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
        cajaImagen = pygame.image.load("imagenes/botones/botonVacio.png")
        self.cajaDimensionX = CajaTexto(self.director.pantalla,"caja",60,250, cajaImagen, 60,40)
        self.cajaDimensionX_valor = 1280
        self.cajaDimensionY = CajaTexto(self.director.pantalla,"caja",150,250, cajaImagen, 60,40)
        self.cajaDimensionY_valor = 720
        self.cajaPerforante = CajaTexto(self.director.pantalla,"caja",self.director.ancho-380,150, cajaImagen, 40,40)
        self.cajaPerforante_valor = 10
        self.caja100mm = CajaTexto(self.director.pantalla,"caja",self.director.ancho-380,200, cajaImagen, 40,40)
        self.caja100mm_valor = 10
        self.caja60mm = CajaTexto(self.director.pantalla,"caja",self.director.ancho-380,250, cajaImagen, 40,40)
        self.caja60mm_valor = 10
        self.cajaGravedad = CajaTexto(self.director.pantalla, "caja", 60,300, cajaImagen, 60,40)
        self.cajaGravedad_valor = 9.8

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
        self.gravedad= self.cajaGravedad_valor

        #parametros que almacenan los efectos de entorno
        
        self.viento = 0
        self.viento_o_no = False
        self.indicarClima = "Desactivado"

    
    def on_update(self):
        pygame.display.set_mode(self.director.listaEscenas["escenaHome"].dimensionPantalla)
        self.director.pantalla.blit(self.fondo, (0, 0))
        pygame.display.set_caption("configuraciones")


    def on_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_aplicar):
                if self.compruebaValores():
                    self.registrar()
                    self.cambiarEscenaHome()
                    print('(escenaConfig) PRESION BOTON: presionó el botón aplicado')
            if self.director.checaBoton(self.director.mousePos, self.boton_restablecer):
                self.restablecer()
                print('(escenaConfig) PRESION BOTON: presionó restablecer predeterminado')
            if self.director.checaBoton(self.director.mousePos, self.boton_numJugadores):
                if(self.numJugadores >= 6 or self.numJugadores <=1):
                    self.numJugadores = 2
                else:
                    self.numJugadores += 1
            if self.director.checaBoton(self.director.mousePos, self.boton_afectosEntorno):
                if(self.afectosEntorno=='no'):
                    self.redefinirViento()
                    self.afectosEntorno = 'si'
                else:
                    self.afectosEntorno = 'no'
            if self.director.checaBoton(self.director.mousePos, self.cajaDimensionX):
                self.cajaDimensionY.flag = False
                self.cajaDimensionX.flag = True
                self.cajaPerforante.flag = False
                self.caja100mm.flag = False
                self.caja60mm.flag = False
                self.cajaGravedad.flag = False
            if self.director.checaBoton(self.director.mousePos, self.cajaDimensionY):
                self.cajaDimensionX.flag = False
                self.cajaDimensionY.flag = True
                self.cajaPerforante.flag = False
                self.caja100mm.flag = False
                self.caja60mm.flag = False
                self.cajaGravedad.flag = False
            if self.director.checaBoton(self.director.mousePos, self.cajaPerforante):
                self.cajaDimensionX.flag = False
                self.cajaDimensionY.flag = False
                self.cajaPerforante.flag = True
                self.caja100mm.flag = False
                self.caja60mm.flag = False
                self.cajaGravedad.flag = False
            if self.director.checaBoton(self.director.mousePos, self.caja100mm):
                self.cajaDimensionX.flag = False
                self.cajaDimensionY.flag = False
                self.cajaPerforante.flag = False
                self.caja100mm.flag = True
                self.caja60mm.flag = False
                self.cajaGravedad.flag = False
            if self.director.checaBoton(self.director.mousePos, self.caja60mm):
                self.cajaDimensionX.flag = False
                self.cajaDimensionY.flag = False
                self.cajaPerforante.flag = False
                self.caja100mm.flag = False
                self.caja60mm.flag = True
                self.cajaGravedad.flag = False
            if self.director.checaBoton(self.director.mousePos, self.cajaGravedad):
                self.cajaDimensionX.flag = False
                self.cajaDimensionY.flag = False
                self.cajaPerforante.flag = False
                self.caja100mm.flag = False
                self.caja60mm.flag = False
                self.cajaGravedad.flag = True
        #flags de las cajas: habilitan la escritura de una caja desactivando las otras
        if self.cajaDimensionX.flag:
            try:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.cajaDimensionX.texto = self.cajaDimensionX.texto[:-1]
                        self.cajaDimensionX_valor = int(self.cajaDimensionX.texto)
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
                        self.cajaDimensionY_valor = int(self.cajaDimensionY.texto)
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
                        self.cajaPerforante_valor = int(self.cajaPerforante.texto)
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
                        self.caja100mm_valor = int(self.caja100mm.texto)
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
                        self.caja60mm_valor = int(self.caja60mm.texto)
                    else:
                        self.caja60mm.texto += event.unicode
                        self.caja60mm_valor = int(self.caja60mm.texto)
            except:
                self.caja60mm.texto = self.caja60mm.texto[:-1]
        if self.cajaGravedad.flag:
            try:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.cajaGravedad.texto = self.cajaGravedad.texto[:-1]
                        self.cajaGravedad_valor = float(self.cajaGravedad.texto)
                    else:
                        self.cajaGravedad.texto += event.unicode
                        self.cajaGravedad_valor = float(self.cajaGravedad.texto)
            except:
                self.cajaGravedad.texto = self.cajaGravedad.texto[:-1]

    def on_draw(self, pantalla):

        self.textoEnPantalla(f'         click izquierdo: ++/escribir', 15, ROJO, (self.director.ancho/3, self.director.alto-30), False)
        self.textoEnPantalla(f'----------------------------------------------------------------------------------------------------------------------', 15, BLANCO, (15, 480), False)
        self.textoEnPantalla(f'  INFORMACION LIMITES DEL JUEGO', 13, ROJO, (self.director.ancho/5, 500), False)
        self.textoEnPantalla(f'- Dimensión de la pantalla: Maxima[1600, 1600], Minina[800, 800], Multiplos de 40', 13, BLANCO, (20, 540), False)
        self.textoEnPantalla(f'- Cantidad de jugadores: 6 max', 13, BLANCO, (20, 560), False)
        self.textoEnPantalla(f'- Gravedad: Maxima = 50, Minima = 1', 13, BLANCO, (20, 580), False)
        self.textoEnPantalla(f'- Proyectil perforante: MaxBalas = 100, MinBalas = 10', 13, BLANCO, (20, 600), False)
        self.textoEnPantalla(f'- Proyectil 100mm: MaxBalas = 30, MinBalas = 10', 13, BLANCO, (20, 620), False)
        self.textoEnPantalla(f'- Proyectil 60mm: MaxBalas = 30, MinBalas = 10', 13, BLANCO, (20, 640), False)
        self.textoEnPantalla(f'----------------------------------------------------------------------------------------------------------------------', 15, BLANCO, (15, 660), False)

        self.cajaDimensionX.dibujaBoton()
        self.textoEnPantalla(f'{self.cajaDimensionX.texto}', 15, NEGRO, (self.cajaDimensionX.posX+5, self.cajaDimensionX.posY+5), False)

        self.cajaDimensionY.dibujaBoton()
        self.textoEnPantalla(f'{self.cajaDimensionY.texto}', 15, NEGRO,(self.cajaDimensionY.posX+5, self.cajaDimensionY.posY+5), False)
        self.textoEnPantalla(f'X', 20, BLANCO,(self.cajaDimensionX.posX+67, self.cajaDimensionX.posY), False)
        self.textoEnPantalla(f' dimension de pantalla', 15, BLANCO, (214, 250), False)

        self.cajaPerforante.dibujaBoton()
        self.textoEnPantalla(f'{self.cajaPerforante.texto}', 15, NEGRO, (self.cajaPerforante.posX+5, self.cajaPerforante.posY+5), False)
        self.textoEnPantalla(f' Proyectil Perforante', 15, BLANCO, (self.director.ancho-330, 150), False)

        self.caja100mm.dibujaBoton()
        self.textoEnPantalla(f'{self.caja100mm.texto}', 15, NEGRO, (self.caja100mm.posX+5, self.caja100mm.posY+5), False)
        self.textoEnPantalla(f' Proyectil 100mm', 15, BLANCO, (self.director.ancho-330, 200), False)

        self.caja60mm.dibujaBoton()
        self.textoEnPantalla(f'{self.caja60mm.texto}', 15, NEGRO, (self.caja60mm.posX+5, self.caja60mm.posY+5), False)
        self.textoEnPantalla(f' Proyectil 60mm', 15, BLANCO, (self.director.ancho-330, 250), False)

        self.cajaGravedad.dibujaBoton()
        self.textoEnPantalla(f'{self.cajaGravedad.texto}', 15, NEGRO, (self.cajaGravedad.posX+5, self.cajaGravedad.posY+5), False)
        self.textoEnPantalla(f' Gravedad', 15, BLANCO, (124, 300), False)

        #BotonesImagenes
        botonVacio= pygame.image.load("imagenes/botones/botonVacio.png")
        botonRegistrar = pygame.image.load("imagenes/botones/botonRegistrar.png")
        botonRestablecer = pygame.image.load("imagenes/botones/botonReiniciar.png")

        #botones implementados
        self.boton_aplicar = Boton(pantalla, "play", 64, 420,botonRegistrar,127,40)
        self.boton_aplicar.dibujaBoton()

        self.boton_restablecer = Boton(pantalla, "play", self.director.ancho-80, self.director.alto-380,botonRestablecer,40,40)
        self.boton_restablecer.dibujaBoton()

        self.textoEnPantalla(f' cantidad de jugadores',15,BLANCO,(114,150),False)
        self.boton_numJugadores= Boton(pantalla, "play", 64, 150,botonVacio,40,40)
        self.boton_numJugadores.dibujaBoton()
        self.textoEnPantalla(f'{self.numJugadores}', 15, NEGRO, (80, 150), False)

        self.textoEnPantalla(f' viento?',15,BLANCO,(114,200),False)
        self.boton_afectosEntorno = Boton(pantalla, "play", 64, 200,botonVacio,40,40)
        self.boton_afectosEntorno.dibujaBoton()
        self.textoEnPantalla(f'{self.afectosEntorno}', 15, NEGRO, (80, 200), False)

    def registrar(self):
        # valores predeterminados
        self.dimensionPantalla = (self.cajaDimensionX_valor,self.cajaDimensionY_valor)
        self.perforante = self.cajaPerforante_valor
        self.p105mm= self.caja100mm_valor
        self.p60mm= self.caja60mm_valor
        self.gravedad= self.cajaGravedad_valor

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
        self.director.listaEscenas["escenaHome"].gravedad = self.gravedad

        self.director.cambiarResolucion(self.dimensionPantalla[0],self.dimensionPantalla[1])

        self.director.listaEscenas["escenaHome"].mostrarInformacionTerminal()

    def redefinirViento(self):
        if self.viento_o_no == False:
            self.viento = random.randint(-10,10)
            self.viento_o_no = True
            self.indicarClima = "Activado"

        elif self.viento_o_no == True:
            self.viento = 0
            self.viento_o_no = False
            self.indicarClima = "Desactivado"

    def restablecer(self):
        #cuando se presiona el botón de reestablecer se restablece el viento (por ahora)
        self.director.listaEscenas["escenaHome"].viento = self.viento
        self.viento_o_no = False
        self.indicarClima = "Desactivado"

        # valores predeterminados
        self.numJugadores= 2
        self.afectosEntorno = 'no'
        self.cajaDimensionY.texto = "800"
        self.cajaDimensionX.texto = "800"
        self.cajaPerforante.texto = "10"
        self.caja100mm.texto= "10"
        self.caja60mm.texto= "10"
        self.cajaGravedad.texto= "9.8"

        self.cajaDimensionY_valor = 800
        self.cajaDimensionX_valor = 800
        self.cajaPerforante_valor = 10
        self.caja100mm_valor= 10
        self.caja60m_valoro= 10
        self.cajaGravedad_valor= 9.8
        self.viento = 0

        self.dimensionPantalla = (self.cajaDimensionX_valor, self.cajaDimensionY_valor)
        self.perforante =self.cajaPerforante_valor
        self.p105mm=self.caja100mm_valor
        self.p60mm=self.caja60mm_valor
        self.gravedad=self.cajaGravedad_valor

    def cambiarEscenaHome(self):
        self.director.cambiarEscena(self.director.listaEscenas["escenaHome"])

    def compruebaValores(self):
        #sirve para verificar si los datos ingresados estan correctos
        if self.cajaGravedad_valor > 50 or self.cajaGravedad_valor < 1:
            self.textoEnPantalla("Valores ingresados no son correctos",15,AZUL,(500,610),True)
            return False
        if self.cajaDimensionX_valor<=600 or self.cajaDimensionX_valor>=1600 or self.cajaDimensionX_valor%40!=0: #ejemplo de resolucion
            self.textoEnPantalla("Valores ingresados en ancho no son correctos",15,AZUL,(500,610),True)
            return False
        if self.cajaDimensionY_valor<=600 or self.cajaDimensionY_valor>=1600 or self.cajaDimensionY_valor%40!=0: 
            self.textoEnPantalla("Valores ingresados en alto no son correctos",15,AZUL,(500,610),True)
            return False
        if self.cajaPerforante_valor > 100 or self.cajaPerforante_valor < 10:
            self.textoEnPantalla("Valores ingresados no son correctos",15,AZUL,(500,610),True)
            return False
        if self.caja100mm_valor > 30 or self.caja100mm_valor < 10:
            self.textoEnPantalla("Valores ingresados no son correctos",15,AZUL,(500,610),True)
            return False
        if self.caja60mm_valor > 30 or self.caja60mm_valor < 10:
            self.textoEnPantalla("Valores ingresados no son correctos",15,AZUL,(500,610),True)
            return False
        
        else:
            return True


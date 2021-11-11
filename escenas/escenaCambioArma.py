#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton
from utilidades.colores import *


class EscenaCambioArma(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.botonVolver = None
        self.botonAplicar = None
        self.listaPanelArmas = []
        self.jugadorActual = director.listaEscenas[3].jugadorActual  # pos 0 siempre debe corresponder a escena juego
        self.panel = pygame.image.load("imagenes/fondoVentana.png")
        self.redimensionarPanel(500, 500)
        self.cambioArmaFlag=False

    def on_update(self):
        pygame.display.set_caption("Cambio de armas")  # no cambies esto aun... es para debuggueo

    def on_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.botonVolver):
                self.vuelveJuego()

            for i in range(len(self.jugadorActual.tanque.listaProyectiles)):
                if self.director.checaBoton(self.director.mousePos, self.listaPanelArmas[i]):
                    self.jugadorActual.tanque.cambiarArma(i)
                    self.cambioArmaFlag= True
                    


    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        pantalla.blit(self.fondoTransparente, (0, 0))
        pantalla.blit(self.panel, (390, 80))

        # imagenes -- botones
        volver = pygame.image.load("imagenes/botones/botonVolver.png")

        panelArma = pygame.image.load("imagenes/panelSeleccionArmas.png")

        self.botonVolver = Boton(pantalla, "volver", 580, 500, volver, 127, 40)
        self.botonVolver.dibujaBoton()

        # esto dibuja los paneles por cada arma en listaArmas
        posPanel = 210  # posicion 'y' del panel
        yPanel = 60  # dimension 'x' del panel
        i = 0

        # crea los objetos boton del panel y los agrega a la lista de paneles

        while i < len(self.jugadorActual.tanque.listaProyectiles):
            panel = Boton(pantalla, "seleccion arma", 420, posPanel, panelArma, 300, yPanel)
            self.listaPanelArmas.append(panel)
            self.listaPanelArmas[i].dibujaBoton()
            balaImagen = self.jugadorActual.tanque.listaProyectiles[i].imagen

            balasCantidad = 'Daño: ' + str(self.jugadorActual.tanque.listaProyectiles[i].daño)
            balaNombre = self.jugadorActual.tanque.listaProyectiles[i].nombre

            balaNombreRender = self.textoRender(balaNombre, NEGRO)
            balasCantidadRender = self.textoRender(balasCantidad, NEGRO)

            pantalla.blit(balaImagen, (440, posPanel + 5))
            pantalla.blit(balaNombreRender, (500, posPanel + 10))
            pantalla.blit(balasCantidadRender, (750, posPanel + 10))

            posPanel += yPanel + 10
            i += 1
        if self.cambioArmaFlag:
            self.textoEnPantalla("Se a cambiado de arma exitosamente",15,ROJO,(450,450),True)
        
    def redimensionarPanel(self, x, y):
        self.panel = pygame.transform.scale(self.panel, (x, y))

    def vuelveJuego(self):
        juegoActual = self.director.listaEscenas[3]
        self.director.cambiarEscena(juegoActual)

    def textoRender(self, frase, color):
        fuente = pygame.font.Font("fuentes/fs-gravity.ttf", 25)  # fuente de texto

        texto = fuente.render(frase, 1, color)  # utimo parametro es el color... agregar despues a colores del juego
        return texto

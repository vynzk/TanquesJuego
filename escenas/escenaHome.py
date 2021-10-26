#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Videojuego.Juego import Juego
from escenas.escenaRegistro import EscenaRegistro
import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton
from utilidades.colores import *


class EscenaHome(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.boton_play = None
        self.boton_MasJug = None
        self.cantidadJugadores=2
        self.boton_MenosJug = None
        self.fondo = pygame.image.load("imagenes/fondoHome.png")

    def on_update(self):
        pygame.display.set_caption("Home")  # no cambies esto aun... es para debuggueo

    def on_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_play):
                self.cambiaDePartida()
            if self.director.checaBoton(self.director.mousePos, self.boton_MasJug):
                if(self.cantidadJugadores<6):
                    self.cantidadJugadores+=1
                else:
                    self.textoEnPantalla("El maximo de jugadores es 6",20,ROJO,(150,150),True)
            if self.director.checaBoton(self.director.mousePos, self.boton_MenosJug):
                if self.cantidadJugadores>2:
                    self.cantidadJugadores-=1
                else:
                    self.textoEnPantalla("El minimo de jugadores es 2",20,ROJO,(150,150),True)

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        self.textoEnPantalla(f'Cantidad jugadores: {self.cantidadJugadores}',20,BLANCO,(150,200),False)

        botonJugar = pygame.image.load("imagenes/botones/botonJugar.png")
        botonMasJug = pygame.image.load("imagenes/botones/botonAgregar.png")
        botonMenosJug = pygame.image.load("imagenes/botones/botonDisminuir.png")
        self.boton_play = Boton(pantalla, "play", 580, 500, botonJugar, 127, 40)
        self.boton_MasJug = Boton(pantalla, "Mas jugador", 150, 250, botonMasJug, 127,40)
        self.boton_MenosJug = Boton(pantalla, "Menos Jugador", 300, 250, botonMenosJug, 127,40)
        self.boton_play.dibujaBoton()
        self.boton_MasJug.dibujaBoton()
        self.boton_MenosJug.dibujaBoton()

    def cambiaDePartida(self):
        self.director.guardarEscena(self.director.escena)
        game=Juego(self.cantidadJugadores,1)
        self.director.game=game
        self.director.cambiarEscena(EscenaRegistro(self.director))

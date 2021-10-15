#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from GUI import plantillaEscena
from GUI.Boton import Boton
from GUI.escenaJuego import EscenaJuego


class EscenaRegistro(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.boton_registrar = None  # botón para cambiar a escenaJuego en la versión final
        self.fondo= pygame.image.load("GUI/imagenes/fondoRegistro.png")

    def on_update(self):
        pygame.display.set_caption("Registrar jugadores")
        pass

    def on_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_registrar):
                if self.registrar():
                    self.cambioEscenaJuego()
                # print("salta a escena juego") # debug

    def registrar(self):
        # se registran los jugadores
        if self.director.game.registroJugadores(self.director):
            # se registran las partidas
            if self.director.game.registroPartidas(self.director):
                return True  # el registro de ambos funcionó con exito
        return False  # ocurrió un error

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        pantalla.blit(self.fondo, (0,0))
        botonRegistrar= pygame.image.load("GUI/imagenes/botones/botonRegistrar.png")
        self.boton_registrar = Boton(pantalla, "comenzar", 540, 320,botonRegistrar,127,40)
        self.boton_registrar.dibujaBoton()

    def cambioEscenaJuego(self):
        # define las posiciones aleatorias de los jugadores dentro de cada partida
        for partida in self.director.game.listaPartidas:
            partida.generarPosicionesJug()
            partida.equiparArmasIniciales()
        juegoEscena = EscenaJuego(self.director)
        self.director.guardarEscena(juegoEscena)
        self.director.cambiarEscena(juegoEscena)
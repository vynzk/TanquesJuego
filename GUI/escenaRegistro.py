#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from GUI import plantillaEscena
from GUI.Boton import Boton
from GUI.escenaJuego import EscenaJuego
from Videojuego.Juego import Juego
from GUI.colores import*


class EscenaRegistro(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.boton_registrar = None  # botón para cambiar a escenaJuego en la versión final
        self.fondo= pygame.image.load("GUI/imagenes/fondoRegistro.png")

        self.listaJugadores = [] # se almacenan los nombres de los jugadores
        self.texto_usuario = '' # texto que se mostrará en pantalla al escribir
        self.base = pygame.font.Font(None, 32) # es el tamaño de las letras
        self.cuadroTexto = pygame.Rect(530, 520, 140, 32) # lugar donde se dibujará el cuadrado para ingresar los nombres de los jugadores
        self.variable = 0

    def on_update(self):
        pygame.display.set_caption("Registrar jugadores")
        pass

    def on_event(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                self.texto_usuario = self.texto_usuario[:-1]
            elif evento.key == pygame.K_TAB: # Si el usuario preciona TAB, se agraga un jugador con el texto que ingresó
                self.variable = self.variable+1
                self.listaJugadores.append(self.texto_usuario)
                print("Nombre del jugador", self.variable, "=", self.texto_usuario)
            else:
                self.texto_usuario += evento.unicode

        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_registrar): 
                self.registrar()
                self.cambioEscenaJuego()
                # print("salta a escena juego") # debug

    def registrar(self):
        
        # se registran los jugadores
        if self.director.game.registroJugadores(self.director, self.listaJugadores):
            # se registran las partidas
            if self.director.game.registroPartidas(self.director):
                return True  # el registro de ambos funcionó con exito
        return False  # ocurrió un error

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        pantalla.blit(self.fondo, (0,0))
        botonRegistrar= pygame.image.load("GUI/imagenes/botones/botonRegistrar.png")
        self.boton_registrar = Boton(pantalla, "comenzar", 540, 420,botonRegistrar,127,40)
        self.boton_registrar.dibujaBoton()

        pygame.draw.rect(pantalla, ROJO, self.cuadroTexto, 2)
        superficie = self.base.render(self.texto_usuario, True, BLANCO)
        pantalla.blit(superficie, (self.cuadroTexto.x + 5, self.cuadroTexto.y + 5)) # se ajusta el texto en el cuadrado

        self.cuadroTexto.w = superficie.get_width() + 10 # esto hace que el cuadrado se alargue dependiendo de lo que escriba el usuario
    def cambioEscenaJuego(self):
        # define las posiciones aleatorias de los jugadores dentro de cada partida
        for partida in self.director.game.listaPartidas:
            partida.generarPosicionesJug()
            partida.equiparArmasIniciales()
        juegoEscena = EscenaJuego(self.director)
        self.director.guardarEscena(juegoEscena)
        self.director.cambiarEscena(juegoEscena)

    #def registroGiu(self):
    #    print("uwu")
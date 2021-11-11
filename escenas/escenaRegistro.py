#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton
from escenas.escenaJuego import EscenaJuego
from Videojuego.Juego import Juego 
from utilidades.colores import* 

class EscenaRegistro(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.boton_agregar = None # botón para agregar jugadores
        self.fondo= pygame.image.load("imagenes/fondoRegistro.png")

        self.listaJugadores = [] # se almacenan los nombres de los jugadores 
        self.texto_usuario = '' # texto que se mostrará en pantalla al escribir 
        self.base = pygame.font.Font(None, 32) # es el tamaño de las letras 
        self.cuadroTexto = pygame.Rect(540, 470, 140, 32) # lugar donde se dibujará el cuadrado para ingresar los nombres de los jugadores 
        self.variable = 0 
        self.constante = 0

    def on_update(self):
        pygame.display.set_caption("Registrar jugadores")
        pass

    def on_event(self, evento):
        if evento.type == pygame.KEYDOWN: 
            if evento.key == pygame.K_BACKSPACE: 
                self.texto_usuario = self.texto_usuario[:-1] 
            else: 
                self.texto_usuario += evento.unicode 


        if evento.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_agregar):
                self.agregarJugador()

            if (self.variable == self.director.game.cantidadJugadores):
                self.registrar()
                self.eliminarElementosLista() 
                self.cambioEscenaJuego()
            
    def registrar(self):
        print(f'DEBUG: Objeto juego: {self.director.game}\n- - - - -')
        # se registran los jugadores
        if self.director.game.registroJugadores(self.director, self.listaJugadores):
            # se registran las partidas
            if self.director.game.registroPartidas(self.director):
                return True  # el registro de ambos funcionó con exito
        return False  # ocurrió un error

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        pantalla.blit(self.fondo, (0,0))
        self.mostrarTexto()
        self.mostrarImagenEnPos("imagenes/fondoBlanco.png", (127, 32), (540, 470))

        botonAgregar = pygame.image.load("imagenes/botones/botonAgregar.png")
        self.boton_agregar = Boton(pantalla, "agregar", 540, 520, botonAgregar, 127, 40)
        self.boton_agregar.dibujaBoton()

        pygame.draw.rect(pantalla, BLANCO, self.cuadroTexto) 
        superficie = self.base.render(self.texto_usuario, True, NEGRO) 
        pantalla.blit(superficie, (self.cuadroTexto.x + 5, self.cuadroTexto.y + 5)) # se ajusta el texto en el cuadrado 
 
        self.cuadroTexto.w = superficie.get_width() + 10 # esto hace que el cuadrado se alargue dependiendo de lo que escriba el usuario 

    def cambioEscenaJuego(self):
        # define las posiciones aleatorias de los jugadores dentro de cada partida
        for partida in self.director.game.listaPartidas:
            partida.generarPosicionesJug()
            partida.equiparArmasIniciales()
        juegoEscena = EscenaJuego(self.director)

        """ Se guardarán las escenas hasta ahora utilizadas, por lo que: listaEscenas= [escenaRegistro[2], escenaJuego[3]
        con el motivo de viajar de una a otra en un futuro"""
        self.director.guardarEscena(self.director.escena)
        self.director.guardarEscena(juegoEscena)
        self.director.cambiarEscena(juegoEscena)

    def eliminarElementosLista(self): # se eliminan los elementos de la lista para un futuro uso 
        while self.constante < self.variable: 
            self.listaJugadores.pop() 
            self.constante = self.constante+1 
        self.constante = 0 
        self.variable = 0 

    def agregarJugador(self): 
        self.variable = self.variable+1 
        self.listaJugadores.append(self.texto_usuario)
        print("Nombre del jugador", self.variable, "=", self.texto_usuario) 
        self.texto_usuario = ''

    def mostrarTexto(self):
        self.textoEnPantalla(f'Ingrese el nombre del jugador: {self.variable+1}',15,BLANCO,(480,420),False)
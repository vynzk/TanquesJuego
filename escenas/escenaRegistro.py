#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton
from escenas.escenaJuego import EscenaJuego
from Videojuego.Juego import Juego
from utilidades.colores import *


class EscenaRegistro(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.director.listaEscenas["escenaRegistro"]=self;

        self.boton_agregar = None  # botón para agregar jugadores
        self.boton_ia = None  # Requisito 2 y Requisito 4: boton de ia
        self.fondo = pygame.image.load("imagenes/fondoRegistro.png")

        """ Requisito 2 y 4: lista que almacenará el par (nombreJugador,esIa) para posteriormente registrar
        los jugadores en el juego"""
        self.datosJugadores = []
        self.texto_usuario = ''  # texto que se mostrará en pantalla al escribir
        self.base = pygame.font.Font(None, 32)  # es el tamaño de las letras
        self.cuadroTexto = pygame.Rect(self.director.ancho/2, self.director.alto/2, 127,
                                       40)  # lugar donde se dibujará el cuadrado para ingresar los nombres de los jugadores
        self.contadorJug = 0
        self.constante = 0
        self.contadorIA = 0  # Requisito 2 y Requisito 4: contador de cuantas IA hay en el juego

        #municiones
        self.municionPerforante = self.director.listaEscenas["escenaHome"].perforante
        self.municion105 = self.director.listaEscenas["escenaHome"].p105mm
        self.municion60 = self.director.listaEscenas["escenaHome"].p60mm


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
            """Si se presiona el boton agregar, se agrega el jugador al atributo lista"""
            if self.director.checaBoton(self.director.mousePos, self.boton_agregar):
                print('(escenaRegistro) PRESION BOTON: presionaste boton agregar, jugador humano registrado correctamente')
                self.guardarNombreJug(False)

            """Requisito 2 y Requisito 4: Accion del boton IA, este registra como nombre IA n° y
            presiona el boton agregar automaticamente para que este se registre sin tanto trabajo del usuario"""
            if self.director.checaBoton(self.director.mousePos, self.boton_ia):
                print('(escenaRegistro) PRESION BOTON: presionaste boton IA, IA registrada correctamente')
                self.contadorIA += 1
                self.texto_usuario = f'IA {self.contadorIA}'
                self.guardarNombreJug(True)  # << se registra como jugador

            """Una vez se ha guardado el nombre y si es ia o no (segun el boton presionado), 
            se procede el registro de los jugadores en el Juego (construccion de los objetos Jugadores
            como tal)."""
            if self.contadorJug == self.director.game.cantidadJugadores:
                self.registrar()
                self.eliminarElementosLista()
                self.cambioEscenaJuego()

    def registrar(self):
        # se registran los jugadores
        if self.director.game.registroJugadores(self.director, self.datosJugadores):
            # se registran las partidas
            if self.director.game.registroPartidas(self.director):
                return True  # el registro de ambos funcionó con exito
        return False  # ocurrió un error

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        self.mostrarTexto()
        self.mostrarImagenEnPos("imagenes/fondoBlanco.png", (127, 40), (self.director.ancho/2, self.director.alto/2))

        botonAgregar = pygame.image.load("imagenes/botones/botonAgregar.png")
        self.boton_agregar = Boton(pantalla, "agregar", self.director.ancho/2, self.director.alto/2+120, botonAgregar, 127, 40)
        self.boton_agregar.dibujaBoton()

        """Requisito 2 y Requisito 4: Se crea y muestra el boton IA"""
        botonEsIa = pygame.image.load("imagenes/botones/botonIA.png")
        self.boton_ia = Boton(pantalla, "boton ia", self.director.ancho/2+150,self.director.alto/2, botonEsIa, 127, 40)
        """Requisito 4: El primer jugador es el usuario, por tanto, no debe permitirse que se registre una IA
        como primer jugador, si quieres que juegen sólo IA, comenta el siguiente if"""
        if self.contadorJug > 0:
            self.boton_ia.dibujaBoton()

        pygame.draw.rect(pantalla, BLANCO, self.cuadroTexto)
        superficie = self.base.render(self.texto_usuario, True, NEGRO)
        pantalla.blit(superficie,
                      (self.cuadroTexto.x + 10, self.cuadroTexto.y + 10))  # se ajusta el texto en el cuadrado

        self.cuadroTexto.w = superficie.get_width() + 10  # esto hace que el cuadrado se alargue dependiendo de lo que escriba el usuario

    def cambioEscenaJuego(self):
        # define las posiciones aleatorias de los jugadores dentro de cada partida
        for partida in self.director.game.listaPartidas:
            partida.generarPosicionesJug()
            partida.equiparArmasIniciales(self.municionPerforante,self.municion105,self.municion60)

        self.director.cambiarEscena(EscenaJuego(self.director))

    def eliminarElementosLista(self):  # se eliminan los elementos de la lista para un futuro uso
        while self.constante < self.contadorJug:
            self.datosJugadores.pop()
            self.constante = self.constante + 1
        self.constante = 0
        self.contadorJug = 0

    """ Guarda el nombre del jugador que se registra en el atributo lista nombreJugadores"""

    """ Requisito 2 y Requisito 4:Guarda como información el par (nombre,esIA) en el atributo datosJugadores, recibe
    como parametroun boleando (True/False) para saber si el jugador es una IA o no 
    (esto depende si presiona el boton de IA)"""
    def guardarNombreJug(self, esIA):
        self.contadorJug = self.contadorJug + 1
        self.datosJugadores.append((self.texto_usuario, esIA))
        self.texto_usuario = ''

    def mostrarTexto(self):
        self.textoEnPantalla(f'Ingrese el nombre del jugador: {self.contadorJug + 1}', 20, BLANCO, (self.director.ancho/2-127, self.director.alto/3), False)

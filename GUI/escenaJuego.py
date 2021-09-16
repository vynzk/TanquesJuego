#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import math
from GUI import plantillaEscena
from GUI import bloque
from Mapa import Mapa


class EscenaJuego(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.fondo = pygame.image.load("GUI/imagenes/fondo.jpg")  # se asigna un fondo a la escena juego
        self.mousex, self.mousey = 0, 0  # para movimiento del mouse
        self.partidas = self.director.game.listaPartidas  # la escena juego tiene todas las partidas anteriormente creadas
        self.piso = bloque.Bloque(self.director.pantalla, 1280, 100, (9, 15, 38), 0, 620)  # piso de limite
        self.mapa = Mapa.Mapa()  # se ponen los bloques de tierra en el mapa
        self.jugadorActual = self.director.game.listaPartidas[0].jugadoresActivos[0]
        self.partidaActual = self.director.game.listaPartidas[0]
        self.trayectoria=[]
        self.contador=0

    def on_update(self):  # <<<<<<<<<<<<<<<<<<<<< ACA QUEDA LA CAGÁ
        pygame.display.set_caption("EL JUEGO DE LOS TANQUES IMPLEMENTADO EN PYTHON SIN NOMBRE AUN")

    def on_event(self, event):
        self.mousex, self.mousey = pygame.mouse.get_pos()  # capta el movimiento del mouse

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        # pantalla.fill((0,0,0)) #relleno de pantalla importante en el bucle.
        iteradorBala = self.director.iterador * 10  # fijo, no sacar
        pantalla.blit(self.fondo, (0, 0))
        self.piso.dibujar()
        self.mapa.dibujar(self.director.pantalla)
        self.dibujarTanques()
        if(self.trayectoria==[]):
            self.efectuarDisparo()
        else:
            if(self.contador<len(self.trayectoria)):
                coord=self.trayectoria[self.contador]
                pygame.draw.circle(self.director.pantalla, (0, 255, 0), (coord[0],coord[1]),1)
                self.contador+=1
                pygame.time.wait(125)
            else:
                self.contador=0 # << el contador debe estar limpio para un nuevo jugador
                self.trayectoria=[] # << la trayectoria debe estar limpio para un nuevo jugador
                self.cambiarJugador()
                enter = str(input("Apreta enter para pasar de turno y refrescar pantalla"))

        #enter = str(input("Apreta enter para pasar de turno y refrescar pantalla"))

    # de luis para kekes: sabes que dispara peeeeeeeeero no se muestra en la pantalla, me sigue preguntando el
    # angulo y potencia pero no logro ver la trayectoria
    def efectuarDisparo(self):
        print("---------------------------------------------------------------")
        print("Turno jugador: ",self.jugadorActual.nombre)
        delta = 0
        angulo = int(input("Ingrese su angulo: "))
        velocidad = int(input("Ingrese su potencia: "))
        cuadradoJugador = self.jugadorActual.tanque.bloque
        while True:
            print("el tanque del jugador ",self.jugadorActual," disparó")
            # el +10 en xDisparo es para que parta desde la mitad de la parte superior del tanque
            xDisparo = cuadradoJugador.x+10 + delta * velocidad * math.cos(angulo * 3.1416 / 180)
            # el -1 es para que no impacte el primer disparo del cañon con si mismo (la bala sale de este), si lo quitas
            # la parabola no se dibuja ya que interpreta que se tocó a si mismo (cuando sale la bala)
            yDisparo = cuadradoJugador.y-1 - (delta * velocidad * math.sin(angulo * 3.1416 / 180) - (9.81 * delta * delta) / 2)
            delta += 0.25 # si quieres que hayan más puntitos en la parabola, modifica esto
            # hay que transformarlos a int
            xDisparo = int(xDisparo)
            yDisparo = int(yDisparo)
            #print("debería dibujar una pelota en: (", xDisparo, ",", yDisparo, ")")  # debug
            self.trayectoria.append((xDisparo,yDisparo))
            #print("T:",str(self.trayectoria))
            #pygame.draw.circle(self.director.pantalla, (0, 255, 0), (xDisparo, yDisparo),1)
            #----------------------------------VERIFICAR SI TOCA BLOQUES-----------------------------------------------
            if(self.colisionTierra(xDisparo,yDisparo)): # si impacta un bloque de tierra, se detiene la parabola (bala)
                print("toqué tierra")
                break
            elif(self.saleLimites(xDisparo,yDisparo)): # si impacta con un borde, se detiene la parabola (bala)
                print("salí rango")
                break
            elif(self.colisionTanque(xDisparo,yDisparo)): # si impacta con un tanque, se detiene la parabola (bala)
                print("toqué un tanque")
                break
            #--------------------------------------------------------------------------------------------------------
        #self.cambiarJugador() # cambia de jugadorActual al otro jugador
        
    # permite el cambio de turno entre los dos jugadores (no para n jugadores, sólo sirve para la entrega)
    def cambiarJugador(self):
        listaJugadoresActuales=self.partidaActual.jugadoresActivos
        if(self.jugadorActual==listaJugadoresActuales[0]):
            self.jugadorActual=listaJugadoresActuales[1]
        else:
            self.jugadorActual=listaJugadoresActuales[0]

    # verifica si un bloque de tierra fue impactado, si lo fue retorna true, en caso contrario false
    def colisionTierra(self,xDisparo,yDisparo):
        bloquesTierra=self.mapa.listaBloques
        for bloque in bloquesTierra:
            if(bloque.colision(xDisparo,yDisparo)):
                return True # toca tierra y para el impacto
        return False # permanece en el rango correcto

    # verifica si un borde del mapa fue impactado, si lo fue retorna true, en caso contrario false
    def saleLimites(self,xDisparo,yDisparo):
        if(xDisparo>=1280 or yDisparo>=730 or xDisparo<=0 or yDisparo<=0):
            return True #sale del rango
        return False #dentro del rango

    # verifica si un tanque fue impactado, retorna true si lo fue, en caso contrario false (aun no elimina al tanque)
    # ni menos lo saca del juego, sólo detecta el impacto
    def colisionTanque(self,xDisparo,yDisparo):
        for jugador in self.partidaActual.jugadoresActivos:
            bloqueTanque=jugador.tanque.bloque
            if(bloqueTanque.colision(xDisparo,yDisparo)):
                return True # si el tanque fue impactado
        return False # si ningun tanque de un jugador fue impactado

    def dibujarTanques(self):
        for jugador in self.partidas[0].jugadoresActivos:
            jugador.tanque.bloque.dibujar()

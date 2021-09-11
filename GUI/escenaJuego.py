#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from GUI import plantillaEscena
from GUI import bloque
from Mapa import Mapa
from Tanque import Tanque



class EscenaJuego(plantillaEscena.Escena):
        
        def __init__(self, director): #constructor
            plantillaEscena.Escena.__init__(self, director)
            self.mousex,self.mousey= 0,0 #para movimiento del mouse
            
            # ELEMENTOS DE LA ESCENA #
            self.cuadrado = bloque.Bloque(self.director.pantalla, 100, 100, (222, 34, 221), 0, 0) #cuadrado rosa movible
            self.piso = bloque.Bloque(self.director.pantalla, 1280, 100, (115, 45, 20), 0, 620) #piso de limite
            #self.juego = juego #aun no se implementa en GUI
            self.mapa= Mapa.Mapa()
            #--MARTIN--esto es provisional, pero lo hice para mostrar los tanques en la pantalla
            self.tanque = bloque.Bloque(self.director.pantalla, 20, 20, (255, 0, 0), 20, 520)
            self.tanque2 = bloque.Bloque(self.director.pantalla, 20, 20, (0, 0, 255), 1200, 420) 
        
        #sobreescritura de los metodos de plantilla escena
        def on_update(self):
            pass
        def on_event(self,event):
            #prueba
            self.mousex, self.mousey = pygame.mouse.get_pos() #capta el movimiento del mouse
        
        """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""
        def on_draw(self, pantalla):
            
            pantalla.fill((0,0,0)) #relleno de pantalla importante en el bucle.
            self.piso.dibujar()
            #cuadrado de debuggeo: no sacar hasta entrega final
            self.cuadrado.definir_limite(self.mousex,self.mousey)
            self.cuadrado.dibujar()
            
            # ELEMENTOS EN PANTALLA #
            """Aquí puedes hacer tus pruebas de interfaz, cuidado con el código de arriba"""
            self.mapa.dibujar(self.director.pantalla)
            #--MARTIN--esto también es provisional 
            self.tanque.dibujar()
            self.tanque2.dibujar()
            




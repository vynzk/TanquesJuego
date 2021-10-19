#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from GUI import plantillaEscena
from GUI.Boton import Boton

class EscenaCambioArma(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.botonVolver = None
        self.botonAplicar = None
        self.listaPanelArmas= []
        self.jugadorActual = director.listaEscenas[0].jugadorActual #pos 0 siempre debe corresponder a escena juego
        # -- imagenes -- #
        #self.fondo= pygame.image.load("GUI/imagenes/fondoCambioArma.jpg") 
        self.panel= pygame.image.load("GUI/imagenes/panelArmas.png")
        self.redimensionarPanel(500,500)
        #---------------- #

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
            

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        pantalla.blit(self.fondoTransparente, (0,0))
        pantalla.blit(self.panel, (390, 100))
        
        

        # imagenes -- botones
        volver= pygame.image.load("GUI/imagenes/botones/botonVolver.png")
       
        panelArma= pygame.image.load("GUI/imagenes/panelSeleccionArmas.png")
        
        self.botonVolver = Boton(pantalla, "volver", 580,500,volver,127,40)
        self.botonVolver.dibujaBoton()
        
        
        # esto dibuja los paneles por cada arma en listaArmas
        posPanel=210 #posicion 'y' del panel
        yPanel = 60 #dimension 'y' del panel
        i=0

        #crea los objetos boton del panel y los agrega a la lista de paneles
    
        while i < len(self.jugadorActual.tanque.listaProyectiles):
            panel = Boton(pantalla, "seleccion arma", 480,posPanel,panelArma, 300,yPanel)
            self.listaPanelArmas.append(panel)
            self.listaPanelArmas[i].dibujaBoton()
            balaImagen=self.jugadorActual.tanque.listaProyectiles[i].imagen
            
            balasCantidad= 'Stock: '+ str(self.jugadorActual.tanque.listaProyectiles[i].stock)
            balaNombre = self.jugadorActual.tanque.listaProyectiles[i].nombre
            
            
            balaNombreRender = self.textoRender(balaNombre,(108, 123, 161))
            balasCantidadRender = self.textoRender(balasCantidad,(92, 81, 133))
            
            pantalla.blit(balaImagen, (480,posPanel+ 5))
            pantalla.blit(balaNombreRender, (580,posPanel+ 10))
            pantalla.blit(balasCantidadRender, (800,posPanel+ 10))
            
            
            posPanel+= yPanel + 10
            i += 1
            

    def redimensionarPanel(self, x,y):
        self.panel= pygame.transform.scale(self.panel, (x,y) )
    def vuelveJuego(self):
        juegoActual= self.director.listaEscenas[0]
        self.director.cambiarEscena(juegoActual)

    def textoRender(self,frase,color):
        fuente = pygame.font.Font("GUI/font_pixel.ttf", 10) #fuente de texto
    
        texto = fuente.render(frase, 1, color)#utimo parametro es el color... agregar despues a colores del juego
        return texto
           
    


import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton
from utilidades.colores import *

class EscenaConfig(plantillaEscena.Escena):
    def __init__(self, director):
        plantillaEscena.Escena.__init__(self, director)
        self.director.listaEscenas["escenaConfig"]=self;

        self.fondo= pygame.image.load("imagenes/fondoHome.png")
        # botones
        self.boton_aplicar = None
        self.boton_restablecer = None
        self.boton_afectosEntorno = None
        self.boton_dimensionPantalla = None

        # botones +/- jugadores
        self.boton_MasJug = None
        self.boton_MenosJug = None
        print(self.director.listaEscenas)

        # botones gravedad
        self.boton_gravedad = None
        self.boton_viento = None
        
        #cant municiones
        self.boton_perforante = None
        self.boton_105mm = None
        self.boton_60mm = None

    
    def on_update(self):
        pygame.display.set_caption("configuraciones")

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_aplicar):
                self.cambiarEscenaHome()
                print('presiona aplicado')
            if self.director.checaBoton(self.director.mousePos, self.boton_restablecer):
                print('presiona restablecer predeterminado')  
            #--------------deteccion botones +/- jugadores
           
            if self.director.checaBoton(self.director.mousePos, self.boton_MasJug):
                if(self.director.listaEscenas["escenaHome"].cantidadJugadores<6):
                    self.director.listaEscenas["escenaHome"].cantidadJugadores+=1
                else:
                    self.textoEnPantalla("El maximo de jugadores es 6",20,ROJO,(150,150),True)
            if self.director.checaBoton(self.director.mousePos, self.boton_MenosJug):
                if self.director.listaEscenas["escenaHome"].cantidadJugadores>2:
                    self.director.listaEscenas["escenaHome"].cantidadJugadores-=1
                else:
                    self.textoEnPantalla("El minimo de jugadores es 2",20,ROJO,(150,150),True)
            #------------ deteccion botones clima
            if self.director.checaBoton(self.director.mousePos, self.boton_gravedad):
                print("presione boton gravedad")
                pass
            if self.director.checaBoton(self.director.mousePos, self.boton_viento):
                # si se presiona podria cambiarse el boton a otro color
                print("presione boton viento")
                pass

        

    def on_draw(self, pantalla):
        botonVacio= pygame.image.load("imagenes/botones/botonVacio.png")

        pantalla.blit(self.fondo, (0,0))

        #---------------dibujar botones +/- jug 
        cantidadJugadores=(self.director.listaEscenas["escenaHome"]).cantidadJugadores
        self.textoEnPantalla(f'Cantidad jugadores: {cantidadJugadores}', 20, BLANCO, (150, 200), False)
        botonMasJug = pygame.image.load("imagenes/botones/botonAgregar.png")
        botonMenosJug = pygame.image.load("imagenes/botones/botonDisminuir.png")
        self.boton_MasJug = Boton(pantalla, "Mas jugador", 150, 250, botonMasJug, 127,40)
        self.boton_MenosJug = Boton(pantalla, "Menos Jugador", 300, 250, botonMenosJug, 127,40)
        self.boton_MasJug.dibujaBoton()
        self.boton_MenosJug.dibujaBoton()

        #------------dibuja botones clima
        self.textoEnPantalla(f'Efectos de entorno', 20, BLANCO, (870, 200), False)
        botonGravedad = pygame.image.load("imagenes/botones/botonGravedad.png")
        botonViento = pygame.image.load("imagenes/botones/botonClima.png")
        self.boton_gravedad = Boton(pantalla, "gravedad", 853, 250, botonGravedad, 127, 40)
        self.boton_viento = Boton(pantalla, "clima", 1003, 250, botonViento, 127, 40)
        self.boton_gravedad.dibujaBoton()
        self.boton_viento.dibujaBoton()


        
        self.boton_aplicar = Boton(pantalla, "play", 64, 420,botonVacio,40,40)
        self.boton_aplicar.dibujaBoton()

        self.boton_restablecer = Boton(pantalla, "play", 1200, 420,botonVacio,40,40)
        self.boton_restablecer.dibujaBoton()

        self.textoEnPantalla(f' efectos de entorno?',15,BLANCO,(114,250),False)
        self.boton_afectosEntorno = Boton(pantalla, "play", 64, 250,botonVacio,40,40)
        self.boton_afectosEntorno.dibujaBoton()

        self.textoEnPantalla(f' dimension de pantalla',15,BLANCO,(214,300),False)
        self.boton_dimensionPantalla = Boton(pantalla, "play", 64, 300,botonVacio,127,40)
        self.boton_dimensionPantalla.dibujaBoton()
        
        #municion
        self.textoEnPantalla(f' Proyectil Perforante',15,BLANCO,(950,150),False)
        self.boton_perforante = Boton(pantalla, "play", 900, 150,botonVacio,40,40)
        self.boton_perforante.dibujaBoton()   

        self.boton_105mm = Boton(pantalla, "play", 900, 200,botonVacio,40,40)
        self.boton_105mm.dibujaBoton()  

        self.boton_60mm = Boton(pantalla, "play", 900, 250,botonVacio,40,40)
        self.boton_60mm.dibujaBoton()       

    def cambiarEscenaHome(self):
        self.director.cambiarEscena(self.director.listaEscenas["escenaHome"])
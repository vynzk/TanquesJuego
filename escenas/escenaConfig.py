import pygame
from escenas import plantillaEscena
from utilidades.Boton import Boton
from utilidades.colores import *
import random

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

        #parametro para crear la caja de texto y hacerla funcional
        self.texto_usuario = ''  # texto que se mostrará en pantalla al escribir
        self.base = pygame.font.Font(None, 32)  # es el tamaño de las letras
        self.cuadroTexto = pygame.Rect(64, 200, 140, 32)  # lugar donde se dibujará el cuadrado para ingresar los nombres de los jugadores

        #parametros que almacenan los efectos de entorno
        self.viento = 0
        self.viento_o_no = False
        self.indicarClima = "Desactivado"

    def on_update(self):
        pygame.display.set_caption("configuraciones")

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_aplicar):
                self.cambiarEscenaHome()
                print('presiona aplicado')
            if self.director.checaBoton(self.director.mousePos, self.boton_restaurar):
                self.restablecer()
                print('presiona restablecer predeterminado')  
            #--------------deteccion botones +/- jugadores
           
            if self.director.checaBoton(self.director.mousePos, self.boton_MasJug):
                if(self.director.listaEscenas["escenaHome"].cantidadJugadores<6):
                    self.director.listaEscenas["escenaHome"].cantidadJugadores+=1
                else:
                    self.textoEnPantalla("El maximo de jugadores es 6",20,ROJO,(470,250),True)
            if self.director.checaBoton(self.director.mousePos, self.boton_MenosJug):
                if self.director.listaEscenas["escenaHome"].cantidadJugadores>2:
                    self.director.listaEscenas["escenaHome"].cantidadJugadores-=1
                else:
                    self.textoEnPantalla("El minimo de jugadores es 2",20,ROJO,(470,250),True)
            #------------ deteccion botones clima
            #if self.director.checaBoton(self.director.mousePos, self.boton_gravedad):
            #    print("presione boton gravedad")
            #    pass
            if self.director.checaBoton(self.director.mousePos, self.boton_viento):
                # si se presiona podria cambiarse el boton a otro color
                print("presione boton viento")
                self.redefinirViento()
                #self.textoEnPantalla(f'Efecto de viento: {self.viento}', 20, BLANCO, (500, 250), True)


        # al escribir, solo se toman en cuenta los números (intenté hacerlo enn un solo if, pero no me funcionó de ninguna forma)
        if event.type == pygame.KEYDOWN:
            #if event.key == (pygame.K_0) or (pygame.K_1) or (pygame.K_2) or (pygame.K_3) or (pygame.K_4) or (pygame.K_5) or (pygame.K_6) or (pygame.K_7) or (pygame.K_8) or (pygame.K_9)=):
            if event.key == pygame.K_0:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_1:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_2:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_3:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_4:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_5:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_6:
                self.texto_usuario += event.unicode
            
            elif event.key == pygame.K_7:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_8:
                self.texto_usuario += event.unicode

            elif event.key == pygame.K_9:
                self.texto_usuario += event.unicode
            
            #elif event.key == pygame.K_PERIOD:
            #    self.texto_usuario += event.unicode

            elif event.key == pygame.K_BACKSPACE:
                self.texto_usuario = self.texto_usuario[:-1]
        

    def on_draw(self, pantalla):
        botonVacio= pygame.image.load("imagenes/botones/botonVacio.png")
        botonViento = pygame.image.load("imagenes/botones/botonClima.png")
        botonAplicar = pygame.image.load("imagenes/botones/botonAplicar.png")
        botonRestaurar = pygame.image.load("imagenes/botones/botonRestaurar.png")
        pantalla.blit(self.fondo, (0,0))

        self.mostrarImagenEnPos("imagenes/fondoBlanco.png", (127, 32), (64, 200))

        #---------------dibujar botones +/- jug 
        cantidadJugadores=(self.director.listaEscenas["escenaHome"]).cantidadJugadores
        self.textoEnPantalla(f'Cantidad jugadores: {cantidadJugadores}', 20, BLANCO, (500, 150), False)
        botonMasJug = pygame.image.load("imagenes/botones/botonAgregar.png")
        botonMenosJug = pygame.image.load("imagenes/botones/botonDisminuir.png")
        self.boton_MasJug = Boton(pantalla, "Mas jugador", 500, 200, botonMasJug, 127,40)
        self.boton_MenosJug = Boton(pantalla, "Menos Jugador", 650, 200, botonMenosJug, 127,40)
        self.boton_MasJug.dibujaBoton()
        self.boton_MenosJug.dibujaBoton()


        #------------dibuja botones clima
        #self.textoEnPantalla(f'Efectos de entorno', 20, BLANCO, (870, 200), False)
        #botonGravedad = pygame.image.load("imagenes/botones/botonGravedad.png")
        #botonViento = pygame.image.load("imagenes/botones/botonClima.png")
        #self.boton_gravedad = Boton(pantalla, "gravedad", 853, 250, botonGravedad, 127, 40)
        #self.boton_viento = Boton(pantalla, "play", 64, 150,botonViento,40,40)
        #self.boton_gravedad.dibujaBoton()
        #self.boton_viento.dibujaBoton()


        
        self.boton_aplicar = Boton(pantalla, "play", 64, 420,botonAplicar,127,40)
        self.boton_aplicar.dibujaBoton()

        self.boton_restaurar = Boton(pantalla, "play", 1089, 420,botonRestaurar,127,40)
        self.boton_restaurar.dibujaBoton()

        self.textoEnPantalla(f'Clima : {self.indicarClima}', 15, BLANCO, (214, 150), False)
        #self.textoEnPantalla(f' clima?',15,BLANCO,(214,150),False)
        self.boton_viento = Boton(pantalla, "play", 64, 150,botonViento,127,40)
        self.boton_viento.dibujaBoton()

        self.textoEnPantalla(f' gravedad?',15,BLANCO,(214,200),False)
        #self.boton_gravedad = Boton(pantalla, "play", 64, 200,botonVacio,127,40)
        #self.boton_gravedad.dibujaBoton()

        self.textoEnPantalla(f' dimension de pantalla',15,BLANCO,(214,250),False)
        self.boton_dimensionPantalla = Boton(pantalla, "play", 64, 250,botonVacio,127,40)
        self.boton_dimensionPantalla.dibujaBoton()
        
        #municion
        self.textoEnPantalla(f' Proyectil Perforante',15,BLANCO,(950,150),False)
        self.boton_perforante = Boton(pantalla, "play", 900, 150,botonVacio,40,40)
        self.boton_perforante.dibujaBoton()   

        self.boton_105mm = Boton(pantalla, "play", 900, 200,botonVacio,40,40)
        self.boton_105mm.dibujaBoton()  

        self.boton_60mm = Boton(pantalla, "play", 900, 250,botonVacio,40,40)
        self.boton_60mm.dibujaBoton()       

        #es para crear el cuadro de texto que será utilizado para cambiar la gravedad
        pygame.draw.rect(pantalla, BLANCO, self.cuadroTexto)
        superficie = self.base.render(self.texto_usuario, True, NEGRO)
        pantalla.blit(superficie, (self.cuadroTexto.x + 10, self.cuadroTexto.y + 10))  # se ajusta el texto en el cuadrado

        self.cuadroTexto.w = superficie.get_width() + 10  # esto hace que el cuadrado se alargue dependiendo de lo que escriba el usuario

    def cambiarEscenaHome(self):
        self.director.cambiarEscena(self.director.listaEscenas["escenaHome"])

    #se redefine el viento cuando se presiona el botón de clima
    def redefinirViento(self):
        if self.viento_o_no == False:
            self.viento = random.randint(-10,10)
            self.viento_o_no = True
            self.indicarClima = "Activado"

        elif self.viento_o_no == True:
            self.viento = 0
            self.viento_o_no = False
            self.indicarClima = "Desactivado"

        self.director.listaEscenas["escenaHome"].viento_o_no = self.viento_o_no
        self.director.listaEscenas["escenaHome"].viento = self.viento
        print("viento:",self.viento)

    #cuando se presiona el botón de reestablecer se restablece el viento (por ahora)
    def restablecer(self):
        self.viento = 0
        self.director.listaEscenas["escenaHome"].viento = self.viento
        self.viento_o_no = False
        print("viento:",self.viento)
        self.indicarClima = "Desactivado"
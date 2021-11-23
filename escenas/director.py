# -*- encoding: utf-8 -*-
import pygame


class Director:
    """El director se encarga de iniciar el juego,
        cambiar las escenas y recoger e interpretar los eventos de estas."""

    """ adaptar pantalla: para ello, el director se crea con un determinado ancho y alto
    respectivamente para su pantalla"""
    def __init__(self,ancho,alto):  # constructor
        self.ancho=ancho
        self.alto=alto
        self.pantalla = pygame.display.set_mode((self.ancho,self.alto))
        self.escena = None
        self.running = True
        self.game = None
        self.listaEscenas = dict()
        

    def gameLoop(self):  # bucle del juego
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('(escenaJuego) PRESION BOTON VENTANA: juego terminado por presionar X')
                    self.running = False
                self.escena.on_event(event)  # no mover

            # Actualizado de escena
            self.escena.on_update()
            # Dibujo escena actual
            self.escena.on_draw(self.pantalla)
            pygame.display.update()
        print("\nJUEGO: fin del juego")

    # ---------- funciones kernel (avisar si la tocan) ----------#
    # función que cambia la escena actual a una nueva
    def cambiarEscena(self, escenaNueva):
        self.escena = escenaNueva

    # función que detecta si un botón fue presionado
    def checaBoton(self, mousePos, botonNombre):  # detecta el tocar un boton
        if botonNombre.rect.collidepoint((mousePos)):
            return True

    def cambiarResolucion(self, nuevaX,nuevaY):
        self.ancho= nuevaX
        self.alto= nuevaY
        self.pantalla = pygame.display.set_mode((self.ancho,self.alto))

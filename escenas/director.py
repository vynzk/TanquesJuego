# -*- encoding: utf-8 -*-
import pygame


class Director:
    """El director se encarga de iniciar el juego,
        cambiar las escenas y recoger e interpretar los eventos de estas."""

    def __init__(self):  # constructor
        self.pantalla = pygame.display.set_mode((1280, 720))
        self.escena = None
        self.running = True
        self.game = None
        self.listaEscenas = []
        

    def gameLoop(self):  # bucle del juego
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("JUEGO CERRADO POR PRESIONAR X")
                    self.running = False
                self.escena.on_event(event)  # no mover

            # Actualizado de escena
            self.escena.on_update()
            # Dibujo escena actual
            self.escena.on_draw(self.pantalla)
            pygame.display.update()
        print("FIN DEL JUEGO")

    # ---------- funciones kernel (avisar si la tocan) ----------#
    # función que cambia la escena actual a una nueva
    def cambiarEscena(self, escenaNueva):
        self.escena = escenaNueva

    # función que detecta si un botón fue presionado
    def checaBoton(self, mousePos, botonNombre):  # detecta el tocar un boton
        if botonNombre.rect.collidepoint((mousePos)):
            return True

    def guardarEscena(self,escena):
        self.listaEscenas.append(escena)
        
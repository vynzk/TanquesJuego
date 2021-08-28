# -*- encoding: utf-8 -*-

import pygame


class Director:
    """El director se encarga de iniciar el juego,
        cambiar las escenas y recoger e interpretar los eventos de estas."""
    
    def __init__(self): #constructor
        pygame.display.set_caption("prueba GUI")
        self.pantalla = pygame.display.set_mode((800,600))
        self.escena = None
        self.running = True
    
    def gameLoop(self): #bucle del juego
        while self.running:
            
            #Evento de salida
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('Juego cerrado')
                    self.running = False

            # Detector de eventos de la escena actual
            self.escena.on_event()
            # Actualizado de escena
            self.escena.on_update()
            # Dibujo escena actual
            self.escena.on_draw(self.pantalla)
            pygame.display.flip()

#---------- funciones ----------#
    def cambiarEscena(self, escenaNueva):
        "cambia la escena actual"
        self.escena = escenaNueva           

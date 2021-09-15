# -*- encoding: utf-8 -*-

from GUI.escenaJuego import EscenaJuego
import pygame

class Director:
    """El director se encarga de iniciar el juego,
        cambiar las escenas y recoger e interpretar los eventos de estas."""

    def __init__(self,game):  # constructor

        self.pantalla = pygame.display.set_mode((1280, 720))
        self.escena = None
        self.activadorDisparo= False #por mientras
        self.running = True
        self.listaEscenas = []
        self.mousePos = None
        self.iterador= 0
        self.game=game
        # self.mousex,self.mousey= 0,0 #para movimiento del mouse
        # self.enlistarEscenas() #quizas se implemente en necesidad.

    def gameLoop(self):  # bucle del juego
        while self.running:
            # pygame.display.set_caption("PYTHON TANKS") #si lo activas hay un bug re loco... no lo hagas :-)
            # Evento de salida
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('Juego cerrado')
                    self.running = False
                self.escena.on_event(event)  # no mover

            # Actualizado de escena
            self.escena.on_update()
            # Dibujo escena actual
            self.escena.on_draw(self.pantalla)
            if(self.activadorDisparo==True): #debuggueo
                self.iterador+=1
                

            pygame.display.update()
            
    # ---------- funciones kernel (avisar si la tocan) ----------#
    def cambiarEscena(self, escenaNueva):
        "cambia la escena actual"
        self.escena = escenaNueva
    def EscenaAux(self, EscenaAux): #de debbugueo
        self.escenaAux= EscenaAux
    def checaBoton(self, mousePos, botonNombre):  # detecta el tocar un boton
        if botonNombre.rect.collidepoint((mousePos)):
            return True

    # ---- funciones de luis ---
    def terminoJuego(self):
        # cambiarEscena(escenaCreditos) algo así
        self.juego.mostrarRanking()
        self.juego.definirGanador()
        print("\n!!!!!!!!!!! El/la ganadora es: ", self.juego.getJugadorGanador().getNombre(), " !!!!!!!!!!!!!!")
        print("terminó el juego")

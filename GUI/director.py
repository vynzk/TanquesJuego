from GUI.escenaJuego import EscenaJuego
import pygame

class Director:
    """El director se encarga de iniciar el juego,
        cambiar las escenas y recoger e interpretar los eventos de estas."""
    
    def __init__(self,juego): #constructor
        pygame.display.set_caption("prueba GUI")
        self.pantalla = pygame.display.set_mode((1280,720))
        self.escena = None
        self.running = True
        self.juego=juego

    def gameLoop(self): #bucle del juego
        while self.running:            
            #Evento de salida
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('Juego cerrado')
                    self.running = False
            
            for partida in self.juego.getListaPartidas():
                self.cambiarEscena(partida.getEscena())
                print("\nObjeto escena actual: "+str(self.escena))
                input("saltar de partida")
            break; # << termina
        print("terminó el juego")
        

    def registroJugadores(self):
        self.juego.registroJugadores()

    def registroPartidas(self):
        self.juego.registroPartidas(self) # << le pasas el objeto "self" porque necesitan acceder a el mismo 
        # para tener la pantalla de este.
        self.juego.mostrarCaracteristicas()


    def cambiarEscena(self, escenaNueva):
        "cambia la escena actual"
        self.escena = escenaNueva   
        self.escena.on_event() # BUG: no funciona la deteccion de eventos (el mouse)
        self.escena.on_update()
        self.escena.on_draw(self.pantalla)
        pygame.display.flip()

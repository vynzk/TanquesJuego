from GUI.escenaJuego import EscenaJuego
from Videojuego.Juego import *
from GUI.escenaHome import EscenaHome
from GUI.director import *

def main():
    game = Juego(2, 1)  # (cantidadJugadores,cantidadPartidas) #se automatizó para debuguear lo escencial
    director = Director(game)
    home = EscenaHome(director)  
    director.cambiarEscena(home)
    director.gameLoop()

###
if __name__ == '__main__':
    pygame.init()
    main()

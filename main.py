from Videojuego.Juego import *
from escenas.escenaHome import EscenaHome
from escenas.director import *


def main():
    game = Juego(3, 1)  # (cantidadJugadores,cantidadPartidas) #se automatizó para debuguear lo escencial
    director = Director(game)
    home = EscenaHome(director)  

    director.cambiarEscena(home) #debe ir home
    director.gameLoop()


###
if __name__ == '__main__':
    pygame.init()
    main()

from Videojuego.Juego import *
from escenas.escenaHome import EscenaHome
from escenas.escenaConfig import EscenaConfig
from escenas.director import *

'''orden actual de escenas:
    0 - escenaHome
    1 - escenaConfig
    2 - escenaRegistro
    3 - escenaJuego
'''


def main():
    game = Juego(2, 1)  # (cantidadJugadores,cantidadPartidas) #se automatizó para debuguear lo escencial
    director = Director(game)
    home = EscenaHome(director)
    config = EscenaConfig(director)

    director.guardarEscena(home)
    director.guardarEscena(config)
    director.cambiarEscena(director.listaEscenas[0]) #debe ir home
    director.gameLoop()


###
if __name__ == '__main__':
    pygame.init()
    print('miau')
    main()

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
    director = Director()
    home = EscenaHome(director)  
    director.cambiarEscena(home)
    director.gameLoop()


###
if __name__ == '__main__':
    pygame.init()
    print('miau')
    main()
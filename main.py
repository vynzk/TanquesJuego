from escenas.escenaHome import EscenaHome
from escenas.director import *


def main():
    director = Director()
    home = EscenaHome(director)  

    director.cambiarEscena(home) #debe ir home
    director.gameLoop()


###
if __name__ == '__main__':
    pygame.init()
    main()
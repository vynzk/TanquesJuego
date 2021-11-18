from escenas.escenaHome import EscenaHome
from escenas.director import *


def main():
    director = Director(1200,800)
    home = EscenaHome(director)  
    director.cambiarEscena(home)
    director.gameLoop()


###
if __name__ == '__main__':
    pygame.init()
    main()
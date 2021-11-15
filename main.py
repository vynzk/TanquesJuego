from escenas.escenaHome import EscenaHome
from escenas.director import *


def main():
    director = Director(800,1000)
    home = EscenaHome(director)  
    director.cambiarEscena(home)
    director.gameLoop()


###
if __name__ == '__main__':
    pygame.init()
    main()
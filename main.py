from escenas.escenaHome import EscenaHome
from escenas.escenaConfig import EscenaConfig
from escenas.director import *

def main():
    # buena practica que recomendó el profesor, si esta True mostrará los mensajes
    # de utilidad para el equipo, en caso contrario, la terminal estará limpia 
    debug=True
    director = Director(800,800,debug)
    home = EscenaHome(director)  
    director.cambiarEscena(home)
    director.gameLoop()
    


###
if __name__ == '__main__':
    pygame.init()
    main()
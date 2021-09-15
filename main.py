from Videojuego.Juego import *
from GUI.escenaHome import EscenaHome
from GUI.director import *

""" #no descomentar
while True:
    try:
        cantidadJugadores = int(input("\nIngrese la cantidad de jugadores: "))
        if cantidadJugadores > 1:
            break
        else:
            print("ERROR: la cantidad de jugadores debe ser mayor que 2, intentalo nuevamente")
    except:
        print("ERROR: variable de tipo incorrecto")
while True:
    try:
        cantidadPartidas = int(input("\nIngrese la cantidad de partidas: "))
        if cantidadPartidas >= 1:
            break
        else:
            print("ERROR: la cantidad de partidas debe ser mayor o igual a 1, intentalo nuevamente")
    except:
        print("ERROR: variable de tipo incorrecto")
"""


def main():
    game = Juego(2, 1)  # (cantidadJugadores,cantidadPartidas) #se automatizó para debuguear lo escencial
    director = Director(game)
    home = EscenaHome(director)  # por ahora no toquen esto <3 será la escena predeterminada hasta presentar
    director.cambiarEscena(home)

    # director.registroJugadores() #generan BUG, no descomentar hasta solucionar
    # director.registroPartidas()
    director.gameLoop()


###
if __name__ == '__main__':
    pygame.init()
    main()

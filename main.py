from GUI.plantillaEscena import Escena
from Videojuego.Juego import *
from GUI import escenaJuego
from GUI.director import *

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

game = Juego(cantidadJugadores,cantidadPartidas)
director = Director(game)
director.registroJugadores()
director.registroPartidas()
director.gameLoop() # << ciclo de partidas, acá comienza el juego

###



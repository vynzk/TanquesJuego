from Juego import *

cantidadJugadores=int(input("Ingrese la cantidad de jugadores: "))
cantidadPartidas=int(input("Ingrese la cantidad de partidas: "))
game=Juego(cantidadJugadores,cantidadPartidas)
game.mostrarCaracteristicas()
game.registroJugadores()
game.comenzar()
from Jugador import *
class Partida():
    def __init__(self,listasJugadores):
        self.jugadoresActivos=listasJugadores

    def mostrarJugadoresActivos(self):
        listaNombresActivos=[]
        for jugador in self.jugadoresActivos:
            listaNombresActivos.append(jugador.nombre)
        
        print(" JUGADORES ACTIVOS")
        print("     Nombres: "+str(listaNombresActivos))
        print("     Objetos: "+str(self.jugadoresActivos))

    def eliminarJugador(self):
        print("\nELIMINAR JUGADOR [Debug]")
        self.mostrarJugadoresActivos()
        opcionEliminar=int(input("  Ingrese la posicion del jugador que desea eliminar: "))
        try:
            jugadorEliminado=self.jugadoresActivos[opcionEliminar]
            self.jugadoresActivos.pop(opcionEliminar) # << lo eliminamos
            print(" Jugador/a ",jugadorEliminado," ha sido eliminado")
        except: 
            print(" ERROR: fuera de rango")
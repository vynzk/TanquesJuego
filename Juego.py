from Jugador import *
from Tanque import *

class Juego():
    def __init__(self,cantidadJugadores):
        self.cantidadJugadores=cantidadJugadores
        self.listaJugadores=[]
        self.listaTanquesDisponibles=[Tanque] # acá iran los objetos tanques disponibles para elegir inicialmente

    # funcion que registra a un jugador seleccionando su nombre y su tanque inicial
    def agregarJugador(self):
        # KERNEL: ACÁ DEBE MOSTRARSE LA CAJA DE TEXTO DONDE ALMACENARÁ EL NOMBRE DEL JUGADOR
        # EL TEXTO QUE CONTENGA ESTE DEBE SER JUGARDADO EN MI VARIABLE "nombre"
        nombre=str(input("Ingrese su nombre: "))

        # KERNEL: ACÁ DEBE IR LA ELECCION DE TANQUE INICIAL; DE MOMENTO SÓLO ES UNO
        # SIN EMBARGO, DEBE MOSTRARSE EN PANTALLA Y HACER QUE SE ELIJA, DICHA ELECCION
        # SERÁ UN OBJETO TANQUE EN CONCRETO, QUE DEBE GUARDARSE EN MI VAR "tanque"
        # DE MOMENTO, SÓLO ESTA EL TANQUE DEFAULT
        tanque=Tanque("Default") # << indica el nombre del modelo del tanque, en este caso sólo existe uno, el default
        self.listaJugadores.append(Jugador(nombre,tanque)) # << agrega un nuevo Jugador con su nombre y su tanque

    # metodo debug, sin embargo, puede servir para mostrar el tablero
    def mostrarJugadores(self):
        print("### LISTA JUGADORES ###") # borrar en un futuro
        for jugador in self.listaJugadores:
            jugador.mostrarInformacion()

    # metodo que se encargará de llenar la lista de jugadores, registrará tantos jugadores
    # como lo indique la cantidad de jugadores (que debe tener el constructor de esta clase)
    def registroJugadores(self):
        for i in range(1,self.cantidadJugadores+1):
            self.agregarJugador()
        self.mostrarJugadores()

# prueba de que funciona
game=Juego(2)
print("TANQUES DISPONIBLES EN EL JUEGO:"+str(game.listaTanquesDisponibles)+"+\n")
game.registroJugadores()
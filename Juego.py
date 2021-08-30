from Jugador import *
from Tanque import *
from Partida import *

class Juego():
    def __init__(self,cantidadJugadores,cantidadPartidas):
        self.cantidadJugadores=cantidadJugadores
        self.listaJugadores=[]
        self.cantidarPartidas=cantidadPartidas
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
        print("### REGISTRO DE JUGADORES ###")
        for i in range(1,self.cantidadJugadores+1):
            self.agregarJugador()
        self.mostrarJugadores()

    # metodo que comienza la partida (luego de la fase de eleccion y compra)
    def comenzar(self):
        # se jugará tantas partidas como lo indique cantidadPartidas
        print("### COMENZÓ JUEGO ###")
        for i in range(1,self.cantidarPartidas+1):
            print(">>> PARTIDA "+ str(i))
            partida=Partida(self.listaJugadores)
            numeroTurno=1

            # comienzan los turnos
            for jugador in partida.jugadoresActivos:
                print("Turno "+str(numeroTurno)+": "+str(jugador.nombre))
                input("presiona enter para pasar tu turno")
                numeroTurno+=1
        print("### FIN DEL JUEGO ###")


    # metodo debug, para mostrar las caracteristicas de la partida
    def mostrarCaracteristicas(self):
        print("### CARACTERISTICAS DEL JUEGO ####")
        print("Cantidad jugadores: "+str(self.cantidadJugadores))
        print("Cantidad partidas: "+str(self.cantidarPartidas))
        print("Tanques disponibles: "+str(self.listaTanquesDisponibles))


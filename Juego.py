from Jugador import *
from Tanque import *
from Partida import *


class Juego():
    def __init__(self, cantidadJugadores, cantidadPartidas):
        self.cantidadJugadores = cantidadJugadores
        self.listaJugadores = []
        self.cantidarPartidas = cantidadPartidas
        self.listaPartidas = []
        self.listaTanquesDisponibles = [Tanque]  # acá iran los objetos tanques disponibles para elegir inicialmente

    def agregarJugador(self):
        nombre = str(input("Ingrese su nombre: "))
        tanque = Tanque("Default")
        self.listaJugadores.append(Jugador(nombre, tanque))  # << agrega un nuevo Jugador con su nombre y su tanque

    # función que se encargará de llenar la lista de jugadores, registrará tantos jugadores
    # como lo indique la cantidad de jugadores (que debe tener el constructor de esta clase)
    def registroJugadores(self):
        print("\n### REGISTRO DE JUGADORES ###")
        for i in range(1, self.cantidadJugadores + 1):
            self.agregarJugador()

    # función que agregará una partida a la lista de partidas, cada partida agregará como jugadores activos a la
    # totalidad de jugadores que participan en el juego
    def agregarPartida(self, i):
        partida = Partida(i)
        # va agregando los jugadores a la nueva partida
        for jugador in self.listaJugadores:
            partida.agregarJugadores(jugador)
        return partida

    # función que llenara la lista de partidas (atributo) con cada partida creada
    def registroPartidas(self):
        for i in range(1, self.cantidarPartidas + 1):
            self.listaPartidas.append(self.agregarPartida(i))

    def mostrarRanking(self):
        print("\n### R A N K I N G ###")
        for jugador in self.listaJugadores:
            jugador.mostrarInformacion()

    # funcion que comienza la partida (luego de la fase de eleccion y compra)
    def comenzar(self):
        # se jugará tantas partidas como lo indique cantidadPartidas
        self.registroJugadores()
        self.registroPartidas()

        self.mostrarCaracteristicas()
        print("\n       I N I C I A         E L             J U E G O")

        # se empieza a jugar cada partida individualmente
        for partida in self.listaPartidas:
            print("\n>>Partida " + str(partida.getId()))
            numeroTurno = 1
            # mientras exista más de un jugador en pie, se juega
            while len(partida.jugadoresActivos) > 1:
                # comienzan los turnos de los jugadores (vivos)
                for jugador in partida.jugadoresActivos:
                    print("------------------------------------------")
                    print("Turno ", str(numeroTurno), ": ", str(jugador.nombre))

                    # NOTA: esto es un poco enrredado, el metodo eliminar jugador recibe el jugador del turno
                    # actual, esta información es valiosa para mostrar la acción: jugador actual mata al que sigue
                    # por ejemplo. EL jugador actual no puede poseer este metodo porque no tiene información de los
                    # otros jugadores.

                    # que la función reciba a "jugador" no quiere decir precisamente que este muere, sino más bien
                    # que este tiene la posiblidad de atacar
                    partida.eliminarJugador(jugador)
                    input("presiona enter para pasar tu turno")
                    numeroTurno += 1

            # cuando se rompe el ciclo, es decir sólo queda un jugador en pie
            partida.terminarPartida()  # << guarda el unico jugador activo como ganador

        print("\n### FIN DEL JUEGO ###")
        self.mostrarCaracteristicas()
        self.mostrarRanking()

    # metodo debug, para mostrar las caracteristicas de la partida
    def mostrarCaracteristicas(self):
        print("\n### CARACTERISTICAS DEL JUEGO ####")
        print("Cantidad jugadores: " + str(self.cantidadJugadores))
        print("Cantidad partidas: " + str(self.cantidarPartidas))
        print("Tanques disponibles: " + str(self.listaTanquesDisponibles))
        for partida in self.listaPartidas:
            partida.mostrarInformacion()
        print("#######################################")

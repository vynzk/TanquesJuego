class Partida():
    def __init__(self, id, escenaJuego):
        self.id = id
        self.estado = False
        self.jugadorGanador = None
        self.jugadoresActivos = []
        self.escena=escenaJuego

    # funcion que agrega jugadores a su lista de jugadores activos
    def agregarJugadores(self, jugador):
        self.jugadoresActivos.append(jugador)

    # función debug, muestra los nombres y objetos de los jugadores activos
    def mostrarJugadoresActivos(self):
        listaNombresActivos = []
        for jugador in self.jugadoresActivos:
            listaNombresActivos.append(jugador.nombre)

        print(" JUGADORES ACTIVOS")
        print("     Nombres: " + str(listaNombresActivos))
        print("     Objetos: " + str(self.jugadoresActivos))

    # funcion debug, que muestra toda la información de la partida
    def mostrarInformacion(self):
        print("\nPartida " + str(self.id))
        self.mostrarJugadoresActivos()
        print(" Estado: " + str(self.estado))
        print(" Objeto escena: "+str(self.escena))
        print(" Ganador: " + str(self.jugadorGanador))

    # funcion que termina la partida cuando queda sólo un jugador activo dentro de ella
    def terminar(self):
        self.estado = True
        self.jugadorGanador = self.jugadoresActivos[0]
        self.jugadorGanador.sumarVictoria()
        print("\n!!!! El/la jugador/a ", self.jugadorGanador.getNombre(), " ganó la partida !!!!")

    # funcion que permite al tanque de un jugador realizar un disparo
    def efectuarDisparo(self,TanqueAtacante):
        while True: # se realiza este while para probar multiples veces
            delta = 0
            angulo=int(input("Ingrese angulo: "))
            velocidad=int(input("Ingrese la velocidad: "))
            if(angulo==0 and velocidad==0): # para parar las pruebas
                return False # pasa el turno, no chocó con nada
            while delta <= 500:
                xDisparo = TanqueAtacante.getCuadrado().x + delta * velocidad * math.cos(angulo * 3.1416 / 180)
                yDisparo = TanqueAtacante.getCuadrado().y - (delta * velocidad * math.sin(angulo * 3.1416 / 180) - (9.81 * delta * delta) / 2)
                if(comprobarImpactoTanques(xDisparo,yDisparo)== True):
                    return True # comprueba si le llegó a un tanque, si llega, pasa de turno
                delta += 0.01
                pygame.draw.circle(pantalla, (0, 255, 0), (xDisparo, yDisparo),1)

    # comprueba si los jugadores son impactados
    def comprobarImpactoTanques(self,xDisparo,yDisparo):
        for jugador in self.jugadoresActivos:
            #cuadrado del tanque
            cuadradoTanque=jugador.getTank().getCuadrado()
            if(cuadradoTanque.colision(xDisparo,yDisparo)==True):
                print("impactado")
                return True
            else:
                print("no impactado")
                return False

    # funcion que brinda la posibilidad de eliminar jugadores al jugadorAtacante 
    def eliminarJugador(self, jugadorAtacante):
        print("\nELIMINAR JUGADOR [Debug]")
        self.mostrarJugadoresActivos()
        opcionEliminar = int(input("  Ingrese la posicion del jugador que desea eliminar: "))
        try:
            jugadorEliminado = self.jugadoresActivos[opcionEliminar]
            self.jugadoresActivos.pop(opcionEliminar)  # << lo eliminamos
            print("\n>>ACCION: Jugador/a ", jugadorEliminado.getNombre(), " ha sido eliminado por ",
            jugadorAtacante.getNombre())
        except:
            print(" ERROR: fuera de rango")

    def getId(self):
        return self.id

    def getGanador(self):
        return self.jugadorGanador

    # función que retorna el objeto escena en concreto de esa partida, la cual se modifican al disparar
    # eliminar tanques, etc (visualmente)
    def getEscena(self):
        return self.escena 
    
    def getJugadoresActivos(self):
        return self.jugadoresActivos
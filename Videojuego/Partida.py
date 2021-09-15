# en el momento que sólo queda un jugador activo en la partida, se invoca el metodo terminar y pasa a la otra partida
#partida debe ir eliminando a los jugadoras activos cuyo tanque es alcanzado
#partida debe llamar la función "pasarTurno" del jugadorActual (otrogrado por el TurnoActual) al momento de que un proyectil colisione (con un tanque o con el piso)
from Videojuego.AdministradorTurnos import AdministradorTurnos

class Partida():
    def __init__(self, id,pantalla):
        self.id = id
        self.estado = False
        self.pantalla=pantalla # pantalla que le pasa el director)
        self.jugadorGanador = None
        self.jugadoresActivos = []
        self.contadorJugador=0 

    """
    def asignarTurno(self): #i ingresado debe ser igual a 0
        #self.partida.asignarTurno(self.partidaActual.jugadoresActivos[self.i])
        print("Le toca al jugador: ",self.turnoActual.jugadorActual) #debug
        if self.contadorJugador < len(self.jugadoresActivos):
            self.contadorJugador+=1 # le toca al jugador
        else:
            self.contadorJugador=0 # da la vuelta 
        # cambia de jugador
        self.turnoActual.jugadorActual=self.jugadoresActivos[self.contadorJugador]#self.contadorJugador
    """

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

    def mostrarJugadoresPos(self):
        print("\nPartida " + str(self.id))
        for jugador in self.jugadoresActivos:
            print(jugador.nombre," >> (",jugador.tanque.x,",",jugador.tanque.y,")","; color:",jugador.tanque.color)

    # funcion debug, que muestra toda la información de la partida
    def mostrarInformacion(self):
        print("\nPartida " + str(self.id))
        self.mostrarJugadoresActivos()
        print(" Estado: " + str(self.estado))
        print(" Ganador: " + str(self.jugadorGanador))

    # funcion que termina la partida cuando queda sólo un jugador activo dentro de ella
    def terminar(self):
        self.estado = True
        self.jugadorGanador = self.jugadoresActivos[0]
        self.jugadorGanador.sumarVictoria()
        print("\n!!!! El/la jugador/a ", self.jugadorGanador.getNombre(), " ganó la partida !!!!")

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
            # partida.PasarTurno |  aca pasariamos de turno <<<<<<<<<<<<<<<<<<<<
        except:
            print(" ERROR: fuera de rango")

    def getId(self):
        return self.id

    def getGanador(self):
        return self.jugadorGanador
    
    def getJugadoresActivos(self):
        return self.jugadoresActivos

    """
    def setTurno(self,turno):
        self.turnoActual=turno

    def PasarTurno(self):
        # mientras haya un jugador activo
        if( len(self.jugadoresActivos) > 1):
            self.asignarTurno() #entonces automaticamente self.turnoactual.jugadoractual cambia.
            return True
        else:
            self.terminar()
            print("fin de la partida")
            return False
            # llamar escenaFinal() <---- quieres ir a home o otra partida?? o que pase automaticamente 
            # invocar a cambiarPartida <<<<<<<<<<<<<
        # si no entra al while, automaticamente invoca a partida.terminar()
        
    def disparaJugadorActual(self, angulo, potencia):
        self.turnoActual.efectuarDisparo(angulo,potencia)
        self.PasarTurno() #luego de que dispara se llama a pasrturno de clase partida

    """
    
    """
     # funcion que permite al tanque de un jugador realizar un disparo
    def efectuarDisparo(self,TanqueAtacante):
        while True: # se realiza este while para probar multiples veces
            delta = 0
            angulo=int(input("Ingrese angulo: "))
            velocidad=int(input("Ingrese la velocidad: "))
            trayectoria=[]
            if(angulo==0 and velocidad==0): # para parar las pruebas
                return False # pasa el turno, no chocó con nada
            while delta <= 20:
                xDisparo = TanqueAtacante.getCuadrado().x + delta * velocidad * math.cos(angulo * 3.1416 / 180)
                yDisparo = TanqueAtacante.getCuadrado().y - (delta * velocidad * math.sin(angulo * 3.1416 / 180) - (9.81 * delta * delta) / 2)
                trayectoria.append((xDisparo,yDisparo)) # vas agregandolo a la lista de trayectoria
                if(self.comprobarImpactoTanques(xDisparo,yDisparo)== True):
                    # aca 
                    TanqueAtacante.setTrayectoria(trayectoria) # << 
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
    """
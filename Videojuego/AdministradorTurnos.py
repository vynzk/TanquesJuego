import pygame
import math

class AdministradorTurnos:
    def __init__(self,pantalla,partidas):
        self.listaPartidas=partidas
        self.jugadorActual=None # asigna 
        self.trayectoria = [] #temporal
        self.pantalla=pantalla
        self.efectuarDisparo(self.pantalla) # dispara el primer jugador
        self.comenzarPrimeraPartida()

    def comenzarPrimeraPartida(self):
        print("Partidas:",str(self.listaPartidas))
        print("Jug part1:",str(self.listaPartidas[0].jugadoresActivos))
        # aca sucede la designacion de que el primer jugador de la partida 1 dispara
        pass

    # funcion que permite al tanque de un jugador realizar un disparo
    def efectuarDisparo(self,pantalla):
        while True: # se realiza este while para probar multiples veces
            delta = 0
            angulo=int(input("Ingrese angulo: "))
            velocidad=int(input("Ingrese la velocidad: "))
            
            #activar la bala del tanque del jugador actual
            
            trayectoria=[]
            if(angulo==0 and velocidad==0): # para parar las pruebas
                return False # pasa el turno, no chocó con nada
            while delta <= 20:
                xDisparo = self.jugadorActual.tanque.bloque.x + delta * velocidad * math.cos(angulo * 3.1416 / 180)
                yDisparo = self.jugadorActual.tanque.bloque.y - (delta * velocidad * math.sin(angulo * 3.1416 / 180) - (9.81 * delta * delta) / 2)
                trayectoria.append((xDisparo,yDisparo)) # vas agregandolo a la lista de trayectoria
                if(self.comprobarImpactoTanques(xDisparo,yDisparo)== True):
                    # aca hay que pasarle la trayectoria al turno 
                    # TanqueAtacante.setTrayectoria(trayectoria) # << 
                    return True # comprueba si le llegó a un tanque, si llega, pasa de turno
                delta += 0.01
                pygame.draw.circle(pantalla, (0, 255, 0), (xDisparo, yDisparo),1)
        return trayectoria

    # comprueba si los jugadores son impactados
    def comprobarImpactoTanques(self,xDisparo,yDisparo):
        for jugador in self.jugadoresActivos:
            #cuadrado del tanque
            bloqueTanque=jugador.tanque.bloque
            #jugador.getTank().getCuadrado()
            if(bloqueTanque.colision(xDisparo,yDisparo)==True):
                print("impactado")
                return True
            else:
                print("no impactado")
                return False
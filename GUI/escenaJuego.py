#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import math
from GUI import plantillaEscena
from GUI import bloque
from Mapa import Mapa
import time


class EscenaJuego(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.fondo = pygame.image.load("GUI/imagenes/fondo.jpg")  # se asigna un fondo a la escena juego
        self.mousex, self.mousey = 0, 0  # para movimiento del mouse
        self.partidas = self.director.game.listaPartidas  # la escena juego tiene todas las partidas anteriormente creadas
        self.piso = bloque.Bloque(self.director.pantalla, 1280, 100, (9, 15, 38), 0, 620)  # piso de limite
        self.mapa = Mapa.Mapa()  # se ponen los bloques de tierra en el mapa
        self.jugadorActual = self.director.game.listaPartidas[0].jugadoresActivos[0]
        self.partidaActual = self.director.game.listaPartidas[0]
        self.disparoTrayectoria=[]
        self.angulo , self.velocidad = 40 , 114 #no tocar aun... angulos por defecto.
        self.flag = False #confirma si el jugador actual puede disparar
        self.final = False
    def on_update(self):  # <<<<<<<<<<<<<<<<<<<<< ACA QUEDA LA CAGÁ
        pygame.display.set_caption("EL JUEGO DE LOS TANQUES IMPLEMENTADO EN PYTHON SIN NOMBRE AUN")
        #pygame.display.update()
        #prueba de eventos
        self.director.pantalla.blit(self.fondo, (0, 0))
        self.muestreoVelocidadAngulo() #dibuja la velocidad y el angulo elegido por el usuario
        self.piso.dibujar()
        self.mapa.dibujar(self.director.pantalla)
        self.dibujarTanques()
       



    def on_event(self, event):
        #self.mousex, self.mousey = pygame.mouse.get_pos()  # capta el movimiento del mouse (no sacar por debuggueos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.velocidad +=1
                print("left: velocidad --")
            if event.key == pygame.K_RIGHT:
                self.velocidad -=1
                print("right: velocidad ++")
            if event.key == pygame.K_UP:
                self.angulo +=1
                print("up: angulo ++")
            if event.key == pygame.K_DOWN:
                self.angulo -=1
                print("down: angulo --")
            if event.key == pygame.K_SPACE:
                print("space: dispara")
                
                if (self.flag==False):
                    print("flag: true")
                    self.flag= True #flag es para efectuar el disparo
                    self.director.activadorDisparo = True #activa el iterador de disparo en director
                else:
                    print("cambia de TURNOa antes!")
                
            if event.key == pygame.K_TAB:
                print("tab: cambia de turno")
                print("flag: false")
                self.cambioDeTurno()
                self.director.iterador = 0
                self.flag = False

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        iteradorBala = self.director.iterador * 10  # fijo, no sacar
        if(self.flag==False):
            jugadorPos= self.jugadorActual.tanque.bloque
            coordActual=(jugadorPos.x+21,jugadorPos.y+1)
        if (self.flag == True):
            trayectoria=self.efectuarDisparo(self.angulo,self.velocidad)  
            coordActual=trayectoria[(iteradorBala)]

          
        self.verificaColisionBala(coordActual[0],coordActual[1])
        self.jugadorActual.tanque.bala.activaProyectil()
        self.jugadorActual.tanque.bala.sigueTrayectoria(coordActual)
        

        if (self.final):
            self.mensajeFinal()
            
            time.sleep(1)
            self.director.running=False



        #creación del dibujo de la trayectora y el movimiento del objeto proyectil
        """
        trayectoria=self.efectuarDisparo() #deberia pedir pantalla pero no pa no la quiere #además de efectuar disparo deja su trayectoria (no borrar)
        CoordenadaTrayectoriaActual=trayectoria[(iteradorBala)] 
        self.jugadorActual.tanque.bala.sigueTrayectoria(CoordenadaTrayectoriaActual) 
        enter = str(input("Apreta enter para pasar de turno y refrescar pantalla"))
        """
    # de luis para kekes: sabes que dispara peeeeeeeeero no se muestra en la pantalla, me sigue preguntando el
    # angulo y potencia pero no logro ver la trayectoria
    # respuesta de keke: es probable que sea porque no estamos implementando los eventos y es por consola... revisré.
    #   no muestra disparo porque eliminaste la lista que guarda las trayectorias CUIDADO CON ELIMINAR COSAS! pero lo implementaré denuevo.
    def verificaColisionBala(self, xDisparo,yDisparo):
        #----------------------------------VERIFICAR SI TOCA BLOQUES-----------------------------------------------
        if(self.colisionTierra(xDisparo,yDisparo)): # si impacta un bloque de tierra, se detiene la parabola (bala)
            print("toqué tierra")
            self.flag=False
            
            #break;
        elif(self.saleLimites(xDisparo,yDisparo)): # si impacta con un borde, se detiene la parabola (bala)
            print("salí rango")
            self.flag=False
            
            #break;
        elif(self.colisionTanque(xDisparo,yDisparo)): # si impacta con un tanque, se detiene la parabola (bala)
            print("toqué un tanque")
            self.flag=False
            
            #break;
        #--------------------------------------------------------------------------------------------------------
    def efectuarDisparo(self,ang,vel):
        #print("---------------------------------------------------------------")
        #print("Turno jugador: ",self.jugadorActual.nombre)
        angulo = ang#int(input("Ingrese su angulo: "))
        velocidad = vel#int(input("Ingrese su potencia: "))
        
        delta = 0
        cuadrado = self.jugadorActual.tanque.bloque
        self.jugadorActual.tanque.bala.activaProyectil() 
        disparoTrayectoria=[] 
        while delta <= 20: 
            #los "+21 y +1" evitan que el proyectil toque su propio tanque NO TOCAR"
            xDisparo = cuadrado.x+21 + delta * velocidad * math.cos(angulo * 3.1416 / 180) 
            yDisparo = cuadrado.y+1 - (delta * velocidad * math.sin(angulo * 3.1416 / 180) - (9.81 * delta * delta) / 2) 
            disparoTrayectoria.append((xDisparo,yDisparo)) 
            delta += 0.05 
            #descomentar si quieren debuguear la trayectoria 
            #pygame.draw.circle(self.director.pantalla, (0, 255, 0), (xDisparo, yDisparo),1) 
        return disparoTrayectoria
         # cambia de jugadorActual al otro jugador
    
    
    def dispara(self): #dispara el jugador actual y muestra trayectoria #copiada en on_draw (sacar)
        iteradorBala = self.director.iterador * 10  # fijo, no sacar
        trayectoria=self.efectuarDisparo(self.angulo,self.velocidad) #deberia pedir pantalla pero no pa no la quiere #además de efectuar disparo deja su trayectoria (no borrar)
        #print(trayectoria) #debug
        CoordenadaTrayectoriaActual=trayectoria[(iteradorBala)] 
        self.jugadorActual.tanque.bala.activaProyectil()
        self.jugadorActual.tanque.bala.sigueTrayectoria(CoordenadaTrayectoriaActual)

    def cambioDeTurno(self):
        self.cambiarJugador()
    # permite el cambio de turno entre los dos jugadores (no para n jugadores, sólo sirve para la entrega)
    
    
    def cambiarJugador(self):
        listaJugadoresActuales=self.partidaActual.jugadoresActivos
        if(self.jugadorActual==listaJugadoresActuales[0]):
            self.jugadorActual=listaJugadoresActuales[1]
        else:
            self.jugadorActual=listaJugadoresActuales[0]

    # verifica si un bloque de tierra fue impactado, si lo fue retorna true, en caso contrario false
    def colisionTierra(self,xDisparo,yDisparo):
        bloquesTierra=self.mapa.listaBloques
        for bloque in bloquesTierra:
            if(bloque.colision(xDisparo,yDisparo)):
                return True # toca tierra y para el impacto
        return False # permanece en el rango correcto

    # verifica si un borde del mapa fue impactado, si lo fue retorna true, en caso contrario false
    def saleLimites(self,xDisparo,yDisparo):
        if(xDisparo>=1280 or yDisparo>=730 or xDisparo<=0 or yDisparo<=0):
            return True #sale del rango
        return False #dentro del rango

    # verifica si un tanque fue impactado, retorna true si lo fue, en caso contrario false (aun no elimina al tanque)
    # ni menos lo saca del juego, sólo detecta el impacto
    def colisionTanque(self,xDisparo,yDisparo):
        for jugador in self.partidaActual.jugadoresActivos:
            bloqueTanque=jugador.tanque.bloque
            if(bloqueTanque.colision(xDisparo,yDisparo)):
                self.final=True
                return True # si el tanque fue impactado
        return False # si ningun tanque de un jugador fue impactado

    def dibujarTanques(self):
        for jugador in self.partidas[0].jugadoresActivos:
            jugador.tanque.bloque.dibujar()

# ----- keke metodos -----#
    def muestreoVelocidadAngulo(self):
        fuente = pygame.font.SysFont("arial", 20)
        text = "angulo: %d °   velocidad: %d (m/s)" % (self.angulo, self.velocidad) 
        mensaje = fuente.render(text, 1, (255, 255, 255))
        self.director.pantalla.blit(mensaje, (15, 5))
    def mensajeFinal(self):
        fuente = pygame.font.SysFont("arial", 30)
        text = "FIN DEL JUEGO"
        mensaje = fuente.render(text, 1, (255, 0, 0))
        self.director.pantalla.blit(mensaje, (450, 300))

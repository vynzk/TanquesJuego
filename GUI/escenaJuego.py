#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import math
from GUI import plantillaEscena
from GUI import bloque
from Mapa import Mapa


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
        self.angulo , self.velocidad = 35 , 5 #no tocar
        self.flag = False #confirma si el jugador actual puede disparar
    def on_update(self):  # <<<<<<<<<<<<<<<<<<<<< ACA QUEDA LA CAGÁ
        pygame.display.set_caption("EL JUEGO DE LOS TANQUES IMPLEMENTADO EN PYTHON SIN NOMBRE AUN")
        #pygame.display.update()
        #prueba de eventos
        
       



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
                print("flag: true")
                self.flag= True
            if event.key == pygame.K_TAB:
                print("tab: cambia de turno")
                print("flag: false")
                self.cambioDeTurno()
                self.flag = False

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        # pantalla.fill((0,0,0)) #relleno de pantalla importante en el bucle.
        
        self.director.pantalla.blit(self.fondo, (0, 0))
        self.muestreoVelocidadAngulo() #dibuja la velocidad y el angulo elegido por el usuario
        self.piso.dibujar()
        self.mapa.dibujar(self.director.pantalla)
        self.dibujarTanques()
        if (self.flag == True):
            self.dispara()




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
    def efectuarDisparo(self,ang,vel):
        print("---------------------------------------------------------------")
        print("Turno jugador: ",self.jugadorActual.nombre)
        self.flag=False
        delta = 0
        angulo = ang#int(input("Ingrese su angulo: "))
        velocidad = vel#int(input("Ingrese su potencia: "))
        cuadradoJugador = self.jugadorActual.tanque.bloque

        tanquePos= (self.jugadorActual.tanque.x,self.jugadorActual.tanque.y) #posición del tanque del jugador actual (no borrar)
        self.jugadorActual.tanque.bala.activaProyectil(tanquePos) #activa el OBJETO proyectil
        trayectoria=[] #coordenadas para el lanzamiento de la clase proyectil (no borrar)
        while True:
            # el +10 en xDisparo es para que parta desde la mitad de la parte superior del tanque
            xDisparo = cuadradoJugador.x+10 + delta * velocidad * math.cos(angulo * 3.1416 / 180)
            # el -1 es para que no impacte el primer disparo del cañon con si mismo (la bala sale de este), si lo quitas
            # la parabola no se dibuja ya que interpreta que se tocó a si mismo (cuando sale la bala)
            yDisparo = cuadradoJugador.y-1 - (delta * velocidad * math.sin(angulo * 3.1416 / 180) - (9.81 * delta * delta) / 2)
            delta += 0.01 # si quieres que hayan más puntitos en la parabola, modifica esto
            # hay que transformarlos a int
            xDisparo = int(xDisparo)
            yDisparo = int(yDisparo)
            
            trayectoria.append((xDisparo,yDisparo)) #coordenadas para el lanzamiento del proyectil (no borrar)
            
            print("debería dibujar una pelota en: (", xDisparo, ",", yDisparo, ")")  # debug
            pygame.draw.circle(self.director.pantalla, (0, 255, 0), (xDisparo, yDisparo),1) #comentable

            #----------------------------------VERIFICAR SI TOCA BLOQUES-----------------------------------------------
            if(self.colisionTierra(xDisparo,yDisparo)): # si impacta un bloque de tierra, se detiene la parabola (bala)
                print("toqué tierra")
                return trayectoria
                break;
            elif(self.saleLimites(xDisparo,yDisparo)): # si impacta con un borde, se detiene la parabola (bala)
                print("salí rango")
                return trayectoria
                break;
            elif(self.colisionTanque(xDisparo,yDisparo)): # si impacta con un tanque, se detiene la parabola (bala)
                print("toqué un tanque")
                return trayectoria
                break;
            #--------------------------------------------------------------------------------------------------------
        return trayectoria
         # cambia de jugadorActual al otro jugador
    
    
    def dispara(self): #dispara el jugador actual y muestra trayectoria
        iteradorBala = self.director.iterador * 10  # fijo, no sacar
        trayectoria=self.efectuarDisparo(self.angulo,self.velocidad) #deberia pedir pantalla pero no pa no la quiere #además de efectuar disparo deja su trayectoria (no borrar)
        CoordenadaTrayectoriaActual=trayectoria[(iteradorBala)] 
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
                return True # si el tanque fue impactado
        return False # si ningun tanque de un jugador fue impactado

    def dibujarTanques(self):
        for jugador in self.partidas[0].jugadoresActivos:
            jugador.tanque.bloque.dibujar()

# ----- keke metodos -----#
    def muestreoVelocidadAngulo(self):
        fuente = pygame.font.SysFont("arial", 20)
        text = "angulo: %d °   velocidad: %d (m/s)" % (self.angulo, self.velocidad) #primer %3d
        mensaje = fuente.render(text, 1, (255, 255, 255))
        self.director.pantalla.blit(mensaje, (15, 5))
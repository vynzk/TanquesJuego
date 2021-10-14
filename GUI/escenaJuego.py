#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from GUI.escenaRegistro import EscenaRegistro
import pygame
import math
from GUI import plantillaEscena
import time
from GUI.colores import *
from GUI.Boton import Boton
from GUI.escenaCambioArma import EscenaCambioArma
from Tanque.Tanque import *
import random


class EscenaJuego(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.fondo = pygame.image.load("GUI/imagenes/fondoDespejado.png")  # se asigna un fondo a la escena juego
        self.partidas = self.director.game.listaPartidas
        # para esta entrega hay solo una partida y 2 jugadores, por tanto:
        # la partida inicial será la primera partida (De momento es la única)
        self.partidaActual = self.partidas[0]
        # como tambien, el jugador inicial será el primer jugador activo de la primera partida
        self.jugadorActual = self.partidaActual.jugadoresActivos[0]
        self.trayectoria = []
        self.contador = 0
        self.flag = False
        self.jugadorImpactado = None
        self.xMaxDisparo = 0
        self.yMaxDisparo = 0
        self.boton_salir = None
        self.boton_reiniciar = None
        self.boton_cambioArmas = None

    def on_update(self):
        pygame.display.set_caption("NORTHKOREA WARS SIMULATOR")
        self.director.pantalla.blit(self.fondo, (0, 0))
        self.muestreoTurnoVelocidadAngulo()
        pygame.draw.rect(self.director.pantalla, NEGRO, (0, 600, 1280, 120))  # bloque inferior
        self.partidaActual.mapa.dibujarMapa(self.director.pantalla)
        self.muestreoRastreoBala()
        self.dibujarTanques()
        self.mostrarCañon()
        self.muestreoVidaTanques()
        self.muestreoProyectilActual()

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_salir):
                self.director.running=False; # rompe el ciclo gameLoop y sale del juego
            if self.director.checaBoton(self.director.mousePos, self.boton_reiniciar):
                self.reiniciarPartida()
            if self.director.checaBoton(self.director.mousePos, self.boton_cambioArmas):
                print("funciona boton armas")

                # ---- NUEVO CODIGO ----# #ES PROBABLE QUE FALLEN LOS BOTONES EN ESCENA JUEGO POR LA INTERACCION DE OTROS EVENTOS
                self.ventanaArmas()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.jugadorActual.tanque.velocidad -= 1
                # print("potencia: ", self.jugadorActual.tanque.potencia, "; left: potencia --") # debug
            if event.key == pygame.K_RIGHT:
                self.jugadorActual.tanque.velocidad += 1
                # print("potencia: ", self.jugadorActual.tanque.potencia, "; right: potencia ++") # debug
            if event.key == pygame.K_UP:
                if self.jugadorActual.tanque.angulo + 1 < 180:  # si no verificamos, cualquier angulo fuera de este, el proyectil impacta con el propio tanque
                    self.jugadorActual.tanque.angulo += 1
                # print("angulo: ", self.jugadorActual.tanque.angulo, "; up: angulo ++") # debug
            if event.key == pygame.K_DOWN:
                if self.jugadorActual.tanque.angulo - 1 > 0:
                    self.jugadorActual.tanque.angulo -= 1
                # print("angulo: ", self.jugadorActual.tanque.angulo, "; down: angulo --") # debug
            if event.key == pygame.K_c:
                self.jugadorActual.tanque.cambiarProyectil()
            if event.key == pygame.K_SPACE:
                if self.jugadorActual.tanque.proyectilActual.stock > 0:  # posee balas suficientes
                    self.flag = True
                    print("\n--------------ACCION TURNO-------------------------")
                    print(f'Balas antes del arma actual: {self.jugadorActual.tanque.proyectilActual.stock}')  # debug
                    print(">>> jugador/a ", self.jugadorActual.nombre, " disparó")
                    self.jugadorActual.tanque.proyectilActual.stock -= 1  # se le resta una bala ya que disparó
                    print(f'Balas después del arma actual: {self.jugadorActual.tanque.proyectilActual.stock}')  # debug
                else:
                    self.mensajeSinBalas()
                    print(f'Tu proyectil actual no tiene suficientes balas')

    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""

    def on_draw(self, pantalla):
        if self.director.game.juegoTerminado is not True:
            self.boton_salir = Boton(pantalla, "salir", 1160, 0)
            self.boton_salir.dibujaBoton()
            self.boton_reiniciar = Boton(pantalla, "restaurar", 1030, 0)
            self.boton_reiniciar.dibujaBoton()
            self.boton_cambioArmas = Boton(pantalla, "Armas", 1150, 660)
            self.boton_cambioArmas.dibujaBoton()
            # si tiene más de un jugador activo la partida, sigue la partida jugandose
            if len(self.partidaActual.jugadoresActivos) > 1:
                if self.flag:
                    if self.trayectoria == []:
                        self.efectuarDisparo()
                    else:
                        if self.contador < len(self.trayectoria):
                            self.dibujarBala()
                        else:
                            self.limpiarTurno() # se limpian las estadisticas
                            self.cambiarJugador()
                            self.mensajeTurno()
            else:
                self.partidaActual.terminar()
                self.mensajeFinPartida()  # como es una partida de momento, si gana la partida gana el juego
                self.director.game.definirGanador()  # << invocamos que defina un ganador del juego
                # Nota: el metodo anterior cambia el estado de juegoTerminado a True, por tanto, rompe el gameLoop
                # en el director.
        else:
            self.mensajeFinJuego()
            self.director.running = False  # rompe el gameloop para terminar el juego

    # ------------------------------FUNCIONES QUE REPRESENTAN ACCIONES DENTRO DEL JUEGO-----------------------------
    # Toma las posiciones de la bala y va viendo los posibles escenarios para buscar los valores maximos.
    def rastreoBala(self, xDisparo, yDisparo):
        if (self.xMaxDisparo > xDisparo and self.yMaxDisparo > yDisparo):
            return {self.xMaxDisparo, self.yMaxDisparo}
        elif (self.xMaxDisparo > xDisparo and self.yMaxDisparo < yDisparo):
            self.yMaxDisparo = yDisparo
        elif (self.xMaxDisparo < xDisparo and self.yMaxDisparo > yDisparo):
            self.xMaxDisparo = xDisparo
            return {self.xMaxDisparo, self.yMaxDisparo}
        else:
            self.xMaxDisparo = xDisparo
            self.yMaxDisparo = yDisparo
            return {self.xMaxDisparo, self.yMaxDisparo}

    def efectuarDisparo(self):
        delta = 0
        self.xMaxDisparo = 0
        self.yMaxDisparo = 0
        xJugador = self.jugadorActual.tanque.bloque.x
        yJugador = self.jugadorActual.tanque.bloque.y
        while True:
            xDisparo = int(xJugador + 20 + delta * self.jugadorActual.tanque.velocidad * math.cos(
                self.jugadorActual.tanque.angulo * 3.1416 / 180))
            yDisparo = int(yJugador - 1 - (
                    delta * self.jugadorActual.tanque.velocidad * math.sin(
                self.jugadorActual.tanque.angulo * 3.1416 / 180) - (9.81 * delta * delta) / 2))
            delta += 0.1  # si quieres que hayan más puntitos en la parabola, modifica esto
            self.rastreoBala(xDisparo, yDisparo)
            self.trayectoria.append((xDisparo, yDisparo))
            # ----------------------------------VERIFICAR SI TOCA BLOQUES-----------------------------------------------
            jugadorImpactado = self.colisionTanque(xDisparo, yDisparo)
            if jugadorImpactado is not None:  # si impacta con un tanque, se detiene la parabola (bala)
                print("proyectil: toqué un tanque")  # debug
                self.jugadorImpactado = jugadorImpactado
                break

            elif self.colisionTierra(xDisparo, yDisparo):
                print("proyectil: toqué tierra")  # debug
                break

            elif self.saleLimites(xDisparo, yDisparo):  # si impacta con un borde, se detiene la parabola (bala)
                print("proyectil: salí rango")  # debug
                break

    def cambiarJugador(self):
        listaJugadoresActuales = self.partidaActual.jugadoresActivos
        if self.jugadorActual == listaJugadoresActuales[0]:
            self.jugadorActual = listaJugadoresActuales[1]
        else:
            self.jugadorActual = listaJugadoresActuales[0]

    # ----------------------------------FUNCIONES QUE VERIFICAN COLISIÓN---------------------------------------------
    # verifica si un bloque de tierra fue impactado, si lo fue retorna true, en caso contrario false
    def colisionTierra(self, xDisparo, yDisparo):
        bloquesTierra = self.partidaActual.mapa.listaBloques
        for bloque in bloquesTierra:
            if bloque.colision(xDisparo, yDisparo):
                return True  # toca tierra y para el impacto
        return False  # permanece en el rango correcto

    # verifica si un borde del mapa fue impactado, si lo fue retorna true, en caso contrario false
    def saleLimites(self, xDisparo, yDisparo):
        if xDisparo >= 1280 or yDisparo >= 730 or xDisparo <= 0 or yDisparo <= 0:
            return True  # sale del rango
        return False  # dentro del rango

    # verifica si un tanque fue impactado, retorna true si lo fue, en caso contrario false (aun no elimina al tanque)
    # ni menos lo saca del juego, sólo detecta el impacto
    def colisionTanque(self, xDisparo, yDisparo):
        for jugador in self.partidaActual.jugadoresActivos:
            bloqueTanque = jugador.tanque.bloque
            if bloqueTanque.colision(xDisparo, yDisparo):
                return jugador  # si el tanque fue impactado
        return None  # si ningun tanque de un jugador fue impactado

    # ---------------------------------FUNCIONES QUE DIBUJAN EN LA ESCENA------------------------------------------
    def dibujarTanques(self):
        for jugador in self.partidas[0].jugadoresActivos:
            jugador.tanque.bloque.dibujar()

    def dibujarBala(self):
        coord = self.trayectoria[self.contador]
        # dibuja el proyectil (el color dependerá de que clase de proyectil es)
        pygame.draw.circle(self.director.pantalla, self.jugadorActual.tanque.proyectilActual.color,
                           (coord[0], coord[1]), 3)
        self.contador += 1
        if self.contador == len(self.trayectoria):
            if self.jugadorImpactado is not None:
                dañoEfectuado = self.jugadorActual.tanque.proyectilActual.daño
                if dañoEfectuado >= self.jugadorImpactado.tanque.vida:
                    print(
                        f'<<< el jugador/a {self.jugadorImpactado.nombre} ha sido eliminado por {self.jugadorActual.nombre}')
                    self.partidaActual.eliminarJugador(self.jugadorImpactado)  # elimina al jugador
                else:
                    print(
                        f'<<< el jugador/a {self.jugadorImpactado.nombre} ha sido impactado por {self.jugadorActual.nombre}, le ha quitado {dañoEfectuado} vida')
                    # se le resta la vida del arma del jugador contrario
                    self.jugadorImpactado.tanque.vida -= dañoEfectuado
        pygame.time.wait(0)

    # ----------------------------------METODOS QUE MUESTRAN TEXTO-------------------------------------------------
    def mensajeTurno(self):
        fuente = pygame.font.SysFont("arial", 30, bold=True)
        text = "TURNO: " + str.upper(self.jugadorActual.nombre)
        mensaje = fuente.render(text, 1, NEGRO)
        self.director.pantalla.blit(mensaje, (450, 300))
        pygame.display.update()
        time.sleep(2)

    def mensajeFinPartida(self):
        fuente = pygame.font.SysFont("arial", 30, bold=True)
        jugadorGanador = self.partidaActual.jugadorGanador
        text = "FIN DE PARTIDA ; GANADOR: " + str.upper(jugadorGanador.nombre)
        mensaje = fuente.render(text, 1, NEGRO)
        self.director.pantalla.blit(mensaje, (450, 300))
        pygame.display.update()
        time.sleep(1)

    def mensajeSinBalas(self):
        fuente = pygame.font.SysFont("arial", 30, bold=True)
        text = "NO TIENES BALAS SUFICIENTES, CAMBIA DE ARMA"
        mensaje = fuente.render(text, 1, NEGRO)
        self.director.pantalla.blit(mensaje, (450, 300))
        pygame.display.update()
        time.sleep(2)

    def mensajeFinJuego(self):
        fuente = pygame.font.SysFont("arial", 30, bold=True)
        jugadorGanador = self.director.game.jugadorGanador
        text = "FIN DEL JUEGO ; GANADOR: " + str.upper(jugadorGanador.nombre)
        mensaje = fuente.render(text, 1, NEGRO)
        self.director.pantalla.blit(mensaje, (450, 400))
        pygame.display.update()
        time.sleep(3)

    def muestreoTurnoVelocidadAngulo(self):
        fuente = pygame.font.SysFont("arial", 20, bold=True)
        text = "Jugador actual: %s ; angulo: %d ° ; velocidad: %d (m/s)" % (
            self.jugadorActual.nombre, self.jugadorActual.tanque.angulo, self.jugadorActual.tanque.velocidad)
        mensaje = fuente.render(text, 1, BLANCO)
        self.director.pantalla.blit(mensaje, (15, 5))

    # Define el mensaje a mostrar en pantalla junto a sus caracteristicas.
    def muestreoRastreoBala(self, bold=True):
        fuente = pygame.font.SysFont("arial", 20, bold=True)

        conversionPxCm = 265 / 10000  # Conversion de pixel a cm ;1 px --> 0,0265 cm

        text = f'Estado disparo {self.flag} ; Desplazamiento: {int(self.xMaxDisparo * conversionPxCm)} [cm] ; Altura maxima: {int(self.yMaxDisparo * conversionPxCm)} [cm]'
        mensaje = fuente.render(text, 1, BLANCO)
        self.director.pantalla.blit(mensaje, (15, 30))

    # Se muestra el cañon para dar una aproximación del angulo a la hora de efectuar el disparo
    def mostrarCañon(self):
        for jugador in self.partidaActual.jugadoresActivos:
            tanque = jugador.tanque
            angulo = tanque.angulo * 3.1416 / -180
            x = tanque.bloque.x + 20
            y = tanque.bloque.y
            pygame.draw.line(self.director.pantalla, NEGRO, [x, y],
                             [x + 50 * math.cos(angulo), y + 50 * math.sin(angulo)], 5)

    def muestreoVidaTanques(self):
        for jugador in self.partidaActual.jugadoresActivos:
            fuente = pygame.font.SysFont("arial", 15, bold=True)
            # se pasan a int ya que son numeros decimales y luego ello se pasa a str para concatenar en un sólo string
            text = str(f'HP: {jugador.tanque.vida}')
            mensaje = fuente.render(text, 1, NEGRO)
            self.director.pantalla.blit(mensaje, (jugador.tanque.x, jugador.tanque.y + 40))

    def muestreoProyectilActual(self):
        fuente = pygame.font.SysFont("arial", 20, True)
        # se pasan a int ya que son numeros decimales y luego ello se pasa a str para concatenar en un sólo string
        proyectilJugActual = self.jugadorActual.tanque.proyectilActual
        text = "Arma actual: " + str(proyectilJugActual.__class__) + "; balas: " + str(
            proyectilJugActual.stock) + "; daño: " + str(proyectilJugActual.daño)
        mensaje = fuente.render(text, 1, BLANCO)
        self.director.pantalla.blit(mensaje, (15, 55))

    # ----------------------------------METODOS BOTONES-----------------------------------------------------------
    def ventanaArmas(self):
        self.director.cambiarEscena(EscenaCambioArma(self.director))

    """
    def escenaSeguro(self):
        reiniciarPartida();
        #self.director.cambiarEscena(EscenaSeguro(self.director,self.partidaActual))
    """

    def limpiarTurno(self):
        self.jugadorImpactado = None  # << se limpia
        # self.bloqueImpactado = None
        self.contador = 0  # << el contador debe estar limpio para un nuevo jugador
        self.trayectoria = []  # << la trayectoria debe estar limpio para un nuevo jugador
        self.flag = False  # << debe apretar enter nuevamente el jugador para disparar
        self.xMaxDisparo = 0
        self.yMaxDisparo = 0

    # cuando se cambia de partida o se crea una nueva, el jugador no puede tener el mismo tanque de la partida
    # anterior, por tanto, deben crearse nuevos
    def asignarNuevosTanques(self):
        listaImagenesTanque = ["GUI/imagenes/bloque/tanqueGris.png", "GUI/imagenes/bloque/tanqueAmarillo.png",
                               "GUI/imagenes/bloque/tanqueCeleste.png", "GUI/imagenes/bloque/tanqueRojo.png",
                               "GUI/imagenes/bloque/tanqueVerde.png"]

        for jugador in self.partidaActual.jugadoresActivos:
            numAleatorio=random.randint(0,len(listaImagenesTanque)-1)
            imagenTanqueAleatoria=listaImagenesTanque[numAleatorio]
            nuevoTanque=Tanque(self.director.pantalla,imagenTanqueAleatoria)
            jugador.tanque=nuevoTanque             
        
    # cuando se presiona el boton de reiniciar, se debe crear una nueva partida que remplace la partida actual
    def reiniciarPartida(self):
        # creo la nueva partida
        nuevaPartida=self.director.game.agregarPartida(self.partidaActual.id,self.director)
        self.asignarNuevosTanques() 

        # se cambia en la lista partidas 
        self.director.game.listaPartidas[self.partidaActual.id-1]=nuevaPartida
        
        # se actualiza la nueva lista
        self.partidas=self.director.game.listaPartidas

        # se remplaza la partida recién creada por la partida actual
        self.partidaActual=self.partidas[0]
        self.jugadorActual=self.partidaActual.jugadoresActivos[0]

        # deben regenerarse las posiciones de los tanques y equiparle las armas
        self.partidaActual.generarPosicionesJug()
        self.partidaActual.equiparArmasIniciales()

        # se limpian las estadisticas
        self.limpiarTurno() 
      
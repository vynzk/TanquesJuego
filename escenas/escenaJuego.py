#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from GUI.escenaRegistro import EscenaRegistro
import pygame
import math
from escenas import plantillaEscena
from Mapa.listasEscenarios import *
from utilidades.colores import *
from utilidades.Boton import Boton
from escenas.escenaCambioArma import EscenaCambioArma
from Tanque.Tanque import *
import random
from escenas.escenaAyuda import EscenaAyuda



class EscenaJuego(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.fondo = fondosLista[random.randint(0,len(fondosLista)-1)]
        self.fondo = pygame.transform.scale(self.fondo, (1280,720) )
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
        self.bloqueImpactado = None
        self.xMaxDisparo = 0
        self.yMaxDisparo = 0
        self.boton_salir = None
        self.boton_reiniciar = None
        self.boton_cambioArmas = None
        self.boton_ayuda = None


    def on_update(self):
        pygame.display.set_caption("NORTHKOREA WARS SIMULATOR")
        self.director.pantalla.blit(self.fondo, (0, 0))
        pygame.draw.rect(self.director.pantalla, NEGRO, (0, 600, 1280, 120))  # barra inferior inferior
        self.partidaActual.mapa.dibujarMapa(self.director.pantalla)
        self.dibujarTanques()
        self.mostrarCañon()
        self.muestreoVidaTanques()



    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.director.mousePos = pygame.mouse.get_pos()
            if self.director.checaBoton(self.director.mousePos, self.boton_salir):
                self.director.running = False;  # rompe el ciclo gameLoop y sale del juego
            if self.director.checaBoton(self.director.mousePos, self.boton_reiniciar):
                self.reiniciarPartida()
            if self.director.checaBoton(self.director.mousePos, self.boton_cambioArmas):
                self.cambiarEscenaArmas()
            if self.director.checaBoton(self.director.mousePos, self.boton_ayuda):
                self.cambiarEscenaAyuda()

        pygame.key.set_repeat(10, 20)
        if event.type == pygame.KEYDOWN and self.flag is False:
            if event.key == pygame.K_SPACE:
                pygame.key.set_repeat()
                if self.jugadorActual.tanque.proyectilActual.municion > 0:  # posee balas suficientes
                    self.flag = True
                    self.jugadorActual.tanque.proyectilActual.municion -= 1  # se le resta una bala ya que disparó
                else:
                    # se muestra mensaje que no posee balas
                    self.textoEnPantalla(f'NO TIENES BALAS SUFICIENTES, CAMBIA DE ARMA',30,BLANCO,(450,300),True)
            
            
            if event.key == pygame.K_LEFT:
                pygame.key.set_repeat(1,50)
                if(200> self.jugadorActual.tanque.velocidad >50):
                    self.jugadorActual.tanque.velocidad -= 1
            if event.key == pygame.K_RIGHT:
                pygame.key.set_repeat(1,50)
                if(200>= self.jugadorActual.tanque.velocidad >50):
                    self.jugadorActual.tanque.velocidad += 1
            if event.key == pygame.K_UP:
                if self.jugadorActual.tanque.angulo + 1 < 180:  # si no verificamos, cualquier angulo fuera de este, el proyectil impacta con el propio tanque
                    self.jugadorActual.tanque.angulo += 1
            if event.key == pygame.K_DOWN:
                pygame.key.set_repeat(1, 50)
                if self.jugadorActual.tanque.angulo - 1 > 0:
                    self.jugadorActual.tanque.angulo -= 1


    """Esta función corresponde a lo mostrado en pantalla: usada en director.py"""
    def on_draw(self, pantalla):
        if self.director.game.juegoTerminado is not True:
            # si tiene más de un jugador activo la partida, sigue la partida jugandose
            if len(self.partidaActual.jugadoresActivos) > 1:
                self.contenidoBarraInferior()
                if self.flag:
                    # si al comenzar un turno, ningun jugador tiene balas, empatan
                    if self.empate() is True:
                        print(f'Los jugadores no poseen balas para terminar el juego, EMPATE!')
                        self.director.running=False
                    if self.trayectoria == []:
                        self.efectuarDisparo()
                    else:
                        if self.contador < len(self.trayectoria):
                            self.dibujarBala()
                        else:
                            self.limpiarTurno()  # se limpian las estadisticas
                            self.cambiarJugador()
            else:
                self.partidaActual.terminar()
                # mensaje fin de partida
                self.textoEnPantalla(f'FIN DE PARTIDA, GANADOR: {self.partidaActual.jugadorGanador.nombre}',30,BLANCO,(450,300),True)
                
                self.director.game.definirGanador()  # << invocamos que defina un ganador del juego
                # Nota: el metodo anterior cambia el estado de juegoTerminado a True, por tanto, rompe el gameLoop
                # en el director.
        else:
            # mensaje fin juego
            self.textoEnPantalla(f'FIN DEL JUEGO, GANADOR: {self.director.game.jugadorGanador.nombre})',30,BLANCO,(450,300),True)
            self.director.running = False  # rompe el gameloop para terminar el juego

    # ------------------------------FUNCIONES QUE REPRESENTAN ACCIONES DENTRO DEL JUEGO-----------------------------

    # Toma las posiciones de la bala y va viendo los posibles escenarios para buscar los valores maximos.
    def calcularDesplazamientoAltura(self, xDisparo, yDisparo):
        conversionCmPx=265 / 10000
        """
        Para calcular el desplazamiento, debemos tomar dos puntos dentro del mapa, el cual son la 
        posicion del tanque donde se efectuo el disparo, como tambien, la posicion en x donde llego este
        """
        self.xMaxDisparo=int(abs(xDisparo-self.jugadorActual.tanque.bloque.x)*conversionCmPx)

        """
        Para calcular la altura, se tomara dos puntos dentro del mapa, el cual son la posicion
        del tanque donde se efectuo el disparo, como tambien, la posicion en y donde llego este
        """
        self.yMaxDisparo=int(abs(yDisparo-self.jugadorActual.tanque.bloque.y)*conversionCmPx)

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
            self.trayectoria.append((xDisparo, yDisparo))
            self.calcularDesplazamientoAltura(xDisparo,yDisparo)
            # ----------------------------------VERIFICAR SI TOCA BLOQUES-----------------------------------------------
            jugadorImpactado = self.colisionTanque(xDisparo, yDisparo)
            bloqueImpactado = self.colisionTierra(xDisparo, yDisparo)

            if jugadorImpactado is not None:  # si impacta con un tanque, se detiene la parabola (bala)
                self.jugadorImpactado = jugadorImpactado
                break

            elif self.colisionTierra(xDisparo, yDisparo):
                self.bloqueImpactado = bloqueImpactado
                break

            elif self.tocaBordes(xDisparo, yDisparo):  # si impacta con un borde, se detiene la parabola (bala)
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
                return bloque
        return None

    # verifica si un borde del mapa fue impactado, si lo fue retorna true, en caso contrario false
    def tocaBordes(self, xDisparo, yDisparo):
        if xDisparo >= 1280 or yDisparo >= 600 or xDisparo <= 0 or yDisparo <= 0:
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
                    self.partidaActual.eliminarJugador(self.jugadorImpactado)  # elimina al jugador
                else:
                    # se le resta la vida del arma del jugador contrario
                    self.jugadorImpactado.tanque.vida -= dañoEfectuado
            if self.bloqueImpactado is not None:
                # destruirá el bloque actual y la zona según el daño del proyectil
                self.destruirZonaImpacto(self.bloqueImpactado,self.jugadorActual.tanque.proyectilActual.nombre)

        pygame.time.wait(0)

    # Se muestra el cañon para dar una aproximación del angulo a la hora de efectuar el disparo
    def mostrarCañon(self):
        for jugador in self.partidaActual.jugadoresActivos:
            tanque = jugador.tanque
            angulo = tanque.angulo * 3.1416 / -180
            x = tanque.bloque.x + 20
            y = tanque.bloque.y
            pygame.draw.line(self.director.pantalla, BLANCO, [x, y],
                             [x + 50 * math.cos(angulo), y + 50 * math.sin(angulo)], 5)

    def muestreoVidaTanques(self):
        for jugador in self.partidaActual.jugadoresActivos:
            fuente = pygame.font.SysFont("arial", 15, bold=True)
            # se pasan a int ya que son numeros decimales y luego ello se pasa a str para concatenar en un sólo string
            text = str(f'HP: {jugador.tanque.vida}')
            mensaje = fuente.render(text, 1, BLANCO)
            self.director.pantalla.blit(mensaje, (jugador.tanque.x, jugador.tanque.y + 40))

    def contenidoBarraInferior(self):
        # Información
        self.textoEnPantalla(f'INFORMACIÓN TURNO ACTUAL',25,BLANCO,(20,610),False)
        self.textoEnPantalla(f'Angulo: {self.jugadorActual.tanque.angulo}°',20,BLANCO,(500,610),False)
        self.textoEnPantalla(f'Velocidad: {self.jugadorActual.tanque.velocidad} [cm/s]',20,BLANCO,(650,610),False)

        self.mostrarImagenEnPos(self.jugadorActual.tanque.imagen,(50,50),(20,660))
        self.textoEnPantalla(f'Nombre jugador: {self.jugadorActual.nombre}',20,BLANCO,(80,660),False)
        self.textoEnPantalla(f'Vida tanque: {self.jugadorActual.tanque.vida}',20,BLANCO,(80,690),False)

        #self.mostrarImagenEnPos(self.jugadorActual.tanque.proyectilActual.imagen,(50,50),(20,660))
        self.textoEnPantalla(f'Arma equipada: {self.jugadorActual.tanque.proyectilActual.nombre}',20,BLANCO,
                             (300,660),False)
        self.textoEnPantalla(f'Munición: {self.jugadorActual.tanque.proyectilActual.municion},'
                             f' Daño: {self.jugadorActual.tanque.proyectilActual.daño}',20,BLANCO,(300,690),False)

        self.textoEnPantalla(f'Desplazamiento máxima: {self.xMaxDisparo} [cm]',20,BLANCO,(600,660),False)
        self.textoEnPantalla(f'Altura máxima máxima: {self.yMaxDisparo} [cm]',20,BLANCO,(600,690),False)

        # Botones
        botonSalir=pygame.image.load("imagenes/botones/botonSalir.png")
        botonReiniciar=pygame.image.load("imagenes/botones/botonReiniciar.png")
        botonCambioArmas=pygame.image.load("imagenes/botones/botonMochila.png")
        botonAyuda=pygame.image.load("imagenes/botones/botonMochila.png")

        self.boton_salir = Boton(self.director.pantalla, "Salir", 1100, 670 ,botonSalir,127,40)
        self.boton_salir.dibujaBoton()

        self.boton_reiniciar = Boton(self.director.pantalla, "Reiniciar", 1100, 610, botonReiniciar,127,40)
        self.boton_reiniciar.dibujaBoton()

        self.boton_cambioArmas = Boton(self.director.pantalla, "Armas", 950, 670, botonCambioArmas,127,40)
        self.boton_cambioArmas.dibujaBoton()

        self.boton_ayuda = Boton(self.director.pantalla, "Ayuda", 950, 610, botonAyuda,127,40)
        self.boton_ayuda.dibujaBoton()

    #----------------------------------_DESTRUCCION DE TIERRA ---------------------------------------
    def buscarBloque(self, x, y):
        for bloque in self.partidaActual.mapa.listaBloques:
            if bloque.x == x and bloque.y == y:
                return bloque
        return None

    def buscarTanque(self, x, y):
        for jugador in self.partidaActual.jugadoresActivos:
            if jugador.tanque.bloque.x==x and jugador.tanque.bloque.y==y:
                return jugador.tanque.bloque
        return None

    def destruir(self, bloque):
        # si existe dentro de la lista de bloques
        if bloque is not None:
            self.partidaActual.mapa.listaBloques.remove(bloque)

            bloqueQueCae=bloque
            contador=40
            while(True):
                bloqueSup=self.buscarBloque(bloque.x,bloque.y-contador)

                # si el bloque removido tenía un bloque arriba 
                if bloqueSup is not None:
                    bloqueSup.y=bloqueQueCae.y
                    bloqueQueCae=bloqueSup
                    contador+=40
                else:
                    bloqueTanqueSup=self.buscarTanque(bloque.x,bloque.y-contador)
                    if bloqueTanqueSup is not None:
                        bloqueTanqueSup.y=bloque.y-contador+40
                    break

    def destruirZonaImpacto(self, bloqueImpactado,  nombreArma):
        # animación de impacto
        self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png",(40,40),(self.bloqueImpactado.x,self.bloqueImpactado.y))
        pygame.display.update()
        self.destruir(bloqueImpactado)  # todos rompen el bloque de impacto

        if nombreArma != "Proyectil 60":
            self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png",(40,40),(self.bloqueImpactado.x-40,self.bloqueImpactado.y))
            self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png",(40,40),(self.bloqueImpactado.x+40,self.bloqueImpactado.y))
            bloqueIzquierda = self.buscarBloque(bloqueImpactado.x - 40, bloqueImpactado.y)
            bloqueDerecha = self.buscarBloque(bloqueImpactado.x + 40, bloqueImpactado.y)
            # destrucción de los bloques
            self.destruir(bloqueIzquierda)
            self.destruir(bloqueDerecha)

        if nombreArma == "Proyectil 105":
            pass
            # debe destruir los demás bloques (arriba, abajo, diagonales)
        pygame.time.wait(400) # <-- necesario para que se vean las graficas

    #-----------------------------------DEFINIR EMPATE---------------------------------------------------------
    def empate(self):
        for jugador in self.partidaActual.jugadoresActivos:
            proyectilesJug=jugador.tanque.listaProyectiles
            for proyectil in proyectilesJug:
                if proyectil.municion>0:
                    return False
        return True

    # ----------------------------------METODOS ACCIONADOS POR BOTONES-------------------------------------------
    def cambiarEscenaArmas(self):
        self.director.cambiarEscena(EscenaCambioArma(self.director))

    def cambiarEscenaAyuda(self):
        self.director.cambiarEscena(EscenaAyuda(self.director))

    def reiniciarPartida(self):
        # creo la nueva partida
        nuevaPartida = self.director.game.agregarPartida(self.partidaActual.id, self.director)
        self.asignarNuevosTanques()

        # se cambia en la lista partidas 
        self.director.game.listaPartidas[self.partidaActual.id - 1] = nuevaPartida

        # se actualiza la nueva lista
        self.partidas = self.director.game.listaPartidas

        # se remplaza la partida recién creada por la partida actual
        self.partidaActual = self.partidas[0]
        self.jugadorActual = self.partidaActual.jugadoresActivos[0]

        # deben regenerarse las posiciones de los tanques y equiparle las armas
        self.partidaActual.generarPosicionesJug()
        self.partidaActual.equiparArmasIniciales()

        # se limpian las estadisticas
        self.limpiarTurno()
        #fondo nuevo
        self.fondo = fondosLista[random.randint(0,len(fondosLista)-1)]
        self.fondo = pygame.transform.scale(self.fondo, (1280,720) )

    #----------------------------------METODOS AL CAMBIAR DE TURNO------------------------------------------------
    def limpiarTurno(self):
        self.jugadorImpactado = None  # << se limpia
        self.bloqueImpactado = None
        self.contador = 0  # << el contador debe estar limpio para un nuevo jugador
        self.trayectoria = []  # << la trayectoria debe estar limpio para un nuevo jugador
        self.flag = False  # << debe apretar enter nuevamente el jugador para disparar
        self.xMaxDisparo = 0
        self.yMaxDisparo = 0

    #----------------------------METODOS AL TERMINAR UNA PARTIDA O CREAR UNA NUEVA-----------------------------
    # cuando se cambia de partida o se crea una nueva, el jugador no puede tener el mismo tanque de la partida
    # anterior, por tanto, deben crearse nuevos
    def asignarNuevosTanques(self):
        listaImagenesTanque = ["imagenes/bloque/tanqueGris.png", "imagenes/bloque/tanqueAmarillo.png",
                               "imagenes/bloque/tanqueCeleste.png", "imagenes/bloque/tanqueRojo.png",
                               "imagenes/bloque/tanqueVerde.png"]

        for jugador in self.partidaActual.jugadoresActivos:
            numAleatorio = random.randint(0, len(listaImagenesTanque) - 1)
            imagenTanqueAleatoria = listaImagenesTanque[numAleatorio]
            listaImagenesTanque.remove(imagenTanqueAleatoria)
            nuevoTanque = Tanque(self.director.pantalla, imagenTanqueAleatoria)
            jugador.tanque = nuevoTanque



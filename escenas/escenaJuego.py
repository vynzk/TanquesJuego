#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from GUI.escenaRegistro import EscenaRegistro
import pygame
import math
import time
from escenas import plantillaEscena
from Mapa.listasEscenarios import *
from escenas.escenaCreditos import EscenaCreditos
from utilidades.colores import *
from utilidades.Boton import Boton
from escenas.escenaCambioArma import EscenaCambioArma
from Tanque.Tanque import *
import random
from escenas.escenaAyuda import EscenaAyuda
from Videojuego.Juego import Juego



class EscenaJuego(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)
        self.fondo = fondosLista[random.randint(0,len(fondosLista)-1)]
        self.fondo = pygame.transform.scale(self.fondo, (1280,720) )#El tamaño de la ventana esta en director.ancho y en director.largo
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
        self.boton_infoBala = None
        self.boton_creditos= None


    def on_update(self):
        pygame.display.set_caption("NORTHKOREA WARS SIMULATOR")
        self.director.pantalla.blit(self.fondo, (0, 0))
        
        self.director.pantalla.blit(pygame.image.load('imagenes/banner.png'),(0,600))
        #pygame.draw.rect(self.director.pantalla, NEGRO, (0, 600, 1280, 120))  # barra inferior inferior
        self.partidaActual.mapa.dibujarMapa(self.director.pantalla)
        self.dibujarTanques()
        self.mostrarCañon()
        self.muestreoVidaTanques()
        self.pisoEsLava()
        # self.mostrarLineas() # <--- debug


    def on_event(self, event):
        self.director.mousePos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if self.director.checaBoton(self.director.mousePos, self.boton_salir):
                self.director.running = False  # rompe el ciclo gameLoop y sale del juego
            if self.director.checaBoton(self.director.mousePos, self.boton_reiniciar):
                self.cambiarEscenaRegistro()
                #self.reiniciarPartida()
            if self.director.checaBoton(self.director.mousePos, self.boton_cambioArmas):
                self.cambiarEscenaArmas()
            if self.director.checaBoton(self.director.mousePos, self.boton_ayuda):
                self.cambiarEscenaAyuda()
            if self.director.checaBoton(self.director.mousePos, self.boton_creditos):
                self.cambiarEscenaCreditos()

        if event.type == pygame.KEYDOWN and self.flag is False:
            if event.key == pygame.K_SPACE:
                if self.jugadorActual.tanque.proyectilActual.municion > 0:  # posee balas suficientes
                    self.flag = True
                    self.jugadorActual.tanque.proyectilActual.municion -= 1  # se le resta una bala ya que disparó
                else:
                    # se muestra mensaje que no posee balas
                    self.textoEnPantalla(f'NO TIENES BALAS SUFICIENTES, CAMBIA DE ARMA',30,BLANCO,(300,300),True)


            if event.key == pygame.K_LEFT:             
                if(200> self.jugadorActual.tanque.velocidad >50):
                    self.jugadorActual.tanque.velocidad -= 1
            if event.key == pygame.K_RIGHT:        
                if(200>= self.jugadorActual.tanque.velocidad >50):
                    self.jugadorActual.tanque.velocidad += 1
            if event.key == pygame.K_UP:
                if self.jugadorActual.tanque.angulo + 1 < 180:  # si no verificamos, cualquier angulo fuera de este, el proyectil impacta con el propio tanque
                    self.jugadorActual.tanque.angulo += 1
            if event.key == pygame.K_DOWN:         
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
                        self.textoEnPantalla("EMPATE POR NO TENER BALAS",30,BLANCO,(400,300),True)
                        print(f'Los jugadores no poseen balas para terminar el juego, EMPATE!')
                        time.sleep(5)
                        self.director.running=False
                    if self.trayectoria == []:
                        self.efectuarDisparo()
                    else:
                        if self.contador < len(self.trayectoria):
                            self.dibujarBala()
                        else:
                            self.textoEnPantalla("CAMBIO DE TURNO",30,BLANCO,(500,300),True)
                            self.limpiarTurno()  # se limpian las estadisticas
                            self.cambiarJugador()
            else:
                self.partidaActual.terminar()
                # mensaje fin de partida
                self.textoEnPantalla(f'FIN DE PARTIDA, GANADOR: {self.partidaActual.jugadorGanador.nombre}',30,BLANCO,(400,200),True)
                time.sleep(2)
                self.director.game.definirGanador()  # << invocamos que defina un ganador del juego
                # Nota: el metodo anterior cambia el estado de juegoTerminado a True, por tanto, rompe el gameLoop
                # en el director.
        else:
            # mensaje fin juego
            self.textoEnPantalla(f'FIN DEL JUEGO, GANADOR: {self.director.game.jugadorGanador.nombre}',30,BLANCO,(400,300),True)
            time.sleep(5)
            self.director.running = False  # rompe el gameloop para terminar el juego

    # ------------------------------FUNCIONES QUE REPRESENTAN ACCIONES DENTRO DEL JUEGO-----------------------------

    # Toma las posiciones de la bala y va viendo los posibles escenarios para buscar los valores maximos.
    def calcularDesplazamientoAltura(self, xDisparo, yDisparo):
        conversionCmPx=265 / 10000
        """
        Para calcular el desplazamiento, debemos tomar dos puntos dentro del mapa, el cual son la 
        posicion del tanque donde se efectuo el disparo, como tambien, la posicion en x donde llego este (al final)
        """
        self.xMaxDisparo=int(abs(xDisparo-self.jugadorActual.tanque.bloque.x)*conversionCmPx)

        """
        Para calcular la altura, se tomara dos puntos dentro del mapa, el cual son la posicion
        del tanque donde se efectuo el disparo, como tambien, la posicion en y donde viaja el proyectil
        """
        yDisparoConv=int(abs(yDisparo*conversionCmPx))
        if(yDisparo*conversionCmPx>self.yMaxDisparo):
            self.yMaxDisparo=yDisparoConv

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

    """
    Metodo que pasa de turno al siguiente jugador dentro de la partida, si
    este jugador es el ultimo en la lista de jugadores le pasará el turno
    al primero de la lista. Funciona para n cantidad de jugadores.
    """

    def cambiarJugador(self):
        listaJugadoresPartida = self.partidaActual.jugadoresActivos
        index = listaJugadoresPartida.index(self.jugadorActual)
        if index < len(listaJugadoresPartida) - 1:
            self.jugadorActual = listaJugadoresPartida[index + 1]
        else:  # si llegó al ultimo, le toca al primero
            self.jugadorActual = listaJugadoresPartida[0]

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
                # se muestra la imagen explosion sobre el tanque, para ilustrar el impacto
                self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png",(40,40),
                                        (self.jugadorImpactado.tanque.bloque.x,
                                         self.jugadorImpactado.tanque.bloque.y))
                pygame.time.wait(100)

                dañoEfectuado = self.jugadorActual.tanque.proyectilActual.daño
                if dañoEfectuado >= self.jugadorImpactado.tanque.vida:
                    self.partidaActual.eliminarJugador(self.jugadorImpactado)  # elimina al jugador
                else:
                    # se le resta la vida del arma del jugador contrario
                    self.jugadorImpactado.tanque.vida -= dañoEfectuado
            if self.bloqueImpactado is not None:
                # destruirá el bloque actual y la zona según el daño del proyectil
                self.destruirZonaImpacto(self.bloqueImpactado,self.jugadorActual.tanque.proyectilActual.nombre)
            else:
                # se muestra la imagen explosion con el borde
                self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png",(40,40),(coord[0],coord[1]))
                pygame.time.wait(100)


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
            self.director.pantalla.blit(mensaje, (jugador.tanque.bloque.x, jugador.tanque.bloque.y + 40))

    def contenidoBarraInferior(self):
        # Información
        self.textoEnPantalla(f'Jugador actual: {self.jugadorActual.nombre}',15,BLANCO,(20,605),False)
        self.textoEnPantalla(f'Angulo: {self.jugadorActual.tanque.angulo}',15,BLANCO,(500,610),False)
        self.textoEnPantalla((f'Municion de Bala: ' + str(self.jugadorActual.tanque.proyectilActual.municion)),15,BLANCO,(500,650),False)
        self.textoEnPantalla(f'Velocidad: {self.jugadorActual.tanque.velocidad} [cm/s]',15,BLANCO,(650,610),False)
        cuadroVacioImagen= "imagenes/botones/botonVacio.png"
        self.mostrarImagenEnPos(cuadroVacioImagen,(50,50),(20,640))
        self.mostrarImagenEnPos(self.jugadorActual.tanque.imagen,(30,30),(30,650))
        
        #self.textoEnPantalla(f'Nombre jugador: {self.jugadorActual.nombre}',20,BLANCO,(80,660),False)
        #self.textoEnPantalla(f'Vida tanque: {self.jugadorActual.tanque.vida}',20,BLANCO,(80,690),False)

        #self.mostrarImagenEnPos(self.jugadorActual.tanque.proyectilActual.imagen,(50,50),(20,660))
        #self.textoEnPantalla(f'Arma equipada: {self.jugadorActual.tanque.proyectilActual.nombre}',20,BLANCO,
        #                     (300,660),False)
        #self.textoEnPantalla(f'Munición: {self.jugadorActual.tanque.proyectilActual.municion},'
        #                     f' Daño: {self.jugadorActual.tanque.proyectilActual.daño}',20,BLANCO,(300,690),False)

        self.textoEnPantalla(f'Desplazamiento maximo: {self.xMaxDisparo} [cm]',15,BLANCO,(150,635),False)
        self.textoEnPantalla(f'Altura maxima: {self.yMaxDisparo} [cm]',15,BLANCO,(150,665),False)
        
        

        # Botones
        #infoBala= pygame.image.load(self.jugadorActual.tanque.proyectilActual.pathImagen)
        
        cuadroVacio= pygame.image.load(cuadroVacioImagen)# para tanque y bala
        
        bala = self.jugadorActual.tanque.proyectilActual.pathImagen
        giftCreditos = "imagenes/creditosGift.png"
        
        botonSalir=pygame.image.load("imagenes/botones/botonSalir.png")
        botonReiniciar=pygame.image.load("imagenes/botones/botonReiniciar.png")
        botonCambioArmas=pygame.image.load("imagenes/botones/botonMochila.png")
        botonAyuda=pygame.image.load("imagenes/botones/botonAyuda.png")

        self.boton_infoBala= Boton(self.director.pantalla, "proyectil actual\ndaño: {self.jugadorActual.tanque.proyectilActual.daño} ", 80, 640 ,cuadroVacio,50,50)
        self.boton_infoBala.dibujaBoton()
        self.mostrarImagenEnPos(bala,(50,50),(80,640))

        
        self.boton_salir = Boton(self.director.pantalla, "", 1220, 660 ,botonSalir,40,40)
        self.boton_salir.dibujaBoton()

        self.boton_reiniciar = Boton(self.director.pantalla, "", 1220, 610, botonReiniciar,40,40)
        self.boton_reiniciar.dibujaBoton()

        self.boton_cambioArmas = Boton(self.director.pantalla, "", 1170, 660, botonCambioArmas,40,40)
        self.boton_cambioArmas.dibujaBoton()

        self.boton_ayuda = Boton(self.director.pantalla, "", 1170, 610, botonAyuda,40,40)
        self.boton_ayuda.dibujaBoton()

        self.boton_creditos = Boton(self.director.pantalla, "", 1235, 5, cuadroVacio,40,40)
        self.boton_creditos.dibujaBoton()
        self.mostrarImagenEnPos(giftCreditos,(30,30),(1240,10))

    #----------------------------------DESTRUCCIóN DE TIERRA ---------------------------------------
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
            self.partidaActual.mapa.listaBloques.remove(bloque) # se remueve el bloque impactado

            listaColumna=[bloque]
            altura=40
            # se van añadiendo los bloques a la lista (se buscan bloques hacia arriba del impactado)
            while True:
                bloqueSup=self.buscarBloque(bloque.x,bloque.y-altura)
                # si el bloque de "tierra" existe
                if bloqueSup is not None:
                    listaColumna.append(bloqueSup)
                    altura+=40
                else:
                    break

            bloqueTanque=self.buscarTanque(bloque.x,bloque.y-altura)
            # si arriba del último bloque de tierra existe un tanque
            if bloqueTanque is not None:
                listaColumna.append(bloqueTanque)

            """
            queremos los bloques al reves, de modo que el de más arriba vaya ocupando la posición
            del que esta abajo, así sucesivamente hasta llegar que el bloque superior al bloque 
            impactado ocupe su posición
            """
            listaColumna.reverse()
            for i in range(0, len(listaColumna) - 1):
                listaColumna[i].y = listaColumna[i + 1].y

    def destruirZonaImpacto(self, bloqueImpactado, nombreArma):
        if nombreArma != "Proyectil 105":
            # animación de impacto
            self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png", (40, 40),
                                    (self.bloqueImpactado.x, self.bloqueImpactado.y))
            self.destruir(bloqueImpactado)  # todos rompen el bloque de impacto

        if nombreArma == "Proyectil Perforante":
            self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png", (40, 40),
                                    (self.bloqueImpactado.x - 40, self.bloqueImpactado.y))
            self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png", (40, 40),
                                    (self.bloqueImpactado.x + 40, self.bloqueImpactado.y))
            # pygame.display.update()
            # time.sleep(3) #<-- debug para notar con mas claridad la gravedad
            bloqueIzquierda = self.buscarBloque(bloqueImpactado.x - 40, bloqueImpactado.y)
            bloqueDerecha = self.buscarBloque(bloqueImpactado.x + 40, bloqueImpactado.y)
            # destrucción de los bloques
            self.destruir(bloqueIzquierda)
            self.destruir(bloqueDerecha)

        if nombreArma == "Proyectil 105":
            ejeY = self.bloqueImpactado.y - 40
            while ejeY < self.bloqueImpactado.y + 80:
                self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png", (40, 40),
                                        (self.bloqueImpactado.x - 40, ejeY))
                self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png", (40, 40), (self.bloqueImpactado.x, ejeY))
                self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png", (40, 40),
                                        (self.bloqueImpactado.x + 40, ejeY))
                # pygame.display.update()
                # time.sleep(3) #<-- debug para notar con mas claridad la gravedad
                bloqueIzquierda = self.buscarBloque(bloqueImpactado.x - 40, ejeY)
                bloqueCentral = self.buscarBloque(bloqueImpactado.x,ejeY)
                bloqueDerecha = self.buscarBloque(bloqueImpactado.x + 40, ejeY)
                self.destruir(bloqueIzquierda)
                self.destruir(bloqueCentral)
                self.destruir(bloqueDerecha)
                ejeY += 40    
                
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
    def cambiarEscenaCreditos(self):
        self.director.cambiarEscena(EscenaCreditos(self.director))  

    def cambiarEscenaAyuda(self):
        self.director.cambiarEscena(EscenaAyuda(self.director))

    """ Cuando se presiona el botón reiniciar, debemos crear un nuevo juego, por tanto, se borra el objeto
    Juego anterior creado y se le asigna al atributo game del director un nuevo objeto juego recién creado
    """
    def cambiarEscenaRegistro(self):
        #print(f'lista escenas antes: {self.director.listaEscenas}') # << debug
        # se limpia/borra el objeto juego anterior y se crea un nuevo juego (manejado por el director)
        del self.director.game
        self.director.game=[]
        self.director.game=Juego(2,1)
        # se cambia a la escena de registro anteriormente guardada
        # se salvan del borrado escenas iniciales
        nuevoHome=self.director.listaEscenas[0]
        nuevoConfig=self.director.listaEscenas[1]
        self.director.cambiarEscena(nuevoHome)
        # se borran las escenas guardadas hasta el momento por el director

        del self.director.listaEscenas
        self.director.listaEscenas=[nuevoHome,nuevoConfig]
        #print(f' lista escena despues: {self.director.listaEscenas}') # << debug
        self.director.escena.textoEnPantalla("Se ha reiniciado el juego correctamente, por favor registra jugadores"
                                             +" nuevamente",20,BLANCO,(100,300),True)
        time.sleep(3)

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

    """
    Metodo que verifica si alguno de los tanques en la instancia actual de la partida
    esta tocando el suelo, de ser afirmativo, elimina el jugador de esa partida
    """

    def pisoEsLava(self):
        for jugador in self.partidaActual.jugadoresActivos:
            if jugador.tanque.bloque.y == 560:
                self.mostrarImagenEnPos("imagenes/bloque/flama.png", (40, 40),
                                        (jugador.tanque.bloque.x, jugador.tanque.bloque.y))
                self.textoEnPantalla("EL PISO ES LAVA", 30, ROJO, (500, 300), True)
                self.partidaActual.eliminarJugador(jugador)

    """
    Metodo que sirve para mostrar lineas horizontales y verticales en la pantalla, cuando
    estas se instersectan podremos notar con más claridad cada bloque dentro del juego,
    principalmente se usará para comprobar que la destrucción de los bloques es correcta y
    que la gravedad funciona correctamente.
    """

    def mostrarLineas(self):
        contadorHorizontal=40
        while contadorHorizontal<640:
            pygame.draw.line(self.director.pantalla,BLANCO,(0,contadorHorizontal),(1280,contadorHorizontal),1)
            contadorHorizontal+=40
        contadorVertical=40
        while contadorVertical<1280:
            pygame.draw.line(self.director.pantalla,BLANCO,(contadorVertical,0),(contadorVertical,600),1)
            contadorVertical+=40


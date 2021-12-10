from os import pipe
import pygame
import math
import time
from escenas import plantillaEscena
from Mapa.listasEscenarios import *
from escenas.director import Director
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
        self.director.listaEscenas["escenaJuego"]=self
        
        self.fondo = fondosLista[random.randint(0, len(fondosLista) - 1)]
        self.fondo = pygame.transform.scale(self.fondo, (self.director.ancho,self.director.ancho))
        self.partidas = self.director.game.listaPartidas
        # para esta entrega hay solo una partida y 2 jugadores, por tanto:
        # la partida inicial será la primera partida (De momento es la única)
        self.partidaActual = self.partidas[0]
        # Requisito 3 U3: El jugador inicial será aleatorio
        self.jugadorActual = random.choice(self.partidaActual.jugadoresActivos)
        self.trayectoria = []
        self.contador = 0
        self.flag = False
        self.jugadorImpactado = None
        self.bloqueImpactado = None
        self.xMaxDisparo = 0
        self.yMaxDisparo = 0
        self.aceleracionVertical = self.director.listaEscenas["escenaHome"].gravedad
        self.aceleracionHorizontal = self.director.listaEscenas["escenaHome"].viento
        self.boton_salir = None
        self.boton_reiniciar = None
        self.boton_cambioArmas = None
        self.boton_ayuda = None
        self.boton_infoBala = None
        self.boton_creditos = None

    def on_update(self):
        pygame.display.set_caption("NORTHKOREA WARS SIMULATOR")
        pygame.display.set_mode((self.director.ancho, self.director.alto))
        self.director.pantalla.blit(self.fondo, (0, 0))
        bannerImagen = pygame.transform.scale(pygame.image.load('imagenes/banner.png'), (self.director.ancho, 120 ))
        self.director.pantalla.blit(bannerImagen, (0, self.director.alto-120))
        # pygame.draw.rect(self.director.pantalla, NEGRO, (0, 600, 1280, 120))  # barra inferior inferior
        self.partidaActual.mapa.dibujarMapa(self.director.pantalla)
        self.dibujarTanques()
        self.mostrarCañon()
        self.muestreoVidaTanques()
        self.pisoEsLava()
        # self.mostrarLineas() # <--- debug

    def on_event(self, event):
        self.director.mousePos = pygame.mouse.get_pos()
        """Requisito 4: Se bloquea presionar botones por parte del usuario en turnos de IA (para evitar bugs)"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.director.checaBoton(self.director.mousePos, self.boton_salir):
                if(self.director.debug):
                    print('(escenaJuego) PRESION BOTON: presionaste el boton salir')
                self.director.running = False  # rompe el ciclo gameLoop y sale del juego
            if self.director.checaBoton(self.director.mousePos, self.boton_reiniciar):
                if(self.director.debug):
                    print('(escenaJuego) PRESION BOTON: presionaste el boton reiniciar, se reiniciará la partida, te llevará de vuelta a escenaHome')
                self.cambiarEscenaHome()
                # self.reiniciarPartida()
            if self.director.checaBoton(self.director.mousePos, self.boton_cambioArmas):
                if(self.director.debug):
                    print('(escenaJuego) PRESION BOTON: presionaste el boton Balas, te llevará a la escenaCambioArmas')
                self.cambiarEscenaArmas()
            if self.director.checaBoton(self.director.mousePos, self.boton_ayuda):
                if(self.director.debug):
                    print('(escenaJuego) PRESION BOTON: presionaste el boton ayuda, te llevará a escenaAyudas')
                self.cambiarEscenaAyuda()
            if self.director.checaBoton(self.director.mousePos, self.boton_creditos):
                if(self.director.debug):
                    print('(escenaJuego) PRESIONA BOTON: presionaste el boton creditos, te llevará a escenaCreditos ')
                self.cambiarEscenaCreditos()

        if event.type == pygame.KEYDOWN and self.flag is False:
            pygame.key.set_repeat(2, 100)
            if event.key == pygame.K_SPACE:
                if self.jugadorActual.tanque.proyectilActual.municion > 0:  # posee balas suficientes
                    self.flag = True
                    self.jugadorActual.tanque.proyectilActual.municion -= 1  # se le resta una bala ya que disparó
                else:
                    # se muestra mensaje que no posee balas
                    self.textoEnPantalla(f'NO TIENES BALAS SUFICIENTES, CAMBIA DE ARMA', 30, BLANCO, (300, 300), True)

            """Requisito 4: Se bloquea mover flechas por parte del usuario en turnos de IA(para evitar bugs)"""
            if self.jugadorActual.esIA is not True:
                if event.key == pygame.K_LEFT:
                    if 200 > self.jugadorActual.tanque.velocidad -1 > 50:
                        self.jugadorActual.tanque.velocidad -= 1
                if event.key == pygame.K_RIGHT:
                    if 200 >= self.jugadorActual.tanque.velocidad +1 > 50:
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
                """Requisito 4: Si es IA, debe actuar autonomamente"""
                if self.jugadorActual.esIA is True:
                    self.decisionIA()
                self.contenidoBarraInferior()
                self.mostrarGravedadViento()
                if self.flag:
                    # si al comenzar un turno, ningun jugador tiene balas, empatan
                    if self.empate() is True:
                        self.textoEnPantalla("EMPATE POR NO TENER BALAS", 30, BLANCO, (self.director.ancho/2 -200,self.director.alto/2), True)
                        if(self.director.debug):
                            print('JUEGO: Los jugadores no poseen balas para terminar el juego, EMPATE!')
                        time.sleep(5)
                        self.director.running = False
                    if self.trayectoria == []:
                        if(self.jugadorActual.esIA is True):
                            if(self.director.debug):
                                print(f'\n(escenaJuego) ACCION: Tanque del jugador {self.jugadorActual.nombre} disparó automaticacamente')
                        else:
                            if(self.director.debug):
                                print(f'\n(escenaJuego) ACCION: Tanque del jugador {self.jugadorActual.nombre} disparó manualmente')
                        self.efectuarDisparo()
                    else:
                        if self.contador < len(self.trayectoria):
                            self.dibujarBala()
                        else:
                            self.limpiarTurno()  # se limpian las estadisticas
                            self.cambiarJugador()
            else:
                """ 
                Requisito 3 U3: Como se terminó la partida dado que en la lista de jugadoresActivos de la partida actual
                sólo queda un jugador, debemos calcular qué jugador destruyó más tanques, por ende, se invoca
                el metodo de a continuación a la partida acutal:
                """
                self.partidaActual.terminar(self.director.game.listaJugadores)
                # mensaje fin de partida
                """ si no empatan es porque existe ganador de la partida, por ende, también lo habrá
                del juego (se construyó con la visión de que el juego podría tener múltiples partidas)"""
                if self.partidaActual.jugadorGanador is not None:
                    self.textoEnPantalla(f'FIN DE PARTIDA, GANADOR: {self.partidaActual.jugadorGanador.nombre}', 20,
                                         BLANCO,
                                         (self.director.ancho/2 -150,self.director.alto/2), True)
                    self.director.game.definirGanador()  # << invocamos que defina un ganador del juego
                    self.textoEnPantalla(f'FIN DEL JUEGO, GANADOR: {self.director.game.jugadorGanador.nombre}', 20, BLANCO,
                                 (self.director.ancho/2 -150,self.director.alto/2+50), True)
                    time.sleep(5)
                else:  # si es none es porque hubo empate
                    self.textoEnPantalla(f'EMPATE POR CANTIDAD DE DESTRUIDOS', 20,
                                         BLANCO,
                                         (self.director.ancho/2 -200,self.director.ancho/2-200), True)
                    self.textoEnPantalla(f'Ganador Juego: Ninguno debido empate',20,BLANCO,(self.director.ancho/2-300,self.director.alto/2),True)
                    time.sleep(5)
                    self.director.game.juegoTerminado=True
        else:
            self.director.running = False  # rompe el gameloop para terminar el juego

    # ------------------------------FUNCIONES QUE REPRESENTAN ACCIONES DENTRO DEL JUEGO-----------------------------

    # Toma las posiciones de la bala y va viendo los posibles escenarios para buscar los valores maximos.
    def calcularDesplazamientoAltura(self, xDisparo, yDisparo):
        conversionCmPx = 265 / 10000
        """
        Para calcular el desplazamiento, debemos tomar dos puntos dentro del mapa, el cual son la 
        posicion del tanque donde se efectuo el disparo, como tambien, la posicion en x donde llego este (al final)
        """
        self.xMaxDisparo = int(abs(xDisparo - self.jugadorActual.tanque.bloque.x) * conversionCmPx)

        """
        Para calcular la altura, se tomara dos puntos dentro del mapa, el cual son la posicion
        del tanque donde se efectuo el disparo, como tambien, la posicion en y donde viaja el proyectil
        """
        yDisparoConv = int(abs(yDisparo * conversionCmPx))
        if yDisparo * conversionCmPx > self.yMaxDisparo:
            self.yMaxDisparo = yDisparoConv

    def efectuarDisparo(self):
        delta = 0
        self.xMaxDisparo = 0
        self.yMaxDisparo = 0
        xJugador = self.jugadorActual.tanque.bloque.x
        yJugador = self.jugadorActual.tanque.bloque.y
        while True:
            #Se aplica la misma formula de la aceleracion de gravedad, pero ahora de forma vertical, lo cual da un efecto de viento
            xDisparo = int(xJugador + 20 + delta * self.jugadorActual.tanque.velocidad * math.cos(
                self.jugadorActual.tanque.angulo * 3.1416 / 180) + (self.aceleracionHorizontal * delta * delta) / 2)
            yDisparo = int(yJugador - 1 - (
                    delta * self.jugadorActual.tanque.velocidad * math.sin(
                self.jugadorActual.tanque.angulo * 3.1416 / 180) - (self.aceleracionVertical * delta * delta) / 2))
            delta += 0.1  # si quieres que hayan más puntitos en la parabola, modifica esto
            self.trayectoria.append((xDisparo, yDisparo))
            self.calcularDesplazamientoAltura(xDisparo, yDisparo)
            # ----------------------------------VERIFICAR SI TOCA BLOQUES-----------------------------------------------
            jugadorImpactado = self.colisionTanque(xDisparo, yDisparo)
            bloqueImpactado = self.colisionTierra(xDisparo, yDisparo)

            if jugadorImpactado is not None:  # si impacta con un tanque, se detiene la parabola (bala)
                self.jugadorImpactado = jugadorImpactado
                if(self.director.debug):
                    print(f'        (escenaJuego) IMPACTO: la bala impactó al tanque del jugador {self.jugadorImpactado.nombre} quitandole {self.jugadorActual.tanque.proyectilActual.daño}')
                break

            elif self.colisionTierra(xDisparo, yDisparo):
                if(self.director.debug):
                    print(f'        (escenaJuego) IMPACTO: la bala impactó un bloque de tierra')
                self.bloqueImpactado = bloqueImpactado
                break

            elif self.tocaBordes(xDisparo, yDisparo):  # si impacta con un borde, se detiene la parabola (bala)
                if(self.director.debug):
                    print(f'        (escenaJuego) IMPACTO: la bala impactó un limite de mapa')
                break

    """
    Requisito 3 U3: Se establece para cada jugador el atributo participoTurno el cual es False en el constructor.
    El primer jugador es aleatorio, por tanto, al participar en el turno se cambia su atributo participoTurno
    a True, posteriormente se filtran todos los jugadores que aun no participan (que tienen su atributo
    participoTurno en False) y se escoge aleatoriamente uno de ellos hasta que todos hayan participado. Cuando
    sucede lo anterior, se completa la RONDA por lo que cada jugador tiene la posibilidad de participar (jugar su turno)
    de forma aleatoria nuevamente siguiendo la misma logica.
    """

    def cambiarJugador(self):
        # como ya participo el jugador actual
        self.jugadorActual.participoTurno = True

        listaJugadoresPartida = self.partidaActual.jugadoresActivos
        jugadoresSinParticipar = list(filter(lambda jug: jug.participoTurno is not True, listaJugadoresPartida))
        if not jugadoresSinParticipar:
            #en el caso de que se activaran los efectos de entorno, se revaloriza el clima por cada ronda
            if self.director.listaEscenas["escenaHome"].viento_o_no == True:
                self.aceleracionHorizontal = random.randint(-10, 10)
            self.textoEnPantalla("SE HA COMPLETADO UNA RONDA DE TURNOS", 20, BLANCO, (self.director.ancho/2 - 200,self.director.alto/2), True)
            if(self.director.debug):
                print("- - - - - - - - - - - - ")  # << debug terminal
            time.sleep(2)
            # se reinicia la particion de cada jugador activo en la partida a False
            for jugador in self.partidaActual.jugadoresActivos:
                jugador.participoTurno = False
        else:
            self.textoEnPantalla("CAMBIO DE TURNO", 20, BLANCO, (self.director.ancho/2 -200, self.director.alto/2), True)
            # elige un jugador que no ha participado para cederle el turno
            self.jugadorActual = random.choice(jugadoresSinParticipar)

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
        """
        Antes, para que toque el borde superior y explote: yDisparo <=0 
        Ahora, si quieres aumentar el "techo", y<=-200 o otra cifra
        """
        if xDisparo >= self.director.ancho or yDisparo >= self.director.alto-120 or xDisparo <= 0 or yDisparo <= -200:
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
                self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png", (40, 40),
                                        (self.jugadorImpactado.tanque.bloque.x,
                                         self.jugadorImpactado.tanque.bloque.y))
                #pygame.time.wait(100)

                dañoEfectuado = self.jugadorActual.tanque.proyectilActual.daño
                if dañoEfectuado >= self.jugadorImpactado.tanque.vida:
                    """ Requisito 3 U3: Si se suicida, no cuenta como un oponente destruido, por el contrario,
                    si un jugador destruye a otro lo será """
                    if self.jugadorActual is not self.jugadorImpactado:
                        self.jugadorActual.oponentesDestruidos += 1
                    self.partidaActual.eliminarJugador(self.jugadorImpactado)  # elimina al jugador

                else:
                    # se le resta la vida del arma del jugador contrario
                    self.jugadorImpactado.tanque.vida -= dañoEfectuado
            if self.bloqueImpactado is not None:
                # destruirá el bloque actual y la zona según el daño del proyectil
                self.destruirZonaImpacto(self.bloqueImpactado, self.jugadorActual.tanque.proyectilActual.nombre)
            else:
                # se muestra la imagen explosion con el borde
                self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png", (40, 40), (coord[0], coord[1]))
                #pygame.time.wait(100)

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
        self.textoEnPantalla(f'Jugador actual: {self.jugadorActual.nombre}', 15, BLANCO, (20, self.director.alto-100), False)
        self.textoEnPantalla(f'Angulo: {self.jugadorActual.tanque.angulo}', 15, BLANCO, ((self.director.ancho/2)+20, self.director.alto-75), False)
        self.textoEnPantalla((f'Municion de Bala: ' + str(self.jugadorActual.tanque.proyectilActual.municion)), 15,
                             BLANCO, ((self.director.ancho/2)+20, self.director.alto-55), False)
        self.textoEnPantalla(f'Velocidad: {self.jugadorActual.tanque.velocidad} [cm/s]', 15, BLANCO, ((self.director.ancho/2)+20, self.director.alto-95), False)
        cuadroVacioImagen = "imagenes/botones/botonVacio.png"

        self.mostrarImagenEnPos(cuadroVacioImagen, (50, 50), (20, self.director.alto-70))
        self.mostrarImagenEnPos(self.jugadorActual.tanque.imagen, (30, 30), (30, self.director.alto-60))

        """ Requisito 2 y 4: Si el jugador del turno es una IA, se muestra un robot en la barra inferior"""
        if self.jugadorActual.esIA is True:
            self.mostrarImagenEnPos("imagenes/IA.png", (50, 50), (self.director.ancho-200, self.director.alto-100))


        self.textoEnPantalla(f'Desplazamiento maximo: {self.xMaxDisparo} [cm]', 15, BLANCO, (150, self.director.alto-75), False)
        self.textoEnPantalla(f'Altura maxima: {self.yMaxDisparo} [cm]', 15, BLANCO, (150, self.director.alto-55), False)

        cuadroVacio = pygame.image.load(cuadroVacioImagen)  # para tanque y bala

        bala = self.jugadorActual.tanque.proyectilActual.pathImagen
        giftCreditos = "imagenes/creditosGift.png"

        botonSalir = pygame.image.load("imagenes/botones/botonSalir.png")
        botonReiniciar = pygame.image.load("imagenes/botones/botonReiniciar.png")
        botonCambioArmas = pygame.image.load("imagenes/botones/botonMochila.png")
        botonAyuda = pygame.image.load("imagenes/botones/botonAyuda.png")

        self.boton_infoBala = Boton(self.director.pantalla,
                                    "proyectil actual\ndaño: {self.jugadorActual.tanque.proyectilActual.daño} ", 80,
                                    self.director.alto-70, cuadroVacio, 50, 50)
        self.boton_infoBala.dibujaBoton()
        self.mostrarImagenEnPos(bala, (50, 50), (80, self.director.alto-70))

        self.boton_salir = Boton(self.director.pantalla, "", self.director.ancho-95, self.director.alto-95, botonSalir, 40, 40)
        self.boton_salir.dibujaBoton()

        self.boton_reiniciar = Boton(self.director.pantalla, "", self.director.ancho-95, self.director.alto-50, botonReiniciar, 40, 40)
        self.boton_reiniciar.dibujaBoton()

        self.boton_cambioArmas = Boton(self.director.pantalla, "", self.director.ancho-50, self.director.alto-50, botonCambioArmas, 40, 40)
        self.boton_cambioArmas.dibujaBoton()

        self.boton_ayuda = Boton(self.director.pantalla, "", self.director.ancho-50, self.director.alto-95, botonAyuda, 40, 40)
        self.boton_ayuda.dibujaBoton()

        self.boton_creditos = Boton(self.director.pantalla, "", self.director.ancho-50, 5, cuadroVacio, 40, 40)
        self.boton_creditos.dibujaBoton()
        self.mostrarImagenEnPos(giftCreditos, (30, 30), (self.director.ancho-45, 10))

    # ----------------------------------_DESTRUCCION DE TIERRA ---------------------------------------
    def buscarBloque(self, x, y):
        for bloque in self.partidaActual.mapa.listaBloques:
            if bloque.x == x and bloque.y == y:
                return bloque
        return None

    def buscarJugador(self, x, y):
        for jugador in self.partidaActual.jugadoresActivos:
            if jugador.tanque.bloque.x == x and jugador.tanque.bloque.y == y:
                return jugador
        return None


    def destruir(self, bloque):
        # si existe dentro de la lista de bloques
        if bloque is not None:
            self.partidaActual.mapa.listaBloques.remove(bloque)  # se remueve el bloque impactado

            listaColumna = [bloque]
            altura = 40
            # se van añadiendo los bloques a la lista (se buscan bloques hacia arriba del impactado)
            while True:
                bloqueSup = self.buscarBloque(bloque.x, bloque.y - altura)
                # si el bloque de "tierra" existe
                if bloqueSup is not None:
                    listaColumna.append(bloqueSup)
                    altura += 40
                else:
                    break

            jugadorImpactado = self.buscarJugador(bloque.x, bloque.y-altura)
            # si arriba del último bloque de tierra existe un tanque
            if jugadorImpactado is not None:
                if(self.director.debug):  
                    print('        (escenaJuego) CAIDA: tanque cae un bloque por gravedad de bloques')
                listaColumna.append(jugadorImpactado.tanque.bloque)
                


            """
            queremos los bloques al reves, de modo que el de más arriba vaya ocupando la posición
            del que esta abajo, así sucesivamente hasta llegar que el bloque superior al bloque 
            impactado ocupe su posición
            """
            listaColumna.reverse()    

            for i in range(0, len(listaColumna) - 1):
                listaColumna[i].y = listaColumna[i + 1].y

            
            # si el jugador impactado existe
            if jugadorImpactado is not None:
                #cantidadBloquesCaida=len(listaColumna)-1 # cant bloques que cae (no se cuenta a si mismo)
                # cambiar daño caida
                danoCaida=10
                if(jugadorImpactado.tanque.vida<=danoCaida):
                    if(self.jugadorActual != jugadorImpactado): # si no es un suicido
                        self.jugadorActual.oponentesDestruidos+=1 # suma una win
                    if(self.director.debug):
                        print(f'        (danoCaida) El jugador {jugadorImpactado.nombre} cayó 1 bloque, dañandosé {danoCaida} lo que lo destruye')
                    self.partidaActual.eliminarJugador(jugadorImpactado) # elimina el jugador
                else: # si es mayor, sobrevive
                    jugadorImpactado.tanque.vida-=danoCaida
                    if(self.director.debug):
                        print(f'        (danoCaida) El jugador {jugadorImpactado.nombre} cayó 1 bloque, dañandosé {danoCaida}')
            

    """ Requisito 1 U3: Dano colateral a los tanques cuando son impactados"""
    def danoColateralTanque(self,posX,posY):
        danoArmaEquipada=self.jugadorActual.tanque.proyectilActual.daño
        danoColateral=danoArmaEquipada/2
        for jugador in self.partidaActual.jugadoresActivos:
            tanqueJugador=jugador.tanque
            bloqueTanqueJugador=jugador.tanque.bloque
            # si el bloque danado por la zona de impacto es un bloque de un tanque
            if(bloqueTanqueJugador.x==posX and bloqueTanqueJugador.y==posY):
                # si el dano mata al tanque
                if danoColateral>=tanqueJugador.vida:
                    if(self.director.debug):
                        print(f'        (escenaJuego) DAÑO COLATERAL: a causa del impacto, el jugador {jugador.nombre} murió (le quitó {danoColateral})')
                    """ Requisito 3 U3: Si se suicida, no cuenta como oponente destruido"""
                    if(self.jugadorActual is not jugador):
                        self.jugadorActual.oponentesDestruidos+=1
                    self.partidaActual.eliminarJugador(jugador) # lo elimina
                # si el dano no quita toda la vida del tanque
                else:
                    if(self.director.debug):
                        print(f'        (escenaJuego) DAÑO COLATERAL: a causa del impacto, el tanque del jugador {jugador.nombre} sufrio daño de {danoColateral}')
                    tanqueJugador.vida-=danoColateral
                    return True
                

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
            
            """ Requisito 1 U3: Dano colateral a los tanques cuando son impactados"""
            self.danoColateralTanque(bloqueImpactado.x - 40,bloqueImpactado.y)
            self.danoColateralTanque(bloqueImpactado.x+40,bloqueImpactado.y)
            # destrucción de los bloques
            self.destruir(bloqueIzquierda)
            self.destruir(bloqueDerecha)

        if nombreArma == "Proyectil 105":
            ejeY = self.bloqueImpactado.y - 40

            """ dano colateral, no puede estar dentro del ciclo while
            dado que, primero debe ver la zona de daño colateral y después
            se van viendo cómo los bloques caen"""
            self.danoColateralTanque(bloqueImpactado.x - 40,bloqueImpactado.y) #1
            self.danoColateralTanque(bloqueImpactado.x,bloqueImpactado.y) #2
            self.danoColateralTanque(bloqueImpactado.x+40,bloqueImpactado.y) #3
            
            self.danoColateralTanque(bloqueImpactado.x - 40,bloqueImpactado.y-40)
            self.danoColateralTanque(bloqueImpactado.x,bloqueImpactado.y-40)
            self.danoColateralTanque(bloqueImpactado.x+40,bloqueImpactado.y-40)

            self.danoColateralTanque(bloqueImpactado.x - 40,bloqueImpactado.y+40)
            self.danoColateralTanque(bloqueImpactado.x,bloqueImpactado.y+40)
            self.danoColateralTanque(bloqueImpactado.x+40,bloqueImpactado.y+40)
            
            while ejeY < self.bloqueImpactado.y + 80:
                self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png", (40, 40),
                                        (self.bloqueImpactado.x - 40, ejeY))
                self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png", (40, 40), (self.bloqueImpactado.x, ejeY))
                self.mostrarImagenEnPos("imagenes/bloque/fondoExplosion.png", (40, 40),
                                        (self.bloqueImpactado.x + 40, ejeY))
                # pygame.display.update()
                # time.sleep(3) #<-- debug para notar con mas claridad la gravedad
                bloqueIzquierda = self.buscarBloque(bloqueImpactado.x - 40, ejeY)
                bloqueCentral = self.buscarBloque(bloqueImpactado.x, ejeY)
                bloqueDerecha = self.buscarBloque(bloqueImpactado.x + 40, ejeY)
                """ Requisito 1 U3: Dano colateral a los tanques cuando son impactados"""
                

                self.destruir(bloqueIzquierda)
                self.destruir(bloqueCentral)
                self.destruir(bloqueDerecha)

                ejeY += 40

        pygame.time.wait(400)  # <-- necesario para que se vean las graficas

    # ----------------------------------DEFINIR EMPATE---------------------------------------------------------
    def empate(self):
        for jugador in self.partidaActual.jugadoresActivos:
            proyectilesJug = jugador.tanque.listaProyectiles
            for proyectil in proyectilesJug:
                if proyectil.municion > 0:
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

    def cambiarEscenaHome(self):
        # se limpia/borra el objeto juego anterior y se crea un nuevo juego (manejado por el director)
        del self.director.game
        self.director.game = None
        pygame.key.set_repeat(0, 0)

        
        self.director.listaEscenas["escenaHome"].viento = 0
        self.director.listaEscenas["escenaHome"].gravedad = 9.8
        self.director.listaEscenas["escenaHome"].viento_o_no = False
        #hacer


        listaBorrar=[]
        """ se recorre el diccionario buscando todas llaves, valor a eliminar, no se pueden
        eliminar directamente en el ciclo ya que se prohibe (error de dict)"""
        for llave,valor in self.director.listaEscenas.items():
            if(llave != "escenaHome"):
                listaBorrar.append([llave,valor])
     
        """ posteriormente, procedemos a borrar"""
        for llave,valor in listaBorrar:
            self.director.listaEscenas.pop(llave) # <<< saca la escena del diccionario
            del valor # << borra el objeto donde se almacena la escena


        self.director.cambiarEscena(self.director.listaEscenas["escenaHome"])
        
        self.director.escena.textoEnPantalla("Se ha reiniciado el juego correctamente, por favor registra jugadores"
                                             + " nuevamente", 20, BLANCO, (100, 300), True)
        time.sleep(3)

    # ----------------------------------METODOS AL CAMBIAR DE TURNO------------------------------------------------
    def limpiarTurno(self):
        self.jugadorImpactado = None  # << se limpia
        self.bloqueImpactado = None
        self.contador = 0  # << el contador debe estar limpio para un nuevo jugador
        self.trayectoria = []  # << la trayectoria debe estar limpio para un nuevo jugador
        self.flag = False  # << debe apretar enter nuevamente el jugador para disparar
        self.xMaxDisparo = 0
        self.yMaxDisparo = 0

    # ----------------------------METODOS AL TERMINAR UNA PARTIDA O CREAR UNA NUEVA-----------------------------
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
            if jugador.tanque.bloque.y == self.director.alto-160:
                self.mostrarImagenEnPos("imagenes/bloque/flama.png", (40, 40),
                                        (jugador.tanque.bloque.x, jugador.tanque.bloque.y))
                self.textoEnPantalla("EL PISO ES LAVA", 20, ROJO, (self.director.ancho/2, self.director.alto/2 -100), True)
                if(self.director.debug):
                    print(f'(escenaJuego) JUEGO: Tanque de jugador {jugador.nombre} se destruyó por la lava')
                self.partidaActual.eliminarJugador(jugador)

    """
    Metodo que sirve para mostrar lineas horizontales y verticales en la pantalla, cuando
    estas se instersectan podremos notar con más claridad cada bloque dentro del juego,
    principalmente se usará para comprobar que la destrucción de los bloques es correcta y
    que la gravedad funciona correctamente.
    """

    def mostrarLineas(self):
        contadorHorizontal = 40
        while contadorHorizontal < 640:
            pygame.draw.line(self.director.pantalla, BLANCO, (0, contadorHorizontal), (1280, contadorHorizontal), 1)
            contadorHorizontal += 40
        contadorVertical = 40
        while contadorVertical < 1280:
            pygame.draw.line(self.director.pantalla, BLANCO, (contadorVertical, 0), (contadorVertical, 600), 1)
            contadorVertical += 40

    """------------------------------------------------------------------------------------
    Requisito 4: Cuando el turno es de una inteligencia artificial, decidirá la decisión automaticamente, no 
    debe el usuario actuar, por tanto, se empleará el metodo de a continuación:
    """

    def decisionIA(self):
        if self.flag is False:
            self.jugadorActual.tanque.angulo = random.randint(0, 180)
            self.jugadorActual.tanque.velocidad = random.randint(50, 100)
            if self.jugadorActual.tanque.proyectilActual.municion > 0:
                self.flag = True
                self.jugadorActual.tanque.proyectilActual.municion -= 1  # se le resta una bala ya que disparó
            # si no tiene municion, debe cambiar de arma por si sola
            else:
                for proyectil in self.jugadorActual.tanque.listaProyectiles:
                    if proyectil.municion > 0:
                        self.jugadorActual.tanque.proyectilActual = proyectil
                        self.textoEnPantalla("IA CAMBIA DE ARMA", 30, ROJO, (300, 300), True)

    def mostrarGravedadViento(self): 
        if self.aceleracionHorizontal == 0:
            viento = "imagenes/sinViento.png"
            self.textoEnPantalla(f'Viento : {self.aceleracionHorizontal} m/s', 15, BLANCO, (100, 0), False) 

        if self.aceleracionHorizontal > 0: 
            viento = "imagenes/banderaVientoDerecha.png" 
            self.textoEnPantalla(f'Viento : {self.aceleracionHorizontal} m/s', 15, BLANCO, (100, 0), False) 
 
        if self.aceleracionHorizontal < 0: 
            viento = "imagenes/banderaVientoIzquierda.png" 
            self.textoEnPantalla(f'Viento : {self.aceleracionHorizontal * -1} m/s', 15, BLANCO, (100, 0), False) 
 
        self.mostrarImagenEnPos(viento, (80, 80), (0, 0)) 
        self.textoEnPantalla(f'Gravedad : {self.aceleracionVertical} m/s^2', 15, BLANCO, (100, 40), False) 

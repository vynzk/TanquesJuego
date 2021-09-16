import pygame

"""esta clase corresponde a la clase padre de los elementos que se interrelacionan
    dentro del juego. 
    
    importancia: recalca en las coordenadas de posición y tamaño del objeto dentro de la pantalla"""


class Bloque:
    def __init__(self, pantalla, ancho, alto, color, x, y):
        self.ancho = ancho
        self.alto = alto
        self.x = x
        self.y = y
        self.color = color
        self.pantalla = pantalla
        self.vivo = True

    def dibujar(self):
        pygame.draw.rect(self.pantalla, self.color, (self.x, self.y, self.ancho, self.alto))


    def destruir(self):
        self.vivo = False
        # se desdibuja/borra, fijando el color del fondo, en este caso negro
        # si nos piden un fondo, encontrar una función que encuentre que se borre y quede invisible
        self.setColor((0, 0, 0))
        self.dibujar()

    def colision(self, xColision, yColision):
        # (x,y)------------| x+delta
        #  |               |
        #  |   colision    | 
        #  |               |   
        # __ y+delta __(x+delta, y+delta)       
        delta = 20  # tamaño del pixel del cuadrado
        xMax = self.getX() + delta  # limite horizontal del cuadrado
        yMax = self.getY() + delta  # limite vertical del cuadrado

        # si se encuentra dentro del limite horizontal del cuadrado
        if self.getX() <= xColision <= xMax:
            # si se encuentra dentro del limite vertical del cuadrado
            if self.getY() <= yColision <= yMax:
                return True  # colision

        return False  # no se encuentra  dentro del rango de colisión

    def setColor(self, color):
        self.color = color

    def getX(self):
        return self.x

    def getY(self):
        return self.y

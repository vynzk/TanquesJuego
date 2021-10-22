import pygame


class Bloque:
    def __init__(self, pantalla, ancho, alto, imagen, x, y):
        self.ancho = ancho
        self.alto = alto
        self.x = x
        self.y = y
        self.pantalla = pantalla
        self.imagen = pygame.image.load(imagen)
        # self.vivo=True

    def dibujar(self):
        self.pantalla.blit(self.imagen,(self.x,self.y))

    def colision(self, xColision, yColision):
        # (x,y)------------| x+delta
        #  |               |
        #  |   colision    | 
        #  |               |   
        # __ y+delta __(x+delta, y+delta)       
        delta = 40  # tamaño del pixel del cuadrado
        xMax = self.x + delta  # limite horizontal del cuadrado
        yMax = self.y + delta  # limite vertical del cuadrado

        # si se encuentra dentro del limite horizontal del cuadrado
        if self.x <= xColision <= xMax:
            # si se encuentra dentro del limite vertical del cuadrado
            if self.y <= yColision <= yMax:
                return True  # colision
        return False  # no se encuentra  dentro del rango de colisión

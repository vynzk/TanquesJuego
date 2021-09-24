import pygame


class Bloque:
    def __init__(self, pantalla, ancho, alto, color, x, y):
        self.ancho = ancho
        self.alto = alto
        self.x = x
        self.y = y
        self.color = color
        self.pantalla = pantalla
        # self.vivo=True

    def dibujar(self):
        pygame.draw.rect(self.pantalla, self.color, (self.x, self.y, self.ancho, self.alto))

    """ esto es innecesario, ya que cuando un bloque es sacado de una lista, se deja de dibujar, un ejemplo es el
    del mapa con su lista de bloques, en un futuro cuando se destruya un bloque, si se saca de esta lista ya no se
    dibujará más. Por tanto, se optará por quitar el atributo vivo/muerto
    
    def destruir(self):
        self.vivo = False
        # se desdibuja/borra, fijando el color del fondo, en este caso negro
        self.color((0, 0, 0))
        self.dibujar()
    """

    def colision(self, xColision, yColision):
        # (x,y)------------| x+delta
        #  |               |
        #  |   colision    | 
        #  |               |   
        # __ y+delta __(x+delta, y+delta)       
        delta = 20  # tamaño del pixel del cuadrado
        xMax = self.x + delta  # limite horizontal del cuadrado
        yMax = self.y + delta  # limite vertical del cuadrado

        # si se encuentra dentro del limite horizontal del cuadrado
        if self.x <= xColision <= xMax:
            # si se encuentra dentro del limite vertical del cuadrado
            if self.y <= yColision <= yMax:
                return True  # colision
        return False  # no se encuentra  dentro del rango de colisión

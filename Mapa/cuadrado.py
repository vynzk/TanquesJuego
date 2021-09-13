from GUI.bloque import Bloque

class Cuadrado(Bloque):
    def __init__(self,pantalla,ancho,alto,color,x,y):
        Bloque.__init__(self,pantalla,ancho,alto,color,x,y)
        # self.vivo lo moví dentro de bloque :) atte: keke

    # función que destruye un cuadrado, esto es dado que le impacta un proyectil
    def destruir(self):
        self.vivo=False
        # se desdibuja/borra, fijando el color del fondo, en este caso negro
        # si nos piden un fondo, encontrar una función que encuentre que se borre y quede invisible
        self.setColor((0,0,0)) 
        self.dibujar()


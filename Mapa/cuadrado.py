from GUI.bloque import Bloque

class Cuadrado(Bloque):
    def __init__(self,pantalla,ancho,alto,color,x,y):
        Bloque.__init__(self,pantalla,ancho,alto,color,x,y)
        self.vivo=True
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

    def colision(self,xColision,yColision):
        # (x,y)------------| x+delta
        #  |               |
        #  |   colision    | 
        #  |               |   
        # __ y+delta __(x+delta, y+delta)       
        delta=20 # tamaño del pixel del cuadrado
        xMax=self.getX()+delta # limite horizontal del cuadrado
        yMax=self.getY()+delta # limite vertical del cuadrado

        # si se encuentra dentro del limite horizontal del cuadrado
        if(self.getX()<=xColision and xColision <= xMax):
            # si se encuentra dentro del limite vertical del cuadrado
            if(self.getY()<=yColision and yColision <= yMax):
                return True # colision
                    
        return False # no se encuentra  dentro del rango de colisión
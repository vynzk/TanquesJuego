"""
import pygame
import sys
import math
from Tanque.Tanque import *

class Proyectil():
	def __init__(self):
		self.cero = 0
		self.velocidad = velocidad
		self.angulo = angulo
		self.constante = 50 #La constante es provisional, aún tengo que ver las colisiones con el terreno

		self.proyectil_size = 25
		self.proyectil_pos = [jugador_pos[0]+50, jugador_pos[1]+14]

		self.proyectil2_size = 25
		self.proyectil2_size = [eneemigo_pos[0]-50, enemigo_pos[1]+14]

	def colisiones(self, enemigo_pos, proyectil_pos):
    		px = proyectil_pos[0]
    		py = proyectil_pos[1]
    		ex = enemigo_pos[0]
    		ey = enemigo_pos[1]

    		if (ex >= px and ex <(px + proyectil_size)) or (px >= ex and px < (ex + enemigo_size)):
    	    		if (ey >= py and ey <(py + proyectil_size)) or (py >= ey and py < (ey + enemigo_size)):
    	    		    return True
    	    		return False

    def disparar(self)	    		
	    while cero<=constante:
	        pygame.draw.rect(ventana, color_verde, 
	        (proyectil_pos[0], proyectil_pos[1], 
	        proyectil_size, 20))

	        x = jugador_pos[0]+50 + cero*velocidad*math.cos(angulo*3.1416/180)
	        y = jugador_pos[1]+14 - (cero*velocidad*math.sin(angulo*3.1416/180) - (9.81*cero*cero)/2)
	        proyectil_pos[0] = x
	        proyectil_pos[1] = y
	        cero+=0.25	    		
"""


import pygame
from GUI.bloque import Bloque
class Proyectil(Bloque):
	def __init__(self,pantalla,ancho,alto,color,x,y):
		Bloque.__init__(self,pantalla,ancho,alto,color,x,y)
		self.vivo=False
		self.balaImagen= pygame.image.load("GUI/imagenes/bomb.png").convert_alpha()
		self.redimensionaBala()

	def activaProyectil(self, coordenadasXY):
		self.vivo=True
	def sigueTrayectoria(self,coordenadasXY): #para que siga la trayectoria de disparo
		"""objetivo??: que siga la trayectoria de disparo... al ser un
		objeto... se puede crear una función que determine cuando colisona
		con la coordenada de otro (como el cuadrado rosa con la interfaz)"""
		if self.vivo==True:
			self.pantalla.blit(self.balaImagen, coordenadasXY)
	def redimensionaBala(self):
		self.balaImagen = pygame.transform.scale(self.balaImagen, (30, 30))


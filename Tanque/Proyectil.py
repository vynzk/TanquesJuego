"""
import pygame
import sys
import math
from Tanque.Tanque import *

class Proyectil():
	def __init__(self):
		self.velocidad = velocidad
		self.angulo = angulo

    def disparar(self, velocidad, angulo)	
    	posx = 20
    	posy = 250 
    	angulo = 60
    	velocidad = 50 

	    while delta<=constante:
	        pygame.draw.rect(ventana, color_verde, 
	        (proyectil_pos[0], proyectil_pos[1], 
	        proyectil_size, 20))

	        x = posx+50 + delta*velocidad*math.cos(angulo*3.1416/180)
	        y = posy+14 - (delta*velocidad*math.sin(angulo*3.1416/180) - (9.81*delta*delta)/2)
	        posx = x
	        posy = y
	        delta+=0.25	    		
"""
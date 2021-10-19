import pygame
from GUI import plantillaEscena
from GUI.Boton import Boton

class EscenaAyuda:
	def __init__(self,director):
		plantillaEscena.Escena.__init__(self, director)
		self.botonVolver = None
		self.fondo=pygame.image.load("GUI/imagenes/fondoTransparente.png")
		#self.fondo= pygame.image.load("GUI/imagenes/fondoAyuda.jpg") #por ahora
		self.panel= pygame.image.load("GUI/imagenes/panelArmas.png")
		self.redimensionarPanel(500,500)

	def on_update(self):
		pygame.display.set_caption("Ayuda") 


	def on_event(self, evento):
		if evento.type == pygame.MOUSEBUTTONDOWN:
			self.director.mousePos = pygame.mouse.get_pos()	
			if self.director.checaBoton(self.director.mousePos, self.botonVolver):
				self.vuelveJuego()

	def on_draw(self, pantalla):
		pantalla.blit(self.fondoTransparente, (0,0))
		pantalla.blit(self.panel, (390, 100))


		# imagenes -- botones
		volver= pygame.image.load("GUI/imagenes/botones/botonVolver.png")
		panelArma= pygame.image.load("GUI/imagenes/panelSeleccionArmas.png")

		self.botonVolver = Boton(pantalla, "volver", 580,500,volver,127,40)
		self.botonVolver.dibujaBoton()


		# esto dibuja los paneles por cada arma en listaArma00
		posPanel=210 #posicion 'y' del panel
		yPanel = 60 #dimension 'y' del panel
		i=0

	def redimensionarPanel(self, x,y):
		self.panel= pygame.transform.scale(self.panel, (x,y) )

	def vuelveJuego(self):
		juegoActual= self.director.listaEscenas[0]
		self.director.cambiarEscena(juegoActual)

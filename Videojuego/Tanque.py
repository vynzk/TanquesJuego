# clase que se borrará, no me corresponde, sin embargo, para calzar mi clase Juego se construirá el prototipo
from GUI.bloque import Bloque

class Tanque(Bloque):
    def __init__(self, modelo, pantalla):
        Bloque.__init__(self, pantalla, 300,300, (0,0,225), 0,0) # hereda de bloque
        self.modelo = "Default"

    def mostrarInformacion(self):
        return "modelo: " + str(self.modelo)


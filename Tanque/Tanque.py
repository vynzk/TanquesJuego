# clase que se borrará, no me corresponde, sin embargo, para calzar mi clase Juego se construirá el prototipo
class Tanque():
    def __init__(self, modelo):
        self.modelo = "Default"

    def mostrarInformacion(self):
        return "modelo: " + str(self.modelo)
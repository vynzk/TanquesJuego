class Jugador():
    def __init__(self,nombre,tanque):
        self.nombre=nombre
        self.tanque=tanque

    def getNombre(self):
        return self.nombre

    def mostrarInformacion(self):
        print("Nombre: ",self.nombre," ; Tanque: ",self.tanque.mostrarInformacion())

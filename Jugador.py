class Jugador():
    # tanque debe ser un objeto tanque, que se guardará en un atributo del jugador
    # por ende, debe estar construido el objeto Tanque
    def __init__(self,nombre,tanque):
        self.nombre=nombre
        self.tanque=tanque

    def mostrarInformacion(self):
        print("Nombre: ",self.nombre," ; Tanque: ",self.tanque)

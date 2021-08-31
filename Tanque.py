class Tanque():
    def __init__(self,modelo):
        self.vivo=True
        self.modelo="Default"

    def mostrarInformacion(self):
        return "vivo:"+str(self.vivo)+" | modelo: "+str(self.modelo)
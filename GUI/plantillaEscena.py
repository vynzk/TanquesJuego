# -*- encoding: utf-8 -*-

class Escena:
    """Clase abstracta para construir las escenas del video juego"""

    def __init__(self, director):
        self.director = director 
        self.iterador= self.director.iterador
    
    def on_update(self): #no se para que es
        "Actualización lógica que se llama automáticamente desde el director."
        raise NotImplemented("Tiene que implementar el método on_update.")

    def on_event(self, event): #creo que son los eventos que van dentro de la escena...
        "Se llama cuando llega un evento especifico al bucle."
        raise NotImplemented("Tiene que implementar el método on_event.")

    def on_draw(self, screen): #para mostrar cosas en pantalla
        "Se llama cuando se quiere dibujar la pantalla."
        raise NotImplemented("Tiene que implementar el método on_draw.")
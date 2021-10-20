#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import plantillaEscena
from utilidades.utilidades import *

class EscenaHome(plantillaEscena.Escena):

    def __init__(self, director):  # constructor
        plantillaEscena.Escena.__init__(self, director)

    # sobreescritura de los metodos de plantilla escena
    def on_update(self):
        pass

    def on_event(self):
        pass

    def on_draw(self, screen):
        pygame.draw.line(screen, ROJO, [10, 10], [650, 470], 2)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

#módulos GUI
import director
import escenaHome
import escenaJuego
#------------------#
def main():
    """Se inicaliza el director y escenas"""
    dir = director.Director()
    home = escenaHome.EscenaHome(dir)
    juego = escenaJuego.EscenaJuego(dir)
    dir.cambiarEscena(juego) # se define primera escena...
    
    dir.gameLoop()

if __name__ == '__main__':
    pygame.init()
    main()
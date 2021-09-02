import pygame
import sys
import math

cero = 0
velocidad = 85
angulo = 60
constante = 50

ancho = 800
alto = 600


contador=10

color_rojo = (255,0,0)
color_negro = (0,0,0)
color_azul = (0,0,255)
color_verde = (0,255,0)

jugador_size = 50
jugador_pos = [10, 540]

enemigo_size = 50
enemigo_pos = [740, 540]

proyectil_size = 25
proyectil_pos = [jugador_pos[0]+50, jugador_pos[1]+14]

ventana = pygame.display.set_mode((ancho, alto))

game_over = False
clock = pygame.time.Clock()

def colisiones(enemigo_pos, proyectil_pos):
    px = proyectil_pos[0]
    py = proyectil_pos[1]
    ex = enemigo_pos[0]
    ey = enemigo_pos[1]

    if (ex >= px and ex <(px + proyectil_size)) or (px >= ex and px < (ex + enemigo_size)):
        if (ey >= py and ey <(py + proyectil_size)) or (py >= ey and py < (ey + enemigo_size)):
            return True
        return False

def proyectil(proyectil_pos):
    if proyectil_pos[1] < ancho and proyectil_pos[1] != (jugador_pos[0]+50):
        proyectil_pos[0] += 20

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        #if event.type == pygame.KEYDOWN:

        #    xp=proyectil_pos[0]
        #    if event.key == pygame.K_SPACE:
        #        xp += proyectil_size
                

        #    proyectil_pos[0] = xp

    #ventana.fill(color_negro)


    pygame.draw.rect(ventana, color_azul, 
        (jugador_pos[0], jugador_pos[1],
        jugador_size, jugador_size))

    pygame.draw.rect(ventana, color_rojo, 
        (enemigo_pos[0], enemigo_pos[1], 
        enemigo_size, enemigo_size))


    while cero<=constante:
        pygame.draw.rect(ventana, color_verde, 
        (proyectil_pos[0], proyectil_pos[1], 
        proyectil_size, 20))

        x = jugador_pos[0]+50 + cero*velocidad*math.cos(angulo*3.1416/180)
        y = jugador_pos[1]+14 - (cero*velocidad*math.sin(angulo*3.1416/180) - (9.81*cero*cero)/2)
        proyectil_pos[0] = x
        proyectil_pos[1] = y
        cero+=0.25
        
        #hacer que el proyectil deje rastro

        if colisiones(enemigo_pos, proyectil_pos):
            game_over = True


    #if proyectil_pos[1] < ancho and proyectil_pos[1] != (jugador_pos[0]+50):
    #    proyectil_pos[0] += 20

    #pygame.draw.rect(ventana, color_azul, 
    #	(jugador_pos[0], jugador_pos[1],
    # 	jugador_size, jugador_size))

    #pygame.draw.rect(ventana, color_rojo, 
    #	(enemigo_pos[0], enemigo_pos[1], 
    #	enemigo_size, enemigo_size))

    #pygame.draw.rect(ventana, color_verde, 
    #	(proyectil_pos[0], proyectil_pos[1], 
    #	proyectil_size, 20))

    

    clock.tick(30)
    pygame.display.update()

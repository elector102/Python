import pygame, sys


pygame.init()
BLACK = [0,0,0]
WIDTH = 1280
HEIGHT = 1024
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

windowSurface.fill(BLACK)

while True:
    events = pygame.event.get()
    for event in events:
        if event.key == pygame.K_p:
             #Do what you want to here
             pass
        if event.type == QUIT:
             pygame.quit()
             sys.exit()
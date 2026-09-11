import sys
import random
import pygame

tile_scale = 7
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
tile = pygame.surface.Surface((tile_scale,tile_scale)) 
def filt(reg, cull):
    reg -= cull
    if reg < 0:
        reg = 0
    if reg > 255:
        reg = 255
    return reg
cull = 0
pygame.mouse.set_visible(False)
while True:
    screen.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    for y in range(0,screen.get_rect().height//tile_scale+1):
        for x in range(0,screen.get_rect().width//tile_scale+1):
            tile.fill((filt(random.randint(0,55),cull),filt(random.randint(0,155),cull),filt(random.randint(0,255),cull)))
            screen.blit(tile, (x*tile_scale,y*tile_scale))
    pygame.display.flip()
    if random.randint(0,10) == 7:
        cull += 1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
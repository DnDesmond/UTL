from Colour_Picker import picks as base_picks
import pygame
pygame.init()
import sys
import os

os.chdir("UTL")

def picks(point, width, range):
    return base_picks(point, width, range, inverse_channels=[1,0,0,0,0,0])

def recolour(surface, colour, new):
    surface = pygame.PixelArray(surface)
    surface.replace((colour),(new))
    surface = surface.make_surface()
    return surface

surface = pygame.image.load("Rot.png")
surface = pygame.transform.scale(surface, (1680,1050))
surfactant = surface.copy()
surfactant = pygame.transform.scale(surfactant, (1680,1))
display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
# image = pygame.image.load("Vignet.png")
# image = recolour(image,(102,102,102),(25,25,25))
# image.set_colorkey((255,255,255))#
vignette = (25,25,25)

# for cat in range(0,1680):
#     surfactant.fill(picks((cat,0), 1680, 500))
#     surface.blit(surfactant, (cat,0))

paused = False
ranged = 0
while True:
    the_base = picks((pygame.mouse.get_pos()[0],0), 1680, ranged)
    the_list = list(the_base)
    the_list.reverse()
    the_list = tuple(the_list)
    # image = recolour(image,vignette,the_list)
    # vignette = the_list
    # image.set_colorkey((255,255,255))
    # for cat in range(0,1680):
    #     surfactant.fill(picks((cat,0), 1680, ranged))
    #     surface.blit(surfactant, (cat,0))
    for cat in range(0,1050):
        surfactant.fill(picks((cat,cat), 1050, ranged))
        surface.blit(surfactant, (0,cat))
    display.blit(surface, (0,0))
    # display.blit(image, (0,0))
    if ranged>1680*0.6:
        ranged = 0
    if not paused:
        ranged += 2
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_p:
                if paused:
                    paused = False
                else:
                    paused = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            newer = []
            for num in the_base:
                newer.append(round(num))
            newer = f"\n{str(newer)}"
            with open("The_Chosen.py", 'a') as file:
                file.write(newer)
            # print(newer)
            # print("\n")
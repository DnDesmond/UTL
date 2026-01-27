from Colour_Picker import picks as base_picks
import pygame
pygame.init()
import sys
import os

# os.chdir("UTL")

def picks(point, width, range):
    return base_picks(point, width, range, inverse_channels=[0,0,0,0,0,0])

def recolour(surface, colour, new):
    surface = pygame.PixelArray(surface)
    surface.replace((colour),(new))
    surface = surface.make_surface()
    return surface

surface = pygame.image.load("Rot.png")
surface = pygame.transform.scale(surface, (1680,1050))
surfactant = surface.copy()
surfactant = pygame.transform.scale(surfactant, (1,1280))
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
    for cat in range(0,1280):
        surfactant.fill(picks((cat,cat), 1280, ranged))
        surface.blit(surfactant, (cat,0))
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
                # newer.append(round(num))
                newer = tuple([round(x) for x in picks(pygame.mouse.get_pos(), 1280, ranged)])
            newer = f"\n{str(newer)}"
            with open("The_Chosen.py", 'a') as file:
                file.write(newer)
            # print(newer)
            # print("\n")
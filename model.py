import sys
import random
import csv
import pygame
from pygame import *
pygame.init()

class Core:
    """Creates a core to hold the relevant variables centrally"""

    def __init__(self):
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.height, self.width = self.screen_rect.height, self.screen_rect.height
        self.clock = pygame.time.Clock()
        with open("Recieved_data.csv", "r") as file:
            handled = [x for x in file]
            filt = ""
            for x in handled:
                filt += x
            handled = filt.strip()
            handled = handled.replace(" ", "")
            handled = handled.replace("\n", "")
            iter = 0
            # while True:
            #     try:
            #         handled.
        self.cezve = csv.reader(handled, delimiter=",")
        part = ""
        parts = []
        iter = 0
        for line in self.cezve:
            part += f"{line[0]},"
            if iter > 2:
                parts.append(part)
                iter = 0
            iter += 1
        print(parts)
        # for part in parts:
        #     print(f"{part}\n")
        # print(handled)
        # print(self.already)
        self.socratic = []
        self.platonic = []
        self.diogenic = []
        self.thinks = [self.socratic, self.platonic, self.diogenic]
        y = 0
        for cat in range(0,20):
            y += random.randint(-25,24)
            self.socratic.append(y+500)
            self.platonic.append(y+500)
            self.diogenic.append(y+500)
        self.paper = Paper(self)
    
    def pulse(self):
           self.check_events()
           self.update_screen()
           self.clock.tick(60)
    
    def update_screen(self):
        self.screen.fill((200,210,200))
        self.paper.update()
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# each tick remove the zero ind and add a new rightmost, recolour the center with pixels at points for output data corresponding to a 1:100 scale

class Paper:
    """Creates and tracks the 'paper' upon which the graph is shown"""

    def __init__(self, core:Core):
        self.core = core
        self.screen = self.core.screen
        self.screen_rect = self.core.screen_rect
        self.image = pygame.surface.Surface((1680,1050))
        self.linea:list[pygame.surface.Surface] = []
        for x in range(0,1680):
            self.linea.append(pygame.surface.Surface((1,1050)))
        for line in self.linea:
            line.fill((200,220,200))
        # for x in range(500,600):
        #     self.linea[x].fill((250,0,40))
        cols = ["red", "green", "blue"]
        self.red = pygame.surface.Surface((2,2))
        self.red.fill((255,0,0))
        self.green = pygame.surface.Surface((2,2))
        self.green.fill((0,255,0))
        self.blue = pygame.surface.Surface((2,2))
        self.blue.fill((0,0,255))
        self.past_whys = [self.core.socratic[0],self.core.platonic[0],self.core.diogenic[0]]
    
    def update(self):
        for line in self.linea:
            self.screen.blit(line, (self.linea.index(line),0))
        self.cycle()
        # self.linea[random.randint(0,len(self.linea)-1)].fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    
    def cycle(self):
        self.linea.remove(self.linea[0])
        self.linea.append(pygame.surface.Surface((1,1050)))
        self.linea[-1].fill((200,220,200))
        whys = [self.core.socratic[0], self.core.platonic[0], self.core.diogenic[0]]
        # y = self.core.socratic[0]
        self.linea[840].blit(self.red, (0,1050-self.core.socratic.pop(0)))
        self.linea[840].blit(self.green, (0,1050-self.core.platonic.pop(0)))
        self.linea[840].blit(self.blue, (0,1050-self.core.diogenic.pop(0)))
        pygame.draw.line(self.linea[840], (255,0,0), (0,1050-whys[0]), (0,1050-self.past_whys[0]))
        pygame.draw.line(self.linea[840], (0,255,0), (0,1050-whys[1]), (0,1050-self.past_whys[1]))
        pygame.draw.line(self.linea[840], (0,0,255), (0,1050-whys[2]), (0,1050-self.past_whys[2]))
        self.past_whys = whys.copy()

class Populus:
    """Creates the actual model and returns values for risk and population"""

    def __init__(self, core:Core):
        self.core = core
        # Due to difficulty in specific populations we model on a sample of 2000
        self.pop = 2000
        # Expected life of 4-6 weeks in days
        self.lifespan = 35
        self.additions = []

    def loss(self):
        death_rate = self.risk
    
    def gain(self):
        if self.core.screen:
            pass


if __name__ == "__main__":
    core = Core()
    while True:
        core.pulse()
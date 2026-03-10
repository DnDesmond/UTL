import sys
import random
from math import sin, pi
import csv
import json
import pygame
from pygame import *
pygame.init()

from cleaner import cleans #type:ignore

class Core:
    """Creates a core to hold the relevant variables centrally"""

    def __init__(self):
        """Initialises all values and imports a version of the received data which has been cleaned"""
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.height, self.width = self.screen_rect.height, self.screen_rect.height
        self.clock = pygame.time.Clock()
        # with open("Recieved_data.csv", "r") as file:
        #     handled = [x for x in file]
        #     filt = ""
        #     for x in handled:
        #         filt += x
        #     handled = filt.strip()
        #     handled = handled.replace(" ", "")
        #     handled = handled.replace("\n", "")
        #     iter = 0
            # while True:
            #     try:
            #         handled.
        # self.cezve = csv.reader(handled, delimiter=",")
        # part = ""
        # parts = []
        # iter = 0
        # print(self.cezve)
        # for line in self.cezve:
        #     part += f"{line[0]},"
        #     if iter > 1:
        #         parts.append(part)
        #         iter = 0
        #     iter += 1
        # print(parts)
        # for part in parts:
        #     print(f"{part}\n")
        # print(handled)
        # print(self.already)
        cleans()
        self.cleaned = json.load(open("Cleaned_data.json", "r", encoding="utf-8"))
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
        self.wipe()
        vis_mult = 6
        self.vis_mult = vis_mult
        self.sinus = []
        for x in self.cleaned:
            self.socratic.append(vis_mult*x[1])
            self.platonic.append(vis_mult*x[0])
            self.diogenic.append(vis_mult*x[2]*100)
        for x in range(0,3601):
            x = x/40
            # x = x%10
            # x = 5-x
            x = (x*pi)/2
            self.sinus.append((sin(0.3*x)+2)*100)
        self.socratic = self.sinus.copy()
        self.paper = Paper(self)
    
    def pulse(self):
        """Runs as a central function to continue progression of the module"""
        self.check_events()
        self.update_screen()
        self.clock.tick(60)
    
    def wipe(self):
        """Removes all data contained in the data lists"""
        for mind in self.thinks:
            mind.clear()
    
    def update_screen(self):
        """Updates the screen with live data"""
        self.screen.fill((200,210,200))
        self.paper.update()
        pygame.display.flip()

    def check_events(self):
        """Checks for keyboard events to see whether to quit"""
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
        self.risky()
    
    def risky(self):
        temp = self.core.socratic[0]/self.core.vis_mult
        soil = self.core.platonic[0]/self.core.vis_mult
        #Clone of risk calculation model from microbit
        risk = 0
        # Accepts half the risk to be the same as the soil moisture level.
        risk += 0.5 - 0.5 * (min(soil, 80) / 80)
        # Renders a risk degree suitable to the survivability of C. Brunneus in variable temperature ranges.
        if temp > 30:
            risk += 0.5
        elif temp > 20 and temp <= 30:
            risk += -0.2
        else:
            risk += 0.5
        self.core.diogenic[0] = risk*self.core.vis_mult*100
        print([risk,temp,soil])

# model based upon changes to the already gathered data, add what-ifs for: sinesoidal temp measure, falling or rising soil with temp or time, disasterousness, (you'll find others)

if __name__ == "__main__":
    core = Core()
    while True:
        core.pulse()
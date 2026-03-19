import sys
import random
from math import sin, pi
import time
import csv
import json
pygammy = input("Do you want added visualistion (pygame module required)\nY/N: ")
# pygammy = "y"

if pygammy.lower() == "y":
    try:
        import pygame
        # from pygame import *
        pygame.init()
        pygammy = True
    except ModuleNotFoundError:
        pygammy = False
        print("Pygame module not found, proceeding with reduced visuals.")
else:
    pygammy = False

from cleaner import cleans #type:ignore

class Core:
    """Creates a core to hold the relevant variables centrally"""

    def __init__(self, pygammy=False):
        """Initialises all values and imports a version of the received data which has been cleaned"""
        self.pygammy = pygammy
        self.temp = 0
        print("For each what-if enter 0 for False or 1 for True:")
        val = input("\tPreset scenarios: ")
        # Accepts inputs for values for AR 2
        drought, falsify, humid, shivers = [False for x in range(0,4)]
        if val == "0":
            val = input("\tSine-Wave Temperatures: ")
            falsify = False
            if val == "1":
                falsify = True
            val = input("\tDrought: ")
            drought = False
            if val == "1":
                drought = True
            val = input("\tHumid: ")
            humid = False
            if val == "1":
                humid = True
            val = input("\tExtreme Cold: ")
            shivers = False
            if val == "1":
                shivers = True
            self.shivers = shivers
        elif val == "2":# For testing of non_adjusted scenario, (dev settings)
            falsify = True
        else:
            val = input("\tGlobal Warming[0], Flooding[1]: ")
            falsify = True
            if val == "0":
                self.temp = "1"
                drought = True
            else:
                self.temp = "-2"
                humid = True
        cleans(falsify, drought, humid, shivers)
        self.falsify = falsify
        self.drought = drought
        self.humid = humid
        self.shivers = shivers
        print("\nPreparing model...")
        time.sleep(1)
        if self.pygammy:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            self.screen_rect = self.screen.get_rect()
            self.height, self.width = self.screen_rect.height, self.screen_rect.width
            self.clock = pygame.time.Clock()
        else:
            self.height, self.width = 1050, 1680
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
            if falsify:
                self.socratic.append(x[1])
            else:
                self.socratic.append(vis_mult*x[1])
            self.socratic[-1] += vis_mult*float(self.temp)*20
            self.platonic.append(vis_mult*x[0])
            self.diogenic.append(vis_mult*x[2]*100)
        self.modelling = False
        self.lastemp = 3600
        if self.pygammy:
            self.paper = Paper(self)
        else:
            self.paper = Papyrus(self)
    
    def pulse(self):
        """Runs as a central function to continue progression of the module"""
        if self.pygammy:
            self.check_events()
            self.clock.tick(60)
        if self.modelling:
            self.continuate()
        self.update_screen()
    
    def continuate(self):
        # Does the actual modelling to fulfill AR's 1 and 2
        self.diogenic = []
        if self.pygammy:
            y = self.paper.past_whys[1]
        else:
            try:
                y = self.platonic[-1]
            except IndexError:
                y = 25
        if y > 100:
            self.platonic.append(y+random.randint(-4,3))
        else:
            self.platonic.append(y+random.randint(-2,5))
        x = self.lastemp
        self.lastemp += 1
        x = x/40
        x = (x*pi)/2
        # Upon switching to modelling instead of displaying data Sine-Wave temperatures are activated by default
        self.socratic.append((((sin(0.3*x)+2))*100)+random.randint(-10,11))
        if self.shivers:
            self.socratic[-1] -= random.randint(20,36)
        # Accounts for live disasters under modelling
        if self.humid:
            self.platonic[-1] += 30
            self.socratic[-1] += 25
        if self.drought:
            self.platonic[-1] -= 40
        self.paper.risky()
    
    def wipe(self):
        """Removes all data contained in the data lists"""
        for mind in self.thinks:
            mind.clear()
    
    def update_screen(self):
        """Updates the screen with live data"""
        if self.pygammy:
            self.screen.fill((200,210,200))
            self.paper.update()
            pygame.display.flip()
        else:
            self.paper.update()

    def check_events(self):
        """Checks for keyboard events to see whether to quit"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# each tick remove the zero ind and add a new rightmost, recolour the center with pixels at points for output data corresponding to a 1:100 scale

class Papyrus:
    def __init__(self, core:Core):
        """Creates a simplified version of Paper for those without the proper modules."""
        self.core = core
    
    def update(self):
        # Simplified version of the Paper update and cycle functions combined
        try:
            try:
                self.risky()
            except IndexError:
                self.core.continuate()
            self.core.socratic.pop(0)
            self.core.platonic.pop(0)
            self.core.diogenic.pop(0)
        except IndexError:
            self.core.continuate()
    
    def risky(self):
        # Finds a risk value based on the current data
        temp = self.core.socratic[0]/self.core.vis_mult
        soil = self.core.platonic[0]/self.core.vis_mult
        #Clone of risk calculation model from microbit
        risk = 0
        # Accepts half the risk to be the same as the soil moisture level. BR 2
        risk += 0.5 - 0.5 * (min(soil, 80) / 80)
        # Renders a risk degree suitable to the survivability of C. Brunneus in variable temperature ranges. BR 2
        if temp > 30:
            risk += 0.5
        elif temp > 20 and temp <= 30:
            risk += -0.2
        else:
            risk += 0.5
        self.core.diogenic.insert(0,risk*self.core.vis_mult*100)
        # if not self.core.modelling:
        #     risk = (self.core.diogenic[0]/(self.core.vis_mult*100))-1
        print(f"{[round(soil, 2),round(temp, 2),round(risk, 2)]}")
        if risk < 0.2:
            final = "Low"
        elif risk >= 0.2 and risk <= 0.7:
            final = "Medium"
        else:
            final = "High"
        print(f"Risk Assessed as: {final}")

class Paper(Papyrus):
    """Creates and tracks the 'paper' upon which the graph is shown"""

    def __init__(self, core:Core):
        super().__init__(core)
        # Initialises requirements for display to properly function
        self.core = core
        self.screen = self.core.screen
        self.screen_rect = self.core.screen_rect
        self.width, self.height = self.core.width, self.core.height
        self.image = pygame.surface.Surface((self.width,self.height))
        # Hosts lines for "rotary" display of data
        self.linea:list[pygame.surface.Surface] = []
        for x in range(0,self.width):
            self.linea.append(pygame.surface.Surface((1,self.height)))
        for line in self.linea:
            line.fill((200,220,200))
        # The colours used for the lines being tracked
        cols = ["red", "green", "blue"]
        self.red = pygame.surface.Surface((2,2))
        self.red.fill((255,0,0))
        self.green = pygame.surface.Surface((2,2))
        self.green.fill((0,255,0))
        self.blue = pygame.surface.Surface((2,2))
        self.blue.fill((0,0,255))
        self.past_whys = [self.core.socratic[0],self.core.platonic[0],self.core.diogenic[0]]
    
    def update(self):
        # Shows all lines and cycles data for display
        for line in self.linea:
            self.screen.blit(line, (self.linea.index(line),0))
        self.cycle()
        # self.linea[random.randint(0,len(self.linea)-1)].fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    
    def cycle(self):
        self.linea.remove(self.linea[0])
        self.linea.append(pygame.surface.Surface((1,self.height)))
        self.linea[-1].fill((200,220,200))
        # Updates dots
        try:
            whys = [self.core.socratic[0], self.core.platonic[0], self.core.diogenic[0]]
            self.linea[840].blit(self.red, (0,self.height-self.core.socratic.pop(0)))
            self.linea[840].blit(self.green, (0,self.height-self.core.platonic.pop(0)))
            self.linea[840].blit(self.blue, (0,self.height-self.core.diogenic.pop(0)))
        except IndexError:
            self.modelling = True
            self.core.continuate()
            whys = [self.core.socratic[0], self.core.platonic[0], self.core.diogenic[0]]
        # Draws line to give the appearance of the lines tracking behind the dots
        pygame.draw.line(self.linea[840], (255,0,0), (0,self.height-whys[0]), (0,self.height-self.past_whys[0]))
        pygame.draw.line(self.linea[840], (0,255,0), (0,self.height-whys[1]), (0,self.height-self.past_whys[1]))
        pygame.draw.line(self.linea[840], (0,0,255), (0,self.height-whys[2]), (0,self.height-self.past_whys[2]))
        pygame.draw.line(self.screen, (125,125,125), (0,self.height-180), (self.width,self.height-180))
        pygame.draw.line(self.screen, (125,125,125), (0,self.height-120), (self.width,self.height-120))
        self.past_whys = whys.copy()
        # Updates risk values and accounts for missing data
        try:
            self.risky()
        except IndexError:
            self.core.continuate()

print(pygammy)
if __name__ == "__main__":
    core = Core(pygammy)
    while True:
        core.pulse()
        if not pygammy:
            time.sleep(0.1)
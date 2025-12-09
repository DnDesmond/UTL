import sys 
import os
import pygame
pygame.init()
from non import letters
from sraith import diction #type:ignore
import random

os.chdir("C:/Users/isaac")
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (879,73)

fadaí = {"a":"á","e":"é","i":"í","o":"ó","u":"ú"}

errs = [" ", ".", ",", "-", "'", "\"", ":", "!"]
ends = [".", "", ". ", "!"]

class Engine:
    """It's a pun"""

    def __init__(self):
        self.screen = pygame.display.set_mode((400,400))
        self.screen_rect = self.screen.get_rect()
        self.width = self.screen_rect.width
        self.height = self.screen_rect.height
        self.clock = pygame.time.Clock()
        self.capped = False
        self.fada = False
        self.font = pygame.font.Font("Odd.otf", 21)
        self.choices = ["first", "second", "third", "fourth", "fifth", "sixth"]
        # self.choices = ["first", "second"]
        self.chosen = random.choice(self.choices)
        self.chosen = self.choices[5]
        self.second = Alt(self.chosen, self)#first
        self.covered = 0
        # self.second.bocht, self.second.spórt, self.second.greann = True, True, True
        self.hidden = True
        # self.hidden = False

    def passage(self):
        try:
            if self.second.subs[0][0] in errs:
                self.second.subs[0] = self.second.subs[0][1:]
            if self.second.subs[0] in ends:
                self.second.subs = self.second.subs[1:]
                self.second.widths = self.second.widths[1:]
                self.covered += 1 
        except IndexError:
            pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LSHIFT:
                    self.capped = True
                if event.key == pygame.K_RALT:
                    self.fada = True
                for char in letters:
                    if event.key == getattr(pygame, f"K_{char}"):
                        if self.fada:
                            if char in fadaí.keys():
                                char = fadaí[char]
                        if self.capped:
                            char = char.upper()
                        try:
                            if self.second.subs[0][0] in errs:
                                self.second.subs[0] = self.second.subs[0][1:]
                            if char == self.second.subs[0][0]:
                                self.second.subs[0] = self.second.subs[0][1:]
                                break
                        except:
                            pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.capped = False
                if event.key == pygame.K_RALT:
                    self.fada = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def texts(self):
        y = 0
        colour_t = (160,160,160)#(140,140,140)#(70,0,20)#(140,140,140)
        colour_b = (70,0,20)
        box = self.font.render(f"{self.second.par}", (70,0,20) , (140,140,140))
        for line in self.second.backs:
            box = self.font.render(line, 0, (140,240,140))
            self.screen.blit(box, ((self.width-box.get_rect().width)/2, y))
            y += 22
        y = self.covered*22
        for line in self.second.subs:
            if not self.hidden:
                box = self.font.render(line, 0, colour_t)#, colour_t)
            if self.hidden:
                box = self.font.render(line, 0, colour_t, colour_t)
            self.screen.blit(box, (self.dist_calc(line,box), y))
            y += 22
    
    def dist_calc(self, line:str, box:pygame.surface.Surface):
        dist = (self.width-self.second.widths[self.second.subs.index(line)]) - box.get_rect().width
        return dist

    def run_it(self):
        while True:
            self.screen.fill((70,0,20))
            self.check_events()
            self.passage()
            self.texts()
            self.clock.tick(60)
            pygame.display.flip()

class Alt:
    """Scríobheann an rud seo alt amháin"""

    def __init__(self, text:str, runner:Engine):
        self.runner = runner
        self.lá = False
        self.bocht = False
        self.spórt = False
        self.greann = False
        self.scoil = False
        self.blian = False
        self.par = f"{"x"*1000}"
        self.lines = diction["Obair Dhian"][text].split(".")
        self.subs = []
        for num in range(len(self.lines)):
            self.lines[num] += "."
        self.widths = []
        self.linearity()
        self.backs = self.subs.copy()
    
    def linearity(self):
        words = []
        for line in self.lines:
            words += line.split(" ")
        lengthage = 0
        negst = ""
        cur = ""
        ind = 0
        for word in words:
            if lengthage + len(negst) < 50:
                cur += word + " "
                lengthage = len(cur)
            else:
                # if cur != ", ":
                self.subs.append(cur)
                width = self.runner.font.render(self.subs[-1], 0, (70,0,20)).get_rect().width
                dist = (self.runner.width-width)/2
                self.widths.append(dist)
                # negst = ""
                cur = word + " "
                lengthage = len(cur)
            ind += 1
            try:
                negst = words[ind+1]
            except IndexError:
                pass
        self.subs.append(cur)
        width = self.runner.font.render(self.subs[-1], 0, (70,0,20)).get_rect().width
        dist = (self.runner.width-width)/2
        self.widths.append(dist)


# for line in second.lines:
#     print(line)
runner = Engine()
runner.run_it()
import sys 
import os
import pygame
pygame.init()
import random
import time
import json
from non import letters
from sraith import sraiths #type:ignore
from RP import resource_path as rp

sraiths = json.load(open("camel.txt", "r", encoding="utf-8"))

# keys = [x for x in sraiths.keys()]
# t = sraiths[keys[0]]
# sraiths[keys[0]] = sraiths[keys[1]]
# sraiths[keys[1]] = t

# os.chdir("C:/Users/isaac")
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (879,73)

fadaí = {"a":"á","e":"é","i":"í","o":"ó","u":"ú"}
umlauten = {"a":"ä","o":"ö","u":"ü"}

errs = [" ", ".", ",", "-", "'", "\"", ":", "!"]
ends = [".", "", ". ", "!"]

class Engine:
    """It's a pun"""

    def __init__(self, width=400, height=400, line_spacing=22):
        self.screen = pygame.display.set_mode((width,height))
        self.screen_rect = self.screen.get_rect()
        self.width = self.screen_rect.width
        self.height = self.screen_rect.height
        self.clock = pygame.time.Clock()
        self.capped = False
        self.fada = False
        self.umlaut = False
        self.char_lim = 50
        # basic y increment = 22
        self.y_inc = line_spacing
        self.colour_t = (160,160,160)
        self.colour_s = (140,240,140)
        self.font = pygame.font.Font(rp("Odd.otf"), 21)
        # self.choices = ["first", "second", "third", "fourth", "fifth", "sixth"]
        self.sraiths:list[dict] = sraiths
        # for name,content in sraiths.items():
        #     setattr(self, name, content)
        #     self.sraiths.append(getattr(self, name))
        self.choices = [x for x in self.sraiths[[x for x in self.sraiths.keys()][0]]]
        # self.choices = ["first", "second"]
        self.chosen = random.choice(self.choices)
        self.chosen = self.choices[0]
        self.second = Alt(self.chosen, self)#first
        self.covered = 0
        # self.second.bocht, self.second.spórt, self.second.greann = True, True, True
        self.hidden = True
        # self.hidden = False
        self.titles = [x for x in self.sraiths.keys()]
        # self.menus:list[Menu] = []
        self.menu_big = Big_Menu(self.titles, self)
        self.backs = self.chosen
        self.start = time.time()

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
        # for button in self.menu_big.buttons:
        #     if button.rect.collidepoint(pygame.mouse.get_pos()):
        #         self.menu_big.relist(button.text)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSLASH:
                    if self.menu_big.hidden:
                        self.menu_big.hidden = False
                        for menu in self.menu_big.menus:
                            menu.hidden = False
                    else:
                        self.menu_big.hidden = True
                        for menu in self.menu_big.menus:
                            menu.hidden = True
                if event.key == pygame.K_0:
                    if self.hidden:
                        self.hidden = False
                    else:
                        self.hidden = True
                if event.key == pygame.K_ESCAPE:
                    self.bow()
                if event.key == pygame.K_LSHIFT:
                    self.capped = True
                if event.key == pygame.K_RALT:
                    self.fada = True
                if event.key == pygame.K_LALT:
                    self.umlaut = True
                if event.key == pygame.K_9:
                    self.rewrite(self.backs, sraith=sraiths[self.menu_big.titles[self.menu_big.menus.index(self.menu_big.forth_menu)]])
                for char in letters:
                    if event.key == getattr(pygame, f"K_{char}"):
                        if self.fada:
                            if char in fadaí.keys():
                                char = fadaí[char]
                        if self.umlaut:
                            if char in umlauten.keys():
                                char = umlauten[char]
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
                if event.key == pygame.K_LALT:
                    self.umlaut = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.menu_big.hidden:
                    col = False
                    for button in self.menu_big.buttons:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            self.menu_big.relist(button.text)
                            self.menu_big.cast = button
                            col = True
                    for button in self.menu_big.forth_menu.buttons:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            self.rewrite(button.text, sraith=sraiths[self.menu_big.titles[self.menu_big.menus.index(self.menu_big.forth_menu)]])
                            self.menu_big.last = button
                            col = True
                    if col == False:
                        self.menu_big.hidden = True
                        for menu in self.menu_big.menus:
                            menu.hidden = True
            if event.type == pygame.QUIT:
                self.bow()
    
    def bow(self):
        pygame.quit()
        # with open("Timekeeps.txt", 'a') as file:
        #     file.write(f"{str(time.time()-self.start)}\n")
        time.sleep(0.1)
        sys.exit()

    def texts(self):
        y = 0
        # y_inc = 29
        colour_t = self.colour_t#(160,160,160)#(140,140,140)#(70,0,20)#(140,140,140)
        colour_b = (70,0,20)
        box = self.font.render(f"{self.second.par}", (70,0,20) , (140,140,140))
        for line in self.second.backs:
            box = self.font.render(line, 0, self.colour_s)#(140,240,140))
            self.screen.blit(box, ((self.width-box.get_rect().width)/2, y))
            y += self.y_inc
        y = self.covered*self.y_inc
        for line in self.second.subs:
            if not self.hidden:
                box = self.font.render(line, 0, colour_t)#, colour_t)
            if self.hidden:
                box = self.font.render(line, 0, colour_t, colour_t)
            self.screen.blit(box, (self.dist_calc(line,box), y))
            y += self.y_inc
    
    def dist_calc(self, line:str, box:pygame.surface.Surface):
        dist = (self.width-self.second.widths[self.second.subs.index(line)]) - box.get_rect().width
        return dist

    def rewrite(self, title, sraith):
        self.second = Alt(title, self, sraith)
        self.backs = title
        self.covered = 0

    def run_it(self):
        while True:
            self.screen.fill((70,0,20))
            self.check_events()
            self.passage()
            self.texts()
            # self.menu.update()
            self.menu_big.update()
            self.clock.tick(60)
            pygame.display.flip()

class Alt:
    """Scríobheann an rud seo alt amháin"""

    def __init__(self, text:str, runner:Engine, sraith=sraiths[[x for x in sraiths.keys()][0]]):
        self.runner = runner
        self.lá = False
        self.bocht = False
        self.spórt = False
        self.greann = False
        self.scoil = False
        self.blian = False
        # 400 pixels works with 50 characters
        self.char_lim = self.runner.char_lim
        self.par = f"{"x"*1000}"
        self.lines = sraith[text].split(".")
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
            if lengthage + len(negst) < self.char_lim:
                cur += word + " "
                lengthage = len(cur)
            else:
                self.subs.append(cur)
                width = self.runner.font.render(self.subs[-1], 0, (70,0,20)).get_rect().width
                dist = (self.runner.width-width)/2
                self.widths.append(dist)
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

class Menu:
    """Attempts at a menu?"""

    def __init__(self, choices, engine:Engine, x=0, bg=False):
        self.engine = engine
        self.choices = choices
        self.image = pygame.surface.Surface((100,400))
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.x = x
        # self.image.fill((70,0,20))
        self.image.fill((4,4,4))
        self.image.set_colorkey((4,4,4))
        self.buttons:list[Button] = []
        if bg:
            self.background = bg
        else:
            self.background = (20,0,70)
        self._initialise_buttons()
        self.hidden = False
    
    def update(self):
        if not self.hidden:
            for button in self.buttons:
                button.update()
            self.engine.screen.blit(self.image, self.rect)
    
    def _initialise_buttons(self):
        for cat in range(len(self.choices)):
            setattr(self, self.choices[cat], Button(self.choices[cat], cat, self, 100, self.background))
            self.buttons.append(getattr(self, self.choices[cat]))

class Big_Menu(Menu):
    """Menu of Menus"""

    def __init__(self, menus, engine:Engine):
        self.background = (20,0,70)
        super().__init__(menus, engine, bg=self.background)
        self.menus:list[Menu] = []
        self.sraiths = engine.sraiths
        self.hidden = False
        self.titles = menus
        for title in self.titles:
            setattr(self, title, Menu([x for x in self.sraiths[title].keys()], engine, 100, self.background))
            self.menus.append(getattr(self, title))
        for button in self.buttons:
            button.rect.x -= 100
        self.forth_menu = self.menus[0]
        self.last = self.menus[0].buttons[0]
        self.cast = self.buttons[0]
    
    def relist(self, title):
        self.forth_menu = self.menus[self.titles.index(title)]
    
    def update(self):
        self.forth_menu.update()
        return super().update()
        


class Button:
    """Creates a menu button"""

    def __init__(self, text, iter, menu:Menu, x=0, bg=False):
        self.menu = menu
        self.text = text
        self.image = pygame.surface.Surface((100,20))
        self.rect = self.image.get_rect()
        self.rect.y += iter*20
        self.rect.x += x
        self.image.fill((70,0,20))
        self.image.blit(self.menu.engine.font.render(text, 0, (120,120,120)), (0,0))
        self.lighter = False
        if bg:
            self.background = bg
        else:
            self.background = (20,0,70)
        self.background_l = [x+30 for x in self.background]
        self.background_l[2] -= 10
    
    def update(self):
        self.brighter()
        self.imager()
        self.menu.image.blit(self.image, (0,self.rect.y))

    def imager(self):
        if self.menu.engine.menu_big.last == self:
            self.image.fill((180,0,70))
        elif self.menu.engine.menu_big.cast == self:
            self.image.fill((140,0,60))
        elif not self.lighter:
            self.image.fill(self.background)
        else:
            self.image.fill(self.background_l)

        self.image.blit(self.menu.engine.font.render(self.text, 0, (120,120,120)), (0,0))
    
    def brighter(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.lighter = True
        else:
            self.lighter = False
        

# for line in second.lines:
#     print(line)
if __name__ == "__main__":
    runner = Engine()
    runner.run_it()
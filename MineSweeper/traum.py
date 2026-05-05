import sys
import os
import random
import json
import time
from RP import resource_path as rp

os.chdir(f"{__file__.removesuffix(os.path.basename(__file__))}")

import pygame
pygame.init()

class Numb:
    """Creates the basic class"""

    def __init__(self, orient=0):
        self.screen = pygame.display.set_mode((600,600))
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = self.screen_rect.width, self.screen_rect.height
        self.orient = orient
        self.buttons:list[Button] = []
        # self.buttons2:list[Button] = []
        # self.buttons3:list[Button] = []
        # self.buttons4:list[Button] = []
        self.tiers = [self.buttons]#, self.buttons2, self.buttons3, self.buttons4]
        # if self.orient == -1:
        #     counts = 5
        #     tiers = 1
        #     self.diagonals = False
        #     self.counter = 0
        # elif self.orient == 0:
        #     counts = 3
        #     tiers = 3
        #     self.diagonals = True
        #     self.counter = 1
        # elif self.orient == 1:
        #     counts = 5
        #     tiers = 2
        #     self.diagonals = False
        #     self.counter = 0
        # elif self.orient == 2:
        #     counts = 2
        #     tiers = 3
        #     self.diagonals = True
        #     self.counter = 3
        with open(rp("loaf.json"), 'r') as file:
            deus = json.loads(file.readline())
            # print(deus)
        tritia = deus[str(orient)]
        counts = tritia["counts"]
        tiers = tritia["tiers"]
        self.diagonals = tritia["diagonals"]
        self.counter = tritia["counter"]
        hidden = tritia["hidden"]
        width = counts*50
        gap = (self.width-width)/2
        for cat in range(0,counts):
            setattr(self, f"button{cat}", Button(cat,self))
            self.buttons.append(getattr(self, f"button{cat}"))
            self.buttons[-1].rect.topleft = [(cat*50)+gap, 40]
        for tier in range(1,tiers):
            setattr(self, f"buttons{tier}", [])
            self.tiers.append(getattr(self, f"buttons{tier}"))
            for cat in range(0,counts):
                setattr(self, f"button{cat}", Button(cat, self, tier))
                self.tiers[-1].append(getattr(self, f"button{cat}"))
                self.tiers[-1][-1].rect.topleft = [(cat*50)+gap, 40+tier*50]
        self.font = pygame.font.match_font("Times New Roman")
        self.font = pygame.font.Font(self.font, 24)
        # if self.orient == 1:
        #     self.tiers[-1][2].hidden = True
        for core in hidden:
            self.tiers[core[0]][core[1]].hidden = True
        self.total = self._numerate()
        # print(self.total)
        # for cat in range(0,counts):
        #     setattr(self, f"button{cat}", Button(cat,self,1))
        #     self.buttons2.append(getattr(self, f"button{cat}"))
        #     self.buttons2[-1].rect.topleft = [(cat*50)+gap, 90]
        # for cat in range(0,counts):
        #     setattr(self, f"button{cat}", Button(cat,self,2))
        #     self.buttons3.append(getattr(self, f"button{cat}"))
        #     self.buttons3[-1].rect.topleft = [(cat*50)+gap, 140]
        # for cat in range(0,counts):
        #     setattr(self, f"button{cat}", Button(cat,self,3))
        #     self.buttons4.append(getattr(self, f"button{cat}"))
        #     self.buttons4[-1].rect.topleft = [(cat*50)+gap, 190]
        self.past = Button(-2, self, -2)
        self.clock = pygame.time.Clock()
    
    def runs(self):
        while True:
            self.check_events()
            self.update_screen()
            self.clock.tick(60)

    def update_screen(self):
        #self.screen.fill((89,61,193))#111,201,188
        self.screen.fill((231,221,208))
        if self.diagonals:
            self.screen.blit(self.font.render(f"Diagonals: {str(self.counter)}", False, (4,4,4), (231,221,208)), (20,20))
        for tier in self.tiers:
            for button in tier:
                button.update()
        pygame.display.flip()
        self.sojourn()
    
    def sojourn(self):
        if self.total == 0:
            time.sleep(1)
            self._ends(False, True)
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._keydowns(event)
            if event.type == pygame.KEYUP:
                self._keyups(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._mousedowns(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self._mouseups(event)
            if event.type == pygame.QUIT:
                self._ends()
    
    def _keydowns(self, event):
        if event.key == pygame.K_q:
            self._ends()
        if event.key == pygame.K_r:
            self._ends(True)
    
    def _keyups(self, event):
        pass
    
    def _mousedowns(self, event):
        if event.button == pygame.BUTTON_LEFT:
            for tier in self.tiers:
                for button in tier:
                    if not button.hidden:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            button.collisory()
                            self.past.post = False
                            self.past = button
                            self.past.post = True

    def _mouseups(self, event):
        pass

    def _ends(self, resets=False, ups=False):
        pygame.quit()
        if resets:
            pygame.init()
            game = Numb(self.orient)
            game.runs()
        if ups:
            try:
                pygame.init()
                game = Numb(self.orient+1)
                game.runs()
            except:
                pygame.quit()
                sys.exit()
        else:
            sys.exit()
    
    def _numerate(self):
        total = 0
        stretch = [[y.hidden for y in x] for x in self.tiers]
        for tier in stretch:
            for bool in tier:
                if not bool:
                    total += 1
        return total

class Button:
    """Creates a button"""

    def __init__(self, ind, king:Numb, y=0):
        self.game = king
        self.screen = self.game.screen
        self.image = pygame.surface.Surface((40,40))
        self.image.fill((30,29,104))
        self.beg = [130,129,204]
        self.rect = self.image.get_rect()
        self.collided = False
        self.devilled = False
        self.hidden = False
        self.diagonals = self.game.diagonals
        self.indexe = ind
        self.post = False
        self.sunday = True
        self.y = y
    
    def update(self):
        if (self.post and self.game.total > 0) and self.devilled == False:
            if self.sunday == False:
                self.image.fill((156,157,12))
            else:
                self.colourise()
        else:
            self.colourise()
        if not self.hidden:
            self.screen.blit(self.image, self.rect)

    def colourise(self):
        try:
            self.image.fill(self.beg)
        except ValueError:
            print(f"Invalid colour of: {self.beg}")
            self.game._ends()

    def collisory(self):
        ind = self.game.past.indexe
        y = self.game.past.y
        struck = False
        if not self.devilled:
            if self.diagonals:
                if (ind+1 == self.indexe or ind-1 == self.indexe) and (y+1 == self.y or y-1 == self.y):
                    if self.game.counter <= 0:
                        self.beg = [245,30,30]
                        self.devilled = True
                        struck = True
                    self.game.counter -= 1
            # Horizontally adjacent
            if (ind+1 == self.indexe or ind-1 == self.indexe) and y == self.y:
                self.beg = [245,30,30]
                self.devilled = True
            # Vertically Adjacent
            elif (y+1 == self.y or y-1 == self.y) and ind == self.indexe:
                self.beg = [245,30,30]
                self.devilled = True
            elif not struck:
                self._walters(ind, y)
        self.collided = self.collided == False

    def _walters(self, ind, y):
        # Vertically opposite
        if ind == self.indexe and (y == (len(self.game.tiers)-1)-(self.y)):
            self.beg = [245,30,30]
            self.devilled = True
        # Horizontally opposite
        elif (ind == (len(self.game.buttons)-1)-(self.indexe)) and y == self.y:
            self.beg = [245,30,30]
            self.devilled = True
        # Colour changes for valid selections
        elif not self.collided:
            self.beg = [x-100 for x in self.beg]
            self.game.total -= 1
        else:
            self.beg = [x+100 for x in self.beg]
            self.game.total += 1



if __name__ == "__main__":
    game = Numb(0)
    game.runs()
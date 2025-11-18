import sys
import os
from math import sqrt

import pygame
from pygame.sprite import Sprite

pygame.init()

from linearity import dotxline, eqs, other

# def horizon(point, point_2, point_3, point_4):
#     # eq_1 = eqs(point, point_2)
#     line_y = point[1]
#     eq_2 = eqs(point_3, point_4)
#     col_x = other(eq_2["cofx"], eq_2["coy"], line_y, eq_2["c"]) # finds the x value at the y value of the horizontal line
#     point_col = (col_x,line_y)
#     coll:bool = dotxline(point_col, point, point_2)
#     return coll

def horizon(vert, vert_2, hori, hori_2):
    coll = dotxline((vert[0],hori[1]),vert, vert_2) and dotxline((vert[0],hori[1]),hori, hori_2)
    return coll

class Game:
    """Does game"""

    def __init__(self):
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height
        self.player = Player(self)
        self.clock = pygame.time.Clock()
        self.horizons = [((401,600),(700,600)),((504,400),(510,400))]
        self.tears = [((501,600),(501,400))]
        self.temps = []
    
    def run_game(self):
        while True:
            self.check_events()
            self.update_screen()
            self.clock.tick(60)
    
    def update_screen(self):
        self.screen.fill((90,168,112))
        # if horizon(self.lines[0][0], self.lines[0][1], self.player.rect.center, self.screen_rect.center):
        #     self.screen.fill((176,150,150))
        self.player.update()
        for line in self.horizons:
            pygame.draw.line(self.screen, (190,190,190), line[0], line[1])
        for line in self.tears:
            pygame.draw.line(self.screen, (190,190,190), line[0], line[1])
        if len(self.temps) == 1:
            pygame.draw.line(self.screen, (215,104,157), self.temps[0], (pygame.mouse.get_pos()[0],self.temps[0][1]))
        pygame.display.flip()
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.player.down > 0:
                        self.player.down = 0
                    self.player.down -= 20
                    if self.player.down < -25:
                        self.player.down = -25
                        # self.player.rect.y -= 2
                    self.player.times = 0
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RIGHT:
                    self.player.rechts = True
                    self.player.hori_times = 0
                if event.key == pygame.K_LEFT:
                    self.player.links = True
                    self.player.hori_times = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.rechts = False
                if event.key == pygame.K_LEFT:
                    self.player.links = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(self.temps) < 1:
                    self.temps.append(pygame.mouse.get_pos())
                else:
                    self.temps.append((pygame.mouse.get_pos()[0],self.temps[0][1]))
                    self.horizons.append(self.temps.copy())
                    self.temps = []

class Player(Sprite):
    """Creates a playerish thingummy"""

    def __init__(self, game:Game):
        super().__init__()
        self.game = game
        self.scale = 30
        self.right = 0
        self.down = 0
        self.rechts = False
        self.links = False
        self.image = pygame.surface.Surface((self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.deli()
        self.exos = [self.rect.center]
        self.times = 0
        self.hori_times = 0

    def update(self):
        # self.deli()
        self.exos = [self.rect.center]
        self.motions()
        self.deli()
        self.colls()
        self.game.screen.blit(self.image, self.rect)
        self.times += 1
        self.hori_times += 1
    
    def deli(self):
        self.sides = [(self.rect.topleft, self.rect.bottomleft), (self.rect.topright, self.rect.bottomright)]
        self.caps = [(self.rect.topleft, self.rect.topright), (self.rect.bottomleft, self.rect.bottomright)]
        self.exos = [self.rect.center]
    
    def motions(self):
        if self.rechts and self.right < 12:
            self.right += 1
        if self.links and self.right > -12:
            self.right -= 1
        if self.right > 0:
            self.right -= 0.5
        if self.right < 0:
            self.right += 0.5
        
        self.rect.x += self.right

        if self.down < 20:
            self.down += 1
        self.rect.y += self.down

    
    def colls(self):
        for line in self.game.horizons:
            hit = False
            if horizon(self.sides[0][0], self.sides[0][1], line[0], line[1]):
                self.cour(line)
            if horizon(self.sides[1][0], self.sides[1][1], line[0], line[1]):
                self.cour(line)
        for line in self.game.tears:
            if horizon(line[0], line[1], self.caps[0][0], self.caps[0][1]):
                self.sacre(line)
            if horizon(line[0], line[1], self.caps[1][0], self.caps[1][1]):
                self.sacre(line)

        if self.rect.bottom > self.game.screen_height:
            self.rect.y -= self.rect.bottom - self.game.screen_height
            self.down = 0

    def cour(self, line):
        if self.times > 1:
            if self.down >= 0:
                self.rect.y -= self.rect.bottom - line[0][1]
            if self.down < 0:
                self.rect.y += line[0][1] - self.rect.top
                self.rect.y += 3
            self.deli()
            self.down = 0

    def sacre(self, line):
        if self.hori_times > 1:
            if self.right >= 0:
                self.rect.x -= self.rect.right - line[0][0]
            if self.right < 0:
                self.rect.x += line[0][0] - self.rect.left
                self.rect.x += 3
            self.deli()
            self.right = 0


game = Game()
if __name__ == "__main__":
    game.run_game()
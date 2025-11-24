import sys
import os
from math import sqrt

import pygame
from pygame.sprite import Sprite

pygame.init()

from linearity import dotxline, eqs, other, simuls

# def horizon(point, point_2, point_3, point_4):
#     # eq_1 = eqs(point, point_2)
#     line_y = point[1]
#     eq_2 = eqs(point_3, point_4)
#     col_x = other(eq_2["cofx"], eq_2["coy"], line_y, eq_2["c"]) # finds the x value at the y value of the horizontal line
#     point_col = (col_x,line_y)
#     coll:bool = dotxline(point_col, point, point_2)
#     return coll

def diagonal_colls(point, point_2, vert_3, vert_4):
    # if vert_3[0] == vert_4[0]:
        eq_1 = eqs(point, point_2)
        col_x = vert_3[0]
        col_y = other(eq_1["coy"], eq_1["cofx"], col_x, eq_1["c"])
        return (col_x,col_y)
    # else:
    #     eq_1 = eqs(point, point_2)
    #     col_y = vert_3[1]
    #     col_x = other(eq_1["cofx"], eq_1["coy"], col_y, eq_1["c"])
    #     return (col_x,col_y)

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
        self.horizons = []#[((401,600),(700,600)),((503,400),(531,400))]
        self.tears = []#[((501,600),(501,402))]
        self.spires = [((400,600),(600,400))]
        self.full_horizons = []
        self.full_tears = []
        self.temps = []
        self.temp = 0
        self.dots = False
        self.block_scale = 10
        self.line_cap_x = 3
        self.line_cap_y = 3
        # self.spiralise()
        # self.player.rect.x += self.screen_width//2
    
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
        for line in self.full_horizons:
            pygame.draw.line(self.screen, (190,190,190), line[0], line[1])
        for line in self.full_tears:
            pygame.draw.line(self.screen, (190,190,190), line[0], line[1])
        if self.dots:
            for x in range(0,self.screen_width, self.block_scale):
                for y in range(0,self.screen_height, self.block_scale):
                    pygame.draw.circle(self.screen, (4,100,100), (x,y), 1, 1)
        for line in self.spires:
            pygame.draw.line(self.screen, (110,210,110), line[0], line[1])
        self.linify()
        pygame.display.flip()
    
    def linify(self):
        if self.temp == 0:
            if len(self.temps) == 1:
                pygame.draw.line(self.screen, (215,104,157), self.temps[0], (pygame.mouse.get_pos()[0],self.temps[0][1]))
        if self.temp == 1:
            if len(self.temps) == 1:
                pygame.draw.line(self.screen, (215,104,157), self.temps[0], (self.temps[0][0],pygame.mouse.get_pos()[1]))
    
    def spiralise(self):
        skip = False
        for line in self.spires:
            for y in range(0,self.screen_width):
                for x in range(0,self.screen_height):
                    if dotxline((x,y), line[0], line[1], 0):
                        if skip == False:
                            self.horizons.append(((x,y),(x,y)))
                            skip = True
                        else:
                            skip = False
        print(len(self.horizons))
    
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
                    if self.player.down > 3:
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
                if event.key == pygame.K_l:
                    if self.dots:
                        self.dots = False
                    else:
                        self.dots = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.rechts = False
                if event.key == pygame.K_LEFT:
                    self.player.links = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                phoint = pygame.mouse.get_pos()
                if event.button == 1:
                    if len(self.temps) < 1:
                        self.temps.append([(phoint[0]//self.block_scale)*self.block_scale,(phoint[1]//self.block_scale)*self.block_scale])
                    else:
                        self.temps.append([(pygame.mouse.get_pos()[0]//self.block_scale)*self.block_scale,self.temps[0][1]])
                        self.full_horizons.append((self.temps[0].copy(),self.temps[1].copy()))
                        if self.temps[0][0] < self.temps[1][0]:
                            self.temps[0][0] += self.line_cap_x
                            self.temps[1][0] -= self.line_cap_x
                        else:
                            self.temps[0][0] -= self.line_cap_x
                            self.temps[1][0] += self.line_cap_x
                        self.horizons.append(self.temps.copy())
                        self.temps = []
                    self.temp = 0
                if event.button == 3:
                    if len(self.temps) < 1:
                        self.temps.append([(phoint[0]//self.block_scale)*self.block_scale,(phoint[1]//self.block_scale)*self.block_scale])
                    else:
                        self.temps.append([self.temps[0][0],(pygame.mouse.get_pos()[1]//self.block_scale)*self.block_scale])
                        self.full_tears.append((self.temps[0].copy(),self.temps[1].copy()))
                        if self.temps[0][1] < self.temps[1][1]:
                            self.temps[0][1] += self.line_cap_y
                            self.temps[1][1] -= self.line_cap_y
                        else:
                            self.temps[0][1] -= self.line_cap_y
                            self.temps[1][1] += self.line_cap_y
                        self.tears.append(self.temps.copy())
                        self.temps = []
                    self.temp = 1

class Player(Sprite):
    """Creates a playerish thingummy"""

    def __init__(self, game:Game):
        super().__init__()
        self.game = game
        self.scale = 29
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
        self.diag_times = 0

    def update(self):
        # self.deli()
        self.exos = [self.rect.center]
        self.motions()
        self.deli()
        self.colls()
        self.game.screen.blit(self.image, self.rect)
        # for line in self.lines:
        #     pygame.draw.line(self.game.screen, (200,160,160), line[0], line[1])
        self.times += 1
        self.hori_times += 1
        self.diag_times += 1
    
    def deli(self):
        self.sides = [(self.rect.topleft, self.rect.bottomleft), 
                      (self.rect.topright, self.rect.bottomright)]
        self.caps = [(self.rect.topleft, self.rect.topright), 
                     (self.rect.bottomleft, self.rect.bottomright)]
        self.lines = self.caps + self.sides
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
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y
        self.prev_d = self.down
        self.prev_r = self.right
        hit = False
        for line in self.game.horizons:
            for side in range(len(self.sides)):
                if not hit:
                    # break
                    if horizon(self.sides[side][0], self.sides[side][1], line[0], line[1]):
                        self.cour(line)
                        hit = True
                        break
        hit = False
        for line in self.game.tears:
            for cap in range(len(self.caps)):
                if not hit:
                    # break
                    if horizon(line[0], line[1], self.caps[cap][0], self.caps[cap][1]):
                        self.sacre(line)
                        hit = True
                        break
        hit = False
        for line in self.game.spires:
            for side in range(len(self.lines)):
                # if not hit:
                col = diagonal_colls(line[0], line[1], self.lines[side][0], self.lines[side][1])
                if col:
                    hit = self.monte(col, line, self.lines[side])
                    # hit = True
                    if hit:
                        break
        self.cory = abs(abs(self.rect.y)-abs(self.prev_y))
        self.corx = abs(abs(self.rect.x)-abs(self.prev_x))
        if self.cory >= 2 and self.corx >= 2:
            if self.cory < self.corx:
                self.rect.x = self.prev_x
                self.down = self.prev_d
            elif self.corx < self.cory:
                self.rect.y = self.prev_y
                self.right = self.prev_r

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
            if self.right > 0:
                self.rect.x -= self.right
                self.rect.x += line[0][0] - self.rect.right
            if self.right < 0:
                self.rect.x += self.right
                self.rect.x -= self.rect.left - line[0][0]
                # self.rect.x += 3
            self.deli()
            self.right = 0
    
    def monte(self, point, line, side):
        if self.times > 1:
            if dotxline(point, line[0], line[1]) and dotxline(point, side[0], side[1]):
                downed = False
                if self.diag_times > 4:
                    if self.down >= 0:
                        self.rect.y -= self.rect.bottom - point[1]
                else:    
                    self.rect.y += point[1] - self.rect.top
                    self.rect.y += 3
                    self.diag_times = 0
                    downed = True
                if self.down < 0 and not downed:
                    self.rect.y += point[1] - self.rect.top
                    self.rect.y += 3
                    self.diag_times = 0
                # if downed:
                #     if self.right > 0:
                #         self.rect.x -= self.right
                #         self.rect.x += point[0] - self.rect.right
                #     if self.right < 0:
                #         self.rect.x += self.right
                #         self.rect.x -= self.rect.left - point[0]
                self.deli()
                self.down = 0
                # self.right = 0
                return True
            else:
                return False


game = Game()
if __name__ == "__main__":
    game.run_game()
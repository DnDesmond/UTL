import pygame
pygame.init()
from pygame.sprite import Sprite
import sys
import random
from Colour_Picker import picks as base_picks
from RP import resource_path as rp
import os

#Issue is with adjustant not returning other than 0
os.chdir("alien_invasion/UTL")
def base_picks(point, width, range, inverse_channels=[0,0,0,0,0,0]):
    greens = width//3
    blues = (width//3)*2
    reds1 = 0
    reds2 = width
    x = point[0]
    green = calcs(x, greens, range)
    blue = calcs(x, blues, range)
    if x < width//2:
        red = calcs(x, reds1, range)
    else:
        red = calcs(x, reds2, range)
    if inverse_channels[0]==1:
        red = 255-red
    if inverse_channels[1]==1:
        green = 255-green
    if inverse_channels[2]==1:
        blue = 255-blue
    if inverse_channels[3]==1:
        temp = red
        red = green
        green = temp
    if inverse_channels[4]==1:
        temp = red
        red = blue
        blue = temp
    if inverse_channels[5]==1:
        temp = blue
        blue = green
        green = temp
    return (red,green,blue)

def calcs(x, bar, range=255):
    if x <= bar:
        res = x-(bar-range)
    elif x >= bar:
        res = (bar+range)-x
    mod = res/abs(range+1)
    res = mod*255
    if res > range:
        res = range
    if res < 0:
        res = 1
    return res

def picks(point, width, range):
    return base_picks(point, width, range, inverse_channels=[0,0,0,0,0,0])

class Game:
    """Attempts a game"""

    def __init__(self):
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height
        self.clock = pygame.time.Clock()
        self.char = Snake(self)
        self.ticks = 0
        self.clicks = 0
        self.bite = Snack(self)
        self.eaten = []

    def run_game(self):
        while True:
            self.check_events()
            self.update_screen()
            self.clock.tick(12)
            self.ticks += 1
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP and not self.char.down:
                    self.turn(0)
                if event.key == pygame.K_DOWN and not self.char.up:
                    self.turn(1)
                if event.key == pygame.K_LEFT and not self.char.right:
                    self.turn(2)
                if event.key == pygame.K_RIGHT and not self.char.left:
                    self.turn(3)
                if event.key == pygame.K_l:
                    self.char.lengthen()
        # if self.char.rect.y > self.bite.rect.y and not self.char.down:
        #     self.turn(0)
        # if self.char.rect.y < self.bite.rect.y and not self.char.up:
        #     self.turn(1)
        # if self.char.rect.x > self.bite.rect.x and not self.char.right:
        #     self.turn(2)
        # if self.char.rect.x < self.bite.rect.x and not self.char.left:
        #     self.turn(3)
        # self.clicks += 1
        # if self.clicks > 20:
        #     if self.char.up or self.char.down:
        #         self.turn(3)
        #     else:
        #         self.turn(0)
    
    def turn(self, ind):
        for cat in range(0,4):
            setattr(self.char, self.char.moves[cat], cat==ind)
        self.clicks = 0

    def update_screen(self):
        # self.screen.fill((self.cols[(self.ticks%len(self.cols))]))
        # self.screen.fill((23,99,127))
        self.screen.fill((102,102,102))
        # try:
        #     self.char.reimage(picks(self.char.rect.topleft, self.screen_width, self.char.tail*10))
        # except ValueError:
        #     print(picks(self.char.rect.topleft, self.screen_width))
        self.char.update()
        self.bite.update()
        pygame.draw.line(self.screen,(0,0,0),(620,360),self.char.rect.center,1)
        pygame.display.flip()
    
class Snake(Sprite):
    """Creates a snake"""

    def __init__(self, game):
        super().__init__()
        self.game:Game = game
        self.scale = 20
        self.width = self.scale
        self.height = self.scale
        self.image = pygame.image.load(rp("Skull.png"))
        self.image.set_colorkey((0,0,0))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.tail_0 = self.rect.copy()
        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.moves = ["up", "down", "left", "right"]
        self.tail = 1
        self.tails: list[pygame.rect.Rect] = [self.tail_0]
        self.fools = [(self.rect.x, self.rect.y)]
        # self.image.set_palette((0,0,0))
        self.image = pygame.PixelArray(self.image)
        # self.image.replace((4,4,4),(102,102,102))
        self.image = self.image.make_surface()
        # self.image.fill((0,0,0))
        self.images = []
        self.breakdown()
        self.og_images = []
        for image in self.images:
            self.og_images.append(image.copy())
        self.temps = self.og_images.copy()
        self.cur = (4,4,4)
        self.og_images.append(self.image)
    
    def update(self):
        self.motion()
        # self.game.screen.blit(self.image, self.rect)
        self.skull()
        for point in self.fools[1:]:
            # self.game.screen.blit(self.image, point)
            # try:
                # self.reimage(picks(point, self.game.screen_width, self.tail*10))
                temp = self.temps.copy()[self.adjutant(point)].copy()
                temp = self.recolour(temp, (4,4,4), picks(point, self.game.screen_width, self.tail*10))
                self.game.screen.blit(temp, point)
            # except TypeError:
            #     pass
        self.rattle()
        # for point in self.fools:
        #     self.game.screen.blit(self.image, point)
        # for tail in self.tails:
        #     self.game.screen.blit(self.image, tail)
    
    def recolour(self, surface, colour, new):
        surface = pygame.PixelArray(surface)
        surface.replace((colour),(new))
        surface = surface.make_surface()
        surface.set_colorkey((0,0,0))
        return surface

    def reimage(self, colour):
        self.images = []
        for image in self.og_images.copy():
            new = self.recolour(image, self.cur, colour)
            new.set_colorkey((0,0,0))
            self.images.append(new)
        self.cur = colour

    def adjutant(self, point):
        self.fools.append(self.rect.topleft)
        point_1 = self.fools[self.fools.index(point)-1]
        point_2 = self.fools[self.fools.index(point)+1]
        sector = [point_1, point_2]
        if self.fools.index(point) == -1:
            sector.append(self.rect.topleft)
        self.fools.pop()
        x,y = point[0],point[1]
        added = 0
        if point in self.game.eaten:
            added = 9
        if (x+self.scale, y) in sector and (x, y+self.scale) in sector:
            return 0+added
        elif (x+self.scale, y) in sector and (x-self.scale, y) in sector:
            return 1+added
        elif (x-self.scale, y) in sector and (x, y+self.scale) in sector:
            return 2+added
        elif (x, y+self.scale) in sector and (x, y-self.scale) in sector:
            return 3+added
        elif (x+self.scale, y) in sector and (x, y-self.scale) in sector:
            return 6+added
        elif (x-self.scale, y) in sector and (x, y-self.scale) in sector:
            return 8+added
        return 1
    
    def rattle(self):
        point = self.fools[0]
        x,y = point[0], point[1]
        poin2 = self.fools[1]
        temp = self.image
        if point in self.game.eaten:
            self.game.eaten.remove(point)
        if (x,y-self.scale) == poin2:
            temp = self.images[4]
        elif (x+self.scale,y) == poin2:
            temp = pygame.transform.rotate(self.images[4],270)
        elif (x,y+self.scale) == poin2:
            temp = pygame.transform.rotate(self.images[4],180)
        elif (x-self.scale,y) == poin2:
            temp = pygame.transform.rotate(self.images[4],90)
        self.game.screen.blit(temp, self.fools[0])

    def skull(self):
        point = self.rect.topleft
        x,y = point[0], point[1]
        poin2 = self.fools[-1]
        if (x,y-self.scale) == poin2:
            self.game.screen.blit(pygame.transform.rotate(self.image,180), self.rect)
        elif (x+self.scale,y) == poin2:
            self.game.screen.blit(pygame.transform.rotate(self.image,90), self.rect)
        elif (x,y+self.scale) == poin2:
            self.game.screen.blit(pygame.transform.rotate(self.image,0), self.rect)
        elif (x-self.scale,y) == poin2:
            self.game.screen.blit(pygame.transform.rotate(self.image,270), self.rect)

    def breakdown(self):
        image = pygame.image.load(rp("Tails.png"))
        for fish in range(0,6):
            for cat in range(0,3):
                imager = pygame.surface.Surface((20,20))
                imager.blit(image,(-cat*20,-fish*20))
                imager = pygame.transform.scale(imager, (self.scale,self.scale))
                imager.set_colorkey((0,0,0))
                self.images.append(imager.copy())

    def lengthen(self):
        # setattr(self, f"tail_{self.tail+1}", getattr(self, f"tail_{self.tail}").copy())
        # self.tails.append(getattr(self, f"tail_{self.tail}"))
        # self.fools.append((self.rect.x, self.rect.y))
        self.fools.reverse()
        self.fools.append(self.fools[0])
        self.fools.reverse()
        self.tail += 1
    
    def trace(self):
        while len(self.fools)>self.tail:
            self.fools.remove(self.fools[0])
        self.fools.append((self.rect.x, self.rect.y))
        # self.fools = []
        # for rect in self.tails:
        #     self.fools.append((rect.x, rect.y))

    def trail(self):
        # self.tails: list[pygame.rect.Rect] = []
        # for tail in range(self.tail, -1, -1):
        #     if tail == 0:
        #         setattr(self, f"tail{tail}", self.rect.copy())
        #         self.tails.append(getattr(self, f"tail{tail}"))
        #     elif tail != 0:
        #         setattr(self, f"tail{tail}", getattr(self, f"tail{tail-1}").copy())
        #         self.tails.append(getattr(self, f"tail{tail}"))
        # self.trace()
        self.trace()


    def motion(self):
        if self.game.ticks % 1 == 0:
            self.trail()
            if self.up:
                self.rect.y -= self.scale
            elif self.down:
                self.rect.y += self.scale
            elif self.left:
                self.rect.x -= self.scale
            elif self.right:
                self.rect.x += self.scale
        if (self.rect.x,self.rect.y) in self.fools[:-2]:
            self.tail = len(self.fools[self.fools.index((self.rect.topleft)):])
            # self.tail = 0
        # self.lengthen()

class Snack(Sprite):
    """Creates refreshments"""

    def __init__(self, game):
        super().__init__()
        self.game: Game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height
        self.image = pygame.image.load(rp("Rot.png"))
        self.image = pygame.transform.scale(self.image, (self.game.char.scale,self.game.char.scale))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(0, self.game.screen_width//self.game.char.scale)*self.game.char.scale, random.randint(0, self.game.screen_height//self.game.char.scale)*self.game.char.scale
    
    def update(self):
        self.relocate()
        self.image.fill(picks(self.rect.topleft, 1680, self.game.char.tail*10))
        self.screen.blit(self.image, self.rect)
    
    def relocate(self):
        if self.rect.colliderect(self.game.char.rect):
            self.game.eaten.append((self.rect.x, self.rect.y))
            self.rect.x, self.rect.y = random.randint(0, self.screen_width//self.game.char.scale-1)*self.game.char.scale, random.randint(0, self.screen_height//self.game.char.scale-1)*self.game.char.scale
            self.game.char.lengthen()


game = Game()
game.run_game()
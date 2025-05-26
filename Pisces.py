import pygame # type: ignore
from pygame.sprite import Sprite # type: ignore
pygame.init()
import sys
import random
import time
import math
from matplotlib import pyplot

class Game:
    """Such and Such"""

    def __init__(self):
        """Initialises all"""
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height
        self.char = Char(self, 500, 500)
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load("Schwarz.png")
        self.image.fill((102,102,102))
        self.image = pygame.transform.scale(self.image, (self.screen_width,self.screen_height))
        self.trail_op = 100
        self.times:list[int] = []
        self.bite = Bite(self)
        self.ticks = 0

    def run_game(self):
        while True:
            self.update_screen()
            self.clock.tick(60)
    
    def update_screen(self):
        if self.ticks%5 == 0:
            self.blit_alpha(self.screen, self.image, (0,0), abs(self.trail_op))
        self.char.update()
        self.bite.update()
        self.check_events()
        pygame.display.flip()
        self.ticks += 1
    
    
    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    self.turn(0)
                if event.key == pygame.K_DOWN:
                    self.turn(1)
                if event.key == pygame.K_LEFT:
                    self.turn(2)
                if event.key == pygame.K_RIGHT:
                    self.turn(3)
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_UP:
            #         self.char.up = False
            #     if event.key == pygame.K_DOWN:
            #         self.char.down = False
            #     if event.key == pygame.K_LEFT:
            #         self.char.left = False
            #     if event.key == pygame.K_RIGHT:
            #         self.char.right = False
        # self.char.left, self.char.right, self.char.up, self.char.down = False, False, False, False
        # if self.char.rect.x > self.bite.rect.x:
        #     self.char.left = True
        # if self.char.rect.x < self.bite.rect.x:
        #     self.char.right = True
        # if self.char.rect.y > self.bite.rect.y:
        #     self.char.up = True
        # if self.char.rect.y < self.bite.rect.y:
        #     self.char.down = True
    
    def modulate(self):
        print(self.times)
        for cat in range(0,20):
            av = sum(self.times)/len(self.times)
            dir = self.difs()
            self.times.append(av+dir)
        pyplot.plot(range(len(self.times)), self.times)
        pyplot.show()
        sys.exit()
    
    def turn(self, ind):
        for cat in range(0,4):
            setattr(self.char, self.char.moves[cat], cat==ind)
    
    def difs(self):
        difs = []
        for num in range(1,len(self.times)):
            difs.append(self.times[num]/self.times[num-1])
        deviation = sum(difs)/len(difs)
        return deviation

class Char(Sprite):
    """Attempts a character."""

    def __init__(self, game, x, y):
        super().__init__()
        self.game:Game = game
        self.screen = self.game.screen
        self.screen_rect = self.game.screen_rect
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height
        self.width = 20
        self.height = 20
        self.x = x
        self.y = y
        self.image = pygame.image.load("Rot.png")
        self.image.fill((0,0,0))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.rect = self.image.get_rect()
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.moves = ["up", "down", "left", "right"]
        self.speed = 20
        self.time_col = 1
        self.colours = []
        self.pos = (0,0)
        for cat in range(0,255):
            self.colours.append((cat, 0, cat))
        for cat in range(254,-1, -1):
            self.colours.append((cat, 0, cat))
        
    def update(self):
        if self.game.ticks%5 == 0:
            self.motion()
        self.colour_check()
        self.screen.blit(self.image, self.rect)
    
    def colour_check(self):
        # if (self.rect.x, self.rect.y) != self.pos:
            # self.image.fill(self.colours[self.time_col%len(self.colours)])
        self.pos = (self.rect.x, self.rect.y)
        self.time_col+=1
    
    def motion(self):
        self.motion_calc()
        self.rect.x += self.x
        self.rect.y += self.y
        self.x, self.y = 0, 0
        if self.rect.bottom < 0:
            self.rect.y = self.screen_height
        elif self.rect.y > self.screen_height:
            self.rect.y = 0-self.height
        if self.rect.right < 0:
            self.rect.x = self.screen_width
        elif self.rect.x > self.screen_width:
            self.rect.x = 0-self.width

    def motion_calc(self):
        if self.up:
            self.y -= self.speed
        elif self.down:
            self.y += self.speed
        elif self.left:
            self.x -= self.speed
        elif self.right:
            self.x += self.speed

class Bite(Sprite):
    """Attempts a snack"""

    def __init__(self, game:Game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.screen_rect = self.game.screen_rect
        self.width = 10
        self.height = 10
        self.image = pygame.image.load("Rot.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = random.randint(0, self.screen_rect.width), random.randint(0, self.screen_rect.height)
        self.time = time.time()
        self.timed = time.time()
        self.stretch = (((self.rect.x-self.game.char.rect.x)**2)+((self.rect.y-self.game.char.rect.y)**2))**(1/2)
    
    def update(self):
        self.collides()
        self.screen.blit(self.image, self.rect)
    
    def collides(self):
        if self.rect.colliderect(self.game.char.rect):
            self.time = time.time()
            self.game.times.append(round(self.stretch/(self.time - self.timed), 4))
            self.timed = self.time
            self.rect.x,self.rect.y = random.randint(0, self.screen_rect.width), random.randint(0, self.screen_rect.height)
            self.game.trail_op -= 5
            self.stretch = (((self.rect.x-self.game.char.rect.x)**2)+((self.rect.y-self.game.char.rect.y)**2))**(1/2)
            # if self.game.trail_op == 0:
            #     pygame.quit()
            #     # self.game.modulate()
            #     sys.exit()
            print("HIT!")

game = Game()

game.run_game()
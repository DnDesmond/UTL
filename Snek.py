import pygame
pygame.init()
from pygame.sprite import Sprite
import sys
import random

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
        self.bite = Snack(self)
        self.cols = []
        for r in range(0,255,10):
            for g in range(0,255,10):
                for b in range(0,255,10):
                    self.cols.append((r,g,b))

    def run_game(self):
        while True:
            self.check_events()
            self.update_screen()
            self.clock.tick(60)
            self.ticks += 1
    
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
                if event.key == pygame.K_l:
                    self.char.lengthen()
    
    def turn(self, ind):
        for cat in range(0,4):
            setattr(self.char, self.char.moves[cat], cat==ind)

    def update_screen(self):
        self.screen.fill((self.cols[(self.ticks%len(self.cols))]))
        self.char.update()
        self.bite.update()
        pygame.display.flip()
    
class Snake(Sprite):
    """Creates a snake"""

    def __init__(self, game):
        super().__init__()
        self.game:Game = game
        self.width = 20
        self.height = 20
        self.image = pygame.image.load("Rot.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.tail_0 = self.rect.copy()
        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.moves = ["up", "down", "left", "right"]
        self.tail = 100
        self.tails: list[pygame.rect.Rect] = [self.tail_0]
        self.fools = [(self.rect.x, self.rect.y)]
    
    def update(self):
        self.motion()
        self.game.screen.blit(self.image, self.rect)
        # for point in self.fools:
        #     self.game.screen.blit(self.image, point)
        # for tail in self.tails:
        #     self.game.screen.blit(self.image, tail)

    
    def lengthen(self):
        # setattr(self, f"tail_{self.tail+1}", getattr(self, f"tail_{self.tail}").copy())
        # self.tails.append(getattr(self, f"tail_{self.tail}"))
        self.fools.append((self.rect.x, self.rect.y))
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
        for point in self.fools:
            self.game.screen.blit(self.image, point)


    def motion(self):
        if self.game.ticks % 5 == 0:
            self.trail()
            if self.up:
                self.rect.y -= 20
            elif self.down:
                self.rect.y += 20
            elif self.left:
                self.rect.x -= 20
            elif self.right:
                self.rect.x += 20
        if (self.rect.x,self.rect.y) in self.fools[:-2]:
            self.tail = len(self.fools[self.fools.index((self.rect.topleft)):])
            # self.tail = 0

class Snack(Sprite):
    """Creates refreshments"""

    def __init__(self, game):
        super().__init__()
        self.game: Game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height
        self.image = pygame.image.load("Rot.png")
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(0, self.game.screen_width//20)*20, random.randint(0, self.game.screen_height//20)*20
    
    def update(self):
        self.relocate()
        self.screen.blit(self.image, self.rect)
    
    def relocate(self):
        if self.rect.colliderect(self.game.char.rect):
            self.rect.x, self.rect.y = random.randint(0, self.screen_width//20-1)*20, random.randint(0, self.screen_height//20-1)*20
            self.game.char.lengthen()


game = Game()
game.run_game()
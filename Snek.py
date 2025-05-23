import pygame
pygame.init()
from pygame.sprite import Sprite
import sys
import random
from Colour_Picker import picks

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
        # self.cols = []
        # for r in range(0,255,10):
        #     for g in range(0,255,10):
        #         for b in range(0,255,10):
        #             self.cols.append((r,g,b))

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
                    # self.char.reimage((200,200,200))
    
    def turn(self, ind):
        for cat in range(0,4):
            setattr(self.char, self.char.moves[cat], cat==ind)

    def update_screen(self):
        # self.screen.fill((self.cols[(self.ticks%len(self.cols))]))
        # self.screen.fill((23,99,127))
        self.screen.fill((102,102,102))
        try:
            self.char.reimage(picks(self.char.rect.topleft, self.screen_width, self.char.tail*10))
        except ValueError:
            print(picks(self.char.rect.topleft, self.screen_width))
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
        self.image = pygame.image.load("Skull.png")
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
        self.cur = (4,4,4)
    
    def update(self):
        self.motion()
        # self.game.screen.blit(self.image, self.rect)
        self.skull()
        for point in self.fools[1:]:
            # self.game.screen.blit(self.image, point)
            try:
                self.game.screen.blit(self.images[self.adjutant(point)], point)
            except TypeError:
                pass
        self.rattle()
        # for point in self.fools:
        #     self.game.screen.blit(self.image, point)
        # for tail in self.tails:
        #     self.game.screen.blit(self.image, tail)
    
    def recolour(self, surface, colour, new):
        surface = pygame.PixelArray(surface)
        surface.replace((colour),(new))
        surface = surface.make_surface()
        return surface

    def reimage(self, colour):
        self.images = []
        self.og_images.append(self.image)
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
        if (x+20, y) in sector and (x, y+20) in sector:
            return 0
        elif (x+20, y) in sector and (x-20, y) in sector:
            return 3
        elif (x-20, y) in sector and (x, y+20) in sector:
            return 6
        elif (x, y+20) in sector and (x, y-20) in sector:
            return 1
        elif (x+20, y) in sector and (x, y-20) in sector:
            return 2 
        elif (x-20, y) in sector and (x, y-20) in sector:
            return 8
    
    def rattle(self):
        point = self.fools[0]
        x,y = point[0], point[1]
        poin2 = self.fools[1]
        if (x,y-20) == poin2:
            self.game.screen.blit(self.images[4], self.fools[0])
        elif (x+20,y) == poin2:
            self.game.screen.blit(pygame.transform.rotate(self.images[4],270), self.fools[0])
        elif (x,y+20) == poin2:
            self.game.screen.blit(pygame.transform.rotate(self.images[4],180), self.fools[0])
        elif (x-20,y) == poin2:
            self.game.screen.blit(pygame.transform.rotate(self.images[4],90), self.fools[0])

    def skull(self):
        point = self.rect.topleft
        x,y = point[0], point[1]
        poin2 = self.fools[-1]
        if (x,y-20) == poin2:
            self.game.screen.blit(pygame.transform.rotate(self.image,180), self.rect)
        elif (x+20,y) == poin2:
            self.game.screen.blit(pygame.transform.rotate(self.image,90), self.rect)
        elif (x,y+20) == poin2:
            self.game.screen.blit(pygame.transform.rotate(self.image,0), self.rect)
        elif (x-20,y) == poin2:
            self.game.screen.blit(pygame.transform.rotate(self.image,270), self.rect)

    def breakdown(self):
        image = pygame.image.load("Tails.png")
        for cat in range(0,3):
            for fish in range(0,3):
                imager = pygame.surface.Surface((20,20))
                imager.blit(image,(-cat*20,-fish*20))
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
        self.lengthen()

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
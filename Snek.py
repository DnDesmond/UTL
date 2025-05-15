import pygame
pygame.init()
from pygame.sprite import Sprite
import sys

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

    def run_game(self):
        while True:
            self.check_events()
            self.update_screen()
            self.clock.tick(10)
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
    
    def turn(self, ind):
        for cat in range(0,4):
            setattr(self.char, self.char.moves[cat], cat==ind)

    def update_screen(self):
        self.screen.fill((50,200,50))
        self.char.update()
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
        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.moves = ["up", "down", "left", "right"]
    
    def update(self):
        self.motion()
        self.game.screen.blit(self.image, self.rect)
    
    def motion(self):
        if self.game.ticks % 5 == 0:
            if self.up:
                self.rect.y -= 20
            elif self.down:
                self.rect.y += 20
            elif self.left:
                self.rect.x -= 20
            elif self.right:
                self.rect.x += 20

game = Game()
game.run_game()
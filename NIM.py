import pygame
from pygame import *
import sys
import os
import time
os.chdir("C:/Users/isaac/Graphics")
from UnderTheLine import Brick

class Ivan:
    """Attempts to create the main game"""

    def __init__(self):
        """Initialises all base attributes"""
        pygame.init()
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.screen_rect = self.screen.get_rect()

        self.cursor_red = pygame.image.load("Graphics/MarkerRed.png").convert_alpha()
        self.cursor_blue = pygame.image.load("Graphics/MarkerGreen.png").convert_alpha()
        self.cursorect = Brick(self, 1,1)

        self.bricks_1 = pygame.sprite.Group()
        self.bricks_2 = pygame.sprite.Group()
        self.bricks_3 = pygame.sprite.Group()
        self.last_y = 0
        self.x_list = [300, 400, 500, 250, 350, 450, 550, 200, 300, 400, 500, 600]
        self.y_list = [100, 100, 100, 300, 300, 300, 300, 500, 500, 500, 500, 500]
        self.level_list = [1,1,1,2,2,2,2,3,3,3,3,3]
        self.player = 0
        self.can_break = False
        self.times = 0

        self.start_button0 = Brick(self, 64, 25)
        self.start_button1 = Brick(self, 64, 25)
        self.start_button0.image = pygame.image.load("Graphics/FoamBrick.png").convert_alpha()
        self.start_button1.image = pygame.image.load("Graphics/BlueBrickWide.png").convert_alpha()
        self.start_button0.image = pygame.transform.scale(self.start_button0.image, (64,self.screen_height))
        self.start_button1.image = pygame.transform.scale(self.start_button1.image, (64,self.screen_height))
        self.start_button0.rect = self.start_button0.image.get_rect()
        self.start_button1.rect = self.start_button0.image.get_rect()
        self.start_button1.rect.right = self.screen_rect.right
        for cat in range(0,12):
            brick = Brick(self, 20, 100)
            brick.rect.x = self.x_list[cat]+240
            brick.rect.y = self.y_list[cat]
            getattr(self, f"bricks_{self.level_list[cat]}").add(brick)
        
        self.track_mouse = pygame.mouse.get_pos()
        self.mousing = False
    
    def run_game(self):
        while True:
            self.update_screen()
            self.check_events()
            self.clock.tick(60)
            self.times += 1
            if len(self.bricks_1)+len(self.bricks_2)+len(self.bricks_3) == 0:
                pygame.mouse.set_pos(self.screen_width/2,50)
                for cat in range(0,12):
                    brick = Brick(self, 20, 100)
                    brick.rect.x = self.x_list[cat]+240
                    brick.rect.y = self.y_list[cat]
                    getattr(self, f"bricks_{self.level_list[cat]}").add(brick)
                self.can_break = False

    
    def update_screen(self):
        self.screen.fill((43,76,192))
        for brick in self.bricks_1:
            brick.image.fill((23,23,23))
            brick.update()
        for brick in self.bricks_2:
            brick.image.fill((123,123,123))
            brick.update()
        for brick in self.bricks_3:
            brick.image.fill((223,223,223))
            brick.update()
        self.start_button0.update()
        self.start_button1.update()
        self.cursorise()
        self.track_mouse = pygame.mouse.get_pos()
        pygame.display.flip()
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousing = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.mousing = False
            if self.mousing:
                if self.can_break and self.last_y != 0:
                    for brick in self.bricks_1:
                        if brick.rect.collidepoint(pygame.mouse.get_pos()) and brick.rect.y == self.last_y:
                            brick.kill()
                            self.last_y = brick.rect.y
                    for brick in self.bricks_2:
                        if brick.rect.collidepoint(pygame.mouse.get_pos()) and brick.rect.y == self.last_y:
                            brick.kill()
                            self.last_y = brick.rect.y
                    for brick in self.bricks_3:
                        if brick.rect.collidepoint(pygame.mouse.get_pos()) and brick.rect.y == self.last_y:
                            brick.kill()
                            self.last_y = brick.rect.y
                elif self.can_break:
                    for brick in self.bricks_1:
                        if brick.rect.collidepoint(pygame.mouse.get_pos()):
                            brick.kill()
                            self.last_y = brick.rect.y
                    for brick in self.bricks_2:
                        if brick.rect.collidepoint(pygame.mouse.get_pos()):
                            brick.kill()
                            self.last_y = brick.rect.y
                    for brick in self.bricks_3:
                        if brick.rect.collidepoint(pygame.mouse.get_pos()):
                            brick.kill()
                            self.last_y = brick.rect.y
                if self.start_button0.rect.collidepoint(pygame.mouse.get_pos()):
                    self.can_break = True
                    if self.player != 0:
                        self.last_y = 0
                        self.player = 0
                elif self.start_button1.rect.collidepoint(pygame.mouse.get_pos()):
                    self.can_break = True
                    if self.player != 1:
                        self.last_y = 0
                        self.player = 1
    
    def timer(self):
        if self.times%600 == 0:
            self.can_break = False
    
    def cursorise(self):
        if self.player == 0:
            self.cursor_image = self.cursor_red
        elif self.player == 1:
            self.cursor_image = self.cursor_blue
        self.cursorect.rect.x = pygame.mouse.get_pos()[0]
        self.cursorect.rect.y = pygame.mouse.get_pos()[1]-28
        self.screen.blit(self.cursor_image, self.cursorect.rect)



thang = Ivan()
thang.run_game()

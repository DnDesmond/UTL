import pygame
from pygame.sprite import Group, Sprite
import sys
import os
import random
import time
import ctypes
import csv
import pickle
from Full_Run import premiere
ctypes.windll.shcore.SetProcessDpiAwareness(0)
import pyautogui
pyautogui.PAUSE = 0
game_scale = 2
from RP import resource_path as r
import json
  
from Breakers import *
if __name__ == "__main__":
    from Brick_coordinates import *

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

class Bouncing:
    """Attempts to make one of those bouncing square in a square things."""

    def __init__(self):
        """Initialise what needs it"""
        pygame.joystick.init()
        self.clock = pygame.time.Clock()

        self.screen = screen
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Bouncing Gimmick")
        self.kinds()

        # Does joystick related happenings
        self.joystick = False
        self.joysticks = []
        if pygame.joystick.get_count() > 0:
            for joy in range(pygame.joystick.get_count()):
                self.joysticks.append(pygame.joystick.Joystick(joy))
            for joystick in self.joysticks:
                joystick.init()
                self.joystick = joystick
        if self.joystick:
            print(self.joystick.get_numbuttons())
            self.button_count = self.joystick.get_numbuttons()
            if self.button_count == 16:
                self.left_pressed = self.joystick.get_button(9)
                self.right_pressed = self.joystick.get_button(10)
                self.option_pressed = True
            elif self.button_count == 11:
                self.left_pressed = self.joystick.get_button(4)
                self.right_pressed = self.joystick.get_button(5)
                self.option_pressed = True

        self.buttonise()    
        self.timer = 0
        self.shielded = 10000
        self.shined = 10000
        self.sped_up = 15000
        self.bordereded = 0
        self.bardereded = 0
        self.left_bricks = 0
        self.extras = 0
        self.opaque = 0
        self.unopaque = 0
        self.trail_length = 50
        self.trail_gap = 4
        self.trail_view = 2
        self.trail_view_base = 2
        self.trail_ether = 0
        self.ball_sprite_index = 0
        self.trail_ways = []
        self.spins = True
        self.main_spins = True
        self.brick_height = 25
        self.brick_width = 64
        self.brick_list = []
        self.frame_rate = 85
        self.Dict1 = Level1()
        self.Dict2 = Level2()
        self.Dict3 = Level3()
        self.Dict4 = Level4()
        self.Dict5 = Level5()
        self.spec1 = Spec1()
        self.spec2 = Spec2()
        self.spec3 = Spec3()
        self.spec4 = Spec4()
        self.spec5 = Spec5()
        self.dev_level1 = self.Dict1.dict
        self.rightbreaker = RightBreaker(self)
        self.farrightbreaker = FarRightBreaker(self)
        self.leftbreaker = LeftBreaker(self)
        self.farleftbreaker = FarLeftBreaker(self)
        self.middlebreaker = MiddleBreaker(self)
        self.in_game = Yarn(self)
        self.bricks = pygame.sprite.Group()
        self.brickes = pygame.sprite.Group()
        self.hard_bricks = pygame.sprite.Group()
        self.spherage = pygame.sprite.Group()
        self.shrapnel = pygame.sprite.Group()
        self.lockaged = pygame.sprite.Group()
        self.can_update = pygame.sprite.Group()
        self.can_upadte = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.dev_bricks = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.backgrund_image = pygame.image.load(r("Shield.png")).convert_alpha()
        self.background_image = pygame.image.load(r("MappedCompassBack.png")).convert_alpha()
        self.overlay_image = pygame.image.load(r("Screenshot (11).png")).convert_alpha()
        self.dev_list = open(r("Brick_coordinates.py"), 'a')
        try:
            self.start_read = open("Start_clause.txt.txt", 'r')
            self.easy_start = self.start_read.readline(-1)
        except FileNotFoundError:
            self.start_read = open("Start_clause.txt.txt", 'w')
            self.easy_start = False
        self.started = False
        self.inner = True
        self.alter = False
        self.lalter = False
        self.new_began = False
        self.paused = False
        self.swift = True
        self.rumbles = False
        self.dev = False
        self.start_read.close()
        self.imige = pygame.image.load(r("See_Through_Wide.png"))
        self.track_mouse = False
        self.track_mouse_pos = pygame.mouse.get_pos()
        self.left_mouse = False
        self.right_mouse = False
        self.overlay = False
        self.next = False
        self.star = False
        self.dos = False
        self.tres = False
        self.cuatro = False
        self.cinco = False

        # Gradient initialisations
        self.grad_up = False
        if self.grad_up:
            self.grad = 1
            self.base_grad = 1
        else:
            self.grad = 180
            self.base_grad = 180
        
        self.lives_left = 10
        self.lives()
        self.spring_ball()
        self.moving_left = False
        self.moving_right = False
        self.create_wall()
        self.controller_buttons = {
            "x":0,
            "circle":1,
            "square":2,
            "triangle":3,
            "share":4,
            "PS":5,
            "options":6,
            "left_stick_click":7,
            "right_stick_click":8,
            "L1":9,
            "R1":10,
            "up_arrow":11,
            "down_arrow":12,
            "left_arrow":13,
            "right_arrow":14,
            "touchpad":15
        }
    
    def buttonise(self):
        self.button_list = []
        self.button_pause = Button(self, 764, 63, 53, 370, "ButtonContinue")
        self.button_option = Button(self, 764, 63, 53, 370+63, "ButtonOption")
        self.button_list.append(self.button_pause)
        self.button_list.append(self.button_option)
    
    def kinds(self):
        """Makes the lists for the types of specialised bricks."""
        self.prof = []
        self.ki('cant_update')
        self.ki('cant_upadte')
        self.ki("undamaged")
        self.ki('plus')
        self.ki('bomb')
        self.ki('doppelbomb')
        self.ki('locked')
        self.ki('launched')
        self.ki('keys')
        self.ki('unbreakable')
        self.ki('new_begin')
        self.ki('sealing')
        self.ki('lotus')
        self.ki('shiny')
        self.ki('cardinal')
        self.ki('will_expand')
        self.ki('expand')
        self.ki('expand1')
        self.ki('expand2')
        self.ki('expand3')
        self.ki('expand4')
        self.ki('expand5')
        self.ki('barrier')
        self.ki("acidic")
        self.ki("accelerate")
        self.ki("trails")
        self.ki("unlocked")
        self.ki("vermillion")
        self.ki("phthalo")
        self.ki("sapphire")
        self.ki("royal")
        self.ki("vermillionlock")
        self.ki("phthalolock")
        self.ki("sapphirelock")
        self.ki("royallock")
        self.ki("adoored")
    
    def ki(self, ci):
        self.prof.append((setattr(self, ci, [])))

    def run_game(self):
        """Learn to read"""
        while True:
            if self.paused == False:
                self.update_screen()
            else:
                self.pause_screen()
            self.check_events()
            self.timer += 1
            self.shielded += 10
            self.shined += 1
            self.sped_up += 1
            if self.sped_up < 1500:
                self.clock.tick((self.frame_rate*2)-20)
            else:
                self.clock.tick(self.frame_rate)
            if self.next:
                self.in_game.real_init()
                break
    
    def update_screen(self):
        """Runs all screen base updates."""
        self.screen.fill((38, 142, 202))
        if self.shielded < 10000:
            self.screen.blit(self.backgrund_image, (0, self.middlebreaker.rect.y + 10))
        #self.screen.blit(self.background_image, (0,0))
        for sphere in self.spherage:
            sphere.update()
        for spere in self.livess:
            spere.update(999)
        for stare in self.stars:
            stare.update()
        for war_crime in self.shrapnel:
            war_crime.update()
        if self.joystick and self.rumbles:
            if self.timer%50 != 0: 
                for joystick in self.joysticks:
                    joystick.rumble(100,150,0)
            else:
                for joystick in self.joysticks:
                    joystick.stop_rumble()
        self.rightbreaker.update()
        self.farrightbreaker.update()
        self.leftbreaker.update()
        self.farleftbreaker.update()
        self.middlebreaker.update()
        #for brikage in self.brickes:
        #    brikage.update()
        if self.overlay:
            self.blit_alpha(self.screen, self.overlay_image, (0,0), 128)
        if not self.inner:
            for brick in self.brickes:
                brick.update()
        if self.dev:
            for brickage in self.dev_bricks:
                brickage.update()
        else:
            for brickage in self.bricks:
                brickage.update()
        if self.new_began:
            self.resets()
        self.levels()
        if self.left_bricks > len(self.bricks) or self.timer % 50 == 0:
            self.borders()
            self.borderes()
        if self.timer % self.trail_gap == 0:
            self.trail()
        for count in range(self.trail_length,0, -1):
            if len(self.trails)>self.trail_length:
                self.opaque = (self.trail_length-count)*self.trail_view
                self.unopaque = (count)*self.trail_view
                self.trail_ways = [self.opaque, self.unopaque]
                dust = self.trails[-count]
                dust.update(self.trail_ways[self.trail_ether])
            else:
                for cat in range(0,self.trail_length):
                    self.trail()
        self.left_bricks = len(self.bricks)
        pygame.display.flip()
    
    def auto(self):
        if self.middlebreaker.rect.centerx < self.mball.x:
            self.moving_right = True
            self.moving_left = False
        elif self.middlebreaker.rect.centerx > self.mball.x:
            self.moving_left = True
            self.moving_right = False
    
    def levels(self):
        if len(self.lockaged) == len(self.bricks) + len(self.brickes):
            for brick in self.bricks:
                brick.kill()
            for brick in self.brickes:
                brick.kill()
            self.dev = False
        if not self.bricks and self.dos == False:
            for cat in range(1,6):
                self.horcrux()
            self.kinds()
            self.create_wall(2)
            self.dos = True
            self.borders()
            self.borderes()
        elif not self.bricks and self.tres == False: 
            for cat in range(1,6):
                self.horcrux()
            self.kinds()
            self.create_wall(3)
            self.tres = True
            self.borders()
            self.borderes()
        elif not self.bricks and self.cuatro == False:
            for cat in range(1,6):
                self.horcrux()
            self.kinds()
            self.brick_width = 32
            self.create_wall(4)
            self.brick_width = 64
            self.cuatro = True
            self.borders()
            self.borderes()
        elif not self.bricks and self.cinco == False:
            for cat in range(1,6):
                self.horcrux()
            self.kinds()
            self.create_wall(5)
            self.cinco = True
            self.borders()
            self.borderes()
    
    def pause_screen(self):
        """Creates the pause screen."""
        self.screen.fill((38, 142, 102))
        is_not_scaled = (self.screen_width, self.screen_height)
        self.pause_background_image = pygame.image.load(r("Backgrounf.png")).convert_alpha()
        self.pause_background_image = pygame.transform.scale(self.pause_background_image, is_not_scaled)
        self.screen.blit(self.pause_background_image, (0,0))
        self.background_rect = self.pause_background_image.get_rect()
        for button in self.button_list:
            self.buttons.add(button)
        for button in self.buttons:
            button.update()
        #self.blit_alpha(self.screen, self.pause_background_image, (0, 0), 128)
        # self.screen.blit(self.pause_background_image, (0,0))
        pygame.display.flip()

    def check_events(self):
        """Check keyboard events."""
        try:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:# or event.key == pygame.K_ESCAPE:
                        if self.alter == True:
                            pygame.quit()
                            nombre = 0
                            self.dev_list.write("\nclass Spec4:\n\tdef __init__(self):\n\t\tself.dict = {\n")
                            for shade in self.dev_bricks:
                                self.dev_list.write(f"\t\t\t{nombre}:({shade.rect.x},{shade.rect.y}),\n")
                                nombre += 1
                            self.dev_list.write("\t\t}")
                            self.dev_list.close()
                            sys.exit()
                        else:
                            pygame.quit()
                            sys.exit()
                    elif event.key == pygame.K_ESCAPE:
                        if self.paused == True:
                            self.paused = False
                            self.buttons = pygame.sprite.Group()
                        else:
                            self.paused = True
                    elif event.key == pygame.K_p and self.started == False:
                        for sphere in self.spherage:
                            sphere.moving_right = True
                            #sphere.fmoving_right = True
                            sphere.moving_up = True
                            self.started = True
                            for cat in range(self.extras):
                                self.spring_ball()
                    elif event.key == pygame.K_LEFT:
                        self.moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = True
                    elif event.key == pygame.K_s:
                        self.star_up()
                    elif event.key == pygame.K_k:
                        for brick in self.bricks:
                            if brick not in self.lockaged:
                                brick.kill()
                        for brick in self.brickes:
                            brick.kill()
                    elif event.key == pygame.K_c:
                        for ball in self.spherage:
                            ball.y = 25
                    elif event.key == pygame.K_f:
                        for ball in self.spherage:
                            ball.recenters()
                    elif event.key == pygame.K_e:
                        self.mball.spin_inator(self.ball_sprite_index)
                        self.ball_sprite_index += 1
                    elif event.key == pygame.K_RALT:
                        self.alter = True
                    elif event.key == pygame.K_LALT:
                        self.lalter = True
                    elif event.key == pygame.K_a:
                        if self.alter:
                            for brick in self.bricks:
                                brick.kill()
                            for brick in self.brickes:
                                brick.kill()
                            self.grad = self.base_grad
                            self.create_wall(0)
                            self.grad = self.base_grad
                            self.dev = True
                    elif event.key == pygame.K_DOWN and self.shined > 10000:
                        if len(self.stars) > 0:
                            self.shined = 0
                            self.shore = self.stars.sprites()[-1]
                            self.shore.kill()
                        else:
                            pass
                    elif event.key == pygame.K_o:
                        self.overlay = True
                    elif event.key == pygame.K_F4 and self.lalter:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = False
                    elif event.key == pygame.K_RALT:
                        self.alter = False
                    elif event.key == pygame.K_LALT:
                        self.lalter = False
                    elif event.key == pygame.K_o:
                        self.overlay = False
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.joystick.get_button(6) and not self.option_pressed:
                        if not self.paused and not self.option_pressed:
                            self.paused = True
                        elif self.paused and not self.option_pressed:
                            self.paused = False
                        self.option_pressed = True
                if event.type == pygame.JOYBUTTONUP:
                    if not self.joystick.get_button(6) and self.option_pressed:
                        self.option_pressed= False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.track_mouse = True
                    self.track_mouse_pos = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[0]:
                        self.left_mouse = True
                    elif pygame.mouse.get_pressed()[2]:
                        self.right_mouse = True
                if self.track_mouse:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.left_mouse:
                        if not self.paused:
                            for brack in self.bricks:
                                if brack.rect.collidepoint(mouse_pos):
                                    self.dev_bricks.add(brack)
                        else:
                            if self.button_pause.rect.collidepoint(self.track_mouse_pos):
                                self.paused = False
                            elif self.button_option.rect.collidepoint(self.track_mouse_pos):
                                if self.trail_view == self.trail_view_base:
                                    self.trail_view = 0
                                else:
                                    self.trail_view = self.trail_view_base
                    elif self.right_mouse:
                        for brack in self.bricks:
                            if brack.rect.collidepoint(mouse_pos):
                                self.dev_bricks.remove(brack)
                    self.track_mouse_pos = (0,0)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.track_mouse = False
                    if not pygame.mouse.get_pressed()[0]:
                        self.left_mouse = False
                    if not pygame.mouse.get_pressed()[2]:
                        self.right_mouse = False
        except SystemError:
            pass
        if self.joystick:
            if self.joystick.get_numbuttons() == 16:
                if self.joystick.get_button(9):
                    self.moving_left = True
                elif self.joystick.get_button(9) != self.left_pressed:
                    self.moving_left = False
                if self.joystick.get_button(10):
                    self.moving_right = True
                elif self.joystick.get_button(10) != self.right_pressed:
                    self.moving_right = False
                if self.joystick.get_button(3) and self.shined > 10000:
                    if len(self.stars) > 0:
                        self.shined = 0
                        self.shore = self.stars.sprites()[-1]
                        self.shore.kill()
                    else:
                        pass
                if self.joystick.get_button(2) and self.started == False:
                    for sphere in self.spherage:
                        sphere.moving_right = True
                        #sphere.fmoving_right = True
                        sphere.moving_up = True
                        self.started = True
                        for cat in range(self.extras):
                            self.spring_ball()
                self.left_pressed = self.joystick.get_button(9)
                self.right_pressed = self.joystick.get_button(10)
                self.option_pressed = self.joystick.get_button(6)
            if self.joystick.get_numbuttons() == 11:
                if self.joystick.get_button(4):
                    self.moving_left = True
                elif self.joystick.get_button(4) != self.left_pressed:
                    self.moving_left = False
                if self.joystick.get_button(5):
                    self.moving_right = True
                elif self.joystick.get_button(5) != self.right_pressed:
                    self.moving_right = False
                if self.joystick.get_button(3) and self.shined > 10000:
                    if len(self.stars) > 0:
                        self.shined = 0
                        self.shore = self.stars.sprites()[-1]
                        self.shore.kill()
                    else:
                        pass
                if self.joystick.get_button(2) and self.started == False:
                    for sphere in self.spherage:
                        sphere.moving_right = True
                        #sphere.fmoving_right = True
                        sphere.moving_up = True
                        self.started = True
                        for cat in range(self.extras):
                            self.spring_ball()
                self.left_pressed = self.joystick.get_button(4)
                self.right_pressed = self.joystick.get_button(5)
        


    def draw_box(self):
        """Draws the larger box for the square to be in."""
        pass

    def create_wall(self, level=1):
        print(self.screen_width)
        print(self.screen_height)
        """Makes the wall for the ball to break."""
        self.brick_dict = {}
        self.bricke_dict = {}
        self.bordereded = 0
        self.current_y = 100
        self.current_x = 0
        self.reinforce = 0
        self.shined = 10000
        if level > 0:
            self.grad = self.base_grad
        for brick in self.bricks:
            brick.kill()
        for brick in self.brickes:
            brick.kill()
        while self.current_y < 301:
            while self.current_x < self.screen_width:
                if level == 0:
                    self.display(self.current_x, self.current_y, self.brick_width, self.brick_height, self.bricks)
                    self.display(self.current_x, self.current_y+3, self.brick_width, self.brick_height-5, self.brickes, inner=self.inner)
                    self.current_y = 300
                    self.current_x = self.screen_width
                elif level == 1:
                    self.gen_level(self.current_x, self.current_y, self.brick_width, self.brick_height, self.bricks,level, False, "Blue")
                    self.gen_level(self.current_x, self.current_y+3, self.brick_width, self.brick_height-5, self.brickes,level, inner=self.inner, grad="Blue")
                    self.current_y = 300
                    self.current_x = self.screen_width
                else:
                    self.gen_level(self.current_x, self.current_y, self.brick_width, self.brick_height, self.bricks,level, False)
                    self.gen_level(self.current_x, self.current_y+3, self.brick_width, self.brick_height-5, self.brickes,level, inner=self.inner)
                    self.current_y = 300
                    self.current_x = self.screen_width
                self.current_x += self.brick_width
            self.current_x = 0
            self.current_y += self.brick_height
            self.reinforce += 1
    
    def borders(self): 
        """So think france"""
        self.bordered = 0
        self.cant_update.clear()
        self.can_update = pygame.sprite.Group()
        for key, value in self.brick_dict.items():
            temp = [value[0] + self.brick_width, value[1]]
            temps = [value[0] - self.brick_width, value[1]]
            tem = [value[0], value[1] + self.brick_height]
            tmp = [value[0], value[1] - self.brick_height]
            if temp in self.brick_dict.values() and temps in self.brick_dict.values() and tem in self.brick_dict.values() and tmp in self.brick_dict.values():
                self.bordered += 1
                self.cant_update.append(key)
        for brick in self.bricks:
            if self.swift:
                if brick not in self.cant_update:
                    self.can_update.add(brick)
            else:
                if True:
                    self.can_update.add(brick)
        if self.bordered < self.bordereded:
            # print(self.bordered)
            pass
        self.bordereded = self.bordered

    def borderes(self):
        """So think france"""
        self.bardered = 0
        self.cant_upadte.clear()
        self.can_upadte = pygame.sprite.Group()
        for key, value in self.bricke_dict.items():
            temp = [value[0] + self.brick_width, value[1]]
            temps = [value[0] - self.brick_width, value[1]]
            tem = [value[0], value[1] + self.brick_height]
            tmp = [value[0], value[1] - self.brick_height]
            if temp in self.bricke_dict.values() and temps in self.bricke_dict.values() and tem in self.bricke_dict.values() and tmp in self.bricke_dict.values():
                self.bardered += 1
                self.cant_upadte.append(key)
        for brick in self.brickes:
            if self.swift:
                if brick not in self.cant_upadte:
                    self.can_upadte.add(brick)
            else:
                if True:
                    self.can_upadte.add(brick)
        if self.bardered < self.bardereded:
            # print(self.bardered)
            pass
        self.bardereded = self.bardered
    
    def display(self, x_position, y_position, width, height, holder, inner=False):
        """Creates the admin display."""
        self.star = False
        if height >= self.brick_height:
            y_position = 0
        else:
            y_position = 3
        self.grad = self.base_grad
        x_position = 0
        while y_position < self.screen_height:
            while x_position < self.screen_width:
                new_brick = self.brick_base(width, height, inner, x_position, y_position)
                if self.grad == 0:
                    new_brick.reinforce()
                elif self.grad == 1:
                    new_brick.damage()
                elif self.grad == 2:
                    new_brick.gunpowder()
                elif self.grad == 3:
                    new_brick.doppelgunpowder()
                elif self.grad == 4:
                    new_brick.lock()
                elif self.grad == 5:
                    new_brick.key()
                elif self.grad == 6:
                    new_brick.open()
                elif self.grad == 7:
                    new_brick.unbreak()
                elif self.grad == 8:
                    new_brick.redo()
                elif self.grad == 9:
                    new_brick.star()
                elif self.grad == 10:
                    new_brick.reinforce()
                elif self.grad == 11:
                    new_brick.homicide()
                elif self.grad == 12:
                    new_brick.bar_expand()
                elif self.grad == 13:
                    new_brick.bar_damage1()
                elif self.grad == 14:
                    new_brick.bar_damage2()
                elif self.grad == 15:
                    new_brick.bar_damage3()
                elif self.grad == 16:
                    new_brick.bar_damage4()
                elif self.grad == 17:
                    new_brick.mystiry()
                elif self.grad == 18:
                    new_brick.ceiling()
                elif self.grad == 19:
                    new_brick.compass()
                elif self.grad == 20:
                    new_brick.up_outer()
                elif self.grad == 21:
                    new_brick.right_outer()
                elif self.grad == 22:
                    new_brick.down_outer()
                elif self.grad == 23:
                    new_brick.left_outer()
                elif self.grad == 24:
                    new_brick.acid()
                elif self.grad == 25:
                    new_brick.shield()
                elif self.grad == 26:
                    new_brick.paint_stripe()
                new_brick.gradient("red", int(self.grad))
                if self.grad_up:
                    if self.grad <= 180:
                        self.grad += 1
                else:
                    if self.grad > 1:
                        self.grad -= 1
                new_brick.rect.x = x_position
                new_brick.rect.y = y_position
                holder.add(new_brick)
                x_position += self.brick_width
            if self.grad_up:
                if self.grad >= 180:
                    self.grad = self.base_grad
            else:
                if self.grad <= 1:
                    self.grad = self.base_grad
            x_position = 0
            y_position += self.brick_height
    
    def gen_level(self, x_position, y_position, width, height, holder, level, inner=False, grad=""):
        self.star = False
        if height >= self.brick_height:
            y_position = 0
        else:
            y_position = 3
        self.grad = self.base_grad
        x_position = 0
        if not self.easy_start:
            rise = self.screen_height
            run = self.screen_width
        elif self.easy_start:
            rise = 125
            run = 5
        while y_position < rise:
            while x_position < run:
                new_brick = self.brick_base(width, height, inner, x_position, y_position)
                if grad:
                    new_brick.gradient(f"{grad}", int(self.grad))
                    pass
                if not self.easy_start:
                    new_brick.rect.x = x_position
                    new_brick.rect.y = y_position
                elif self.easy_start:
                    new_brick.rect.x = self.mball.rect.x
                    new_brick.rect.y = self.mball.rect.y
                    new_brick.soul_sale()
                for lost in getattr(self, f"Dict{level}").dict.values():
                    if not inner:
                        if x_position == lost[0] and y_position == lost[1]:
                            holder.add(new_brick)
                    if inner:
                        if x_position == lost[0] and y_position == lost[1]+3:
                            holder.add(new_brick)
                getattr(self, f"spec{level}").full_specs(x_position, y_position, new_brick)
                if new_brick not in holder:
                    new_brick.kill()
                    if not inner:
                        self.brick_dict.pop(new_brick)
                    elif inner:
                        self.bricke_dict.pop(new_brick)
                if new_brick in holder:
                    if self.grad_up:
                        if self.grad <= 180:
                            self.grad += 1
                    else:
                        if self.grad > 1:
                            self.grad -= 1
                x_position += self.brick_width
            if self.grad_up:
                if self.grad >= 180:
                    self.grad = self.base_grad
            else:
                if self.grad <= 1:
                    self.grad = self.base_grad
            x_position = 0
            y_position += self.brick_height

    def brick_base(self, width, height, inner, x, y):
        self.shrapnel.empty()
        for sphere in self.spherage:
            sphere.recenters()
        new_brick = Brick(self, width, height, inner)
        if height >= self.brick_height:
            self.brick_dict[new_brick] = [x, y]
        elif height < self.brick_height:
            self.bricke_dict[new_brick] = [x, y]
        return(new_brick)

    def spring_ball(self):
        """Creates a ball with the Ball class."""
        if self.started == False:
            self.mball = Ball(self)
            self.spherage.add(self.mball)
        else:
            ball = Ball(self, True)
            self.spherage.add(ball)
    
    def explode(self, x, y):
        """Creates the ball explosion from an explosive brick."""
        echos = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        for echo in echos:
            setattr(self, echo, Ball(self, war_crime=True, chain=False))
        self.shrapnel.add(self.N, self.NE, self.E, self.SE, self.S, self.SW, self.W, self.NW)
        self.N.moving_up, self.N.moving_down, self.N.moving_right, self.N.moving_left = True, False, False, False
        self.NE.moving_up, self.NE.moving_down, self.NE.moving_right, self.NE.moving_left = True, False, True, False
        self.E.moving_up, self.E.moving_down, self.E.moving_right, self.E.moving_left = False, False, True, False
        self.SE.moving_up, self.SE.moving_down, self.SE.moving_right, self.SE.moving_left = False, True, True, False
        self.S.moving_up, self.S.moving_down, self.S.moving_right, self.S.moving_left = False, True, False, False
        self.SW.moving_up, self.SW.moving_down, self.SW.moving_right, self.SW.moving_left = False, True, False, True
        self.W.moving_up, self.W.moving_down, self.W.moving_right, self.W.moving_left = False, False, False, True
        self.NW.moving_up, self.NW.moving_down, self.NW.moving_right, self.NW.moving_left = True, False, False, True
        for war_crime in self.shrapnel:
            if war_crime not in self.launched:
                war_crime.rect.x = x + 22
                war_crime.rect.y = y + 2
                war_crime.x = x + 22
                war_crime.y = y + 2
                self.launched.append(war_crime)
    
    def doppelexplode(self, x, y):
        """Creates the ball explosion from an explosive brick."""
        echos = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        for echo in echos:
            setattr(self, echo, Ball(self, war_crime=True, chain=True))
        self.shrapnel.add(self.N, self.NE, self.E, self.SE, self.S, self.SW, self.W, self.NW)
        self.N.moving_up, self.N.moving_down, self.N.moving_right, self.N.moving_left = True, False, False, False
        self.NE.moving_up, self.NE.moving_down, self.NE.moving_right, self.NE.moving_left = True, False, True, False
        self.E.moving_up, self.E.moving_down, self.E.moving_right, self.E.moving_left = False, False, True, False
        self.SE.moving_up, self.SE.moving_down, self.SE.moving_right, self.SE.moving_left = False, True, True, False
        self.S.moving_up, self.S.moving_down, self.S.moving_right, self.S.moving_left = False, True, False, False
        self.SW.moving_up, self.SW.moving_down, self.SW.moving_right, self.SW.moving_left = False, True, False, True
        self.W.moving_up, self.W.moving_down, self.W.moving_right, self.W.moving_left = False, False, False, True
        self.NW.moving_up, self.NW.moving_down, self.NW.moving_right, self.NW.moving_left = True, False, False, True
        for war_crime in self.shrapnel:
            if war_crime not in self.launched:
                war_crime.rect.x = x + 22
                war_crime.rect.y = y + 2
                war_crime.x = x + 22
                war_crime.y = y + 2
                self.launched.append(war_crime)
    
    def resets(self):
        for brick in self.bricks:
            brick.kill()
        for brick in self.brickes:
            brick.kill()
        self.new_began = False
        self.update_screen()
        self.clock.tick(self.frame_rate)
        self.create_wall()

    def lives(self):
        """Show how many balls are left."""
        self.livess = Group()
        if not self.started:
            for life_number in range(self.lives_left):
                ball = Bal(self)
                ball.rect.x = 10 + life_number * ball.rect.width
                ball.rect.y = 10
                self.livess.add(ball)
        self.livess.draw(self.screen)
    
    def horcrux(self):
        """Increases life by one."""
        snake = Bal(self)
        nombre = self.livess.sprites()[-1]
        snake.rect.x = 10 + nombre.rect.x + 5
        snake.rect.y = 10
        self.livess.add(snake)
    
    def star_up(self):
        """Adds a star power up."""
        star = Star(self)
        if len(self.stars) > 0:
            nombre = self.stars.sprites()[-1]
            star.rect.x = -10 + nombre.rect.x + -10
            star.rect.y = 10
        else:
            star.rect.x = self.screen_width - 20
            star.rect.y = 10
        self.stars.add(star)

    def doubar(self):
        """Doubles bar."""
        offset = self.screen_rect.centerx-self.middlebreaker.rect.x
        self.rightbreaker = BigRightBreaker(self)
        self.farrightbreaker = BigFarRightBreaker(self)
        self.leftbreaker = BigLeftBreaker(self)
        self.farleftbreaker = BigFarLeftBreaker(self)
        self.middlebreaker = BigMiddleBreaker(self)
        self.rightbreaker.x -= offset
        self.farrightbreaker.x -= offset
        self.leftbreaker.x -= offset
        self.farleftbreaker.x -= offset
        self.middlebreaker.x -= offset
    
    def rebar(self):
        offset = self.screen_rect.centerx-self.middlebreaker.rect.x
        self.rightbreaker = RightBreaker(self)
        self.farrightbreaker = FarRightBreaker(self)
        self.leftbreaker = LeftBreaker(self)
        self.farleftbreaker = FarLeftBreaker(self)
        self.middlebreaker = MiddleBreaker(self)
        self.rightbreaker.x -= offset
        self.farrightbreaker.x -= offset
        self.leftbreaker.x -= offset
        self.farleftbreaker.x -= offset
        self.middlebreaker.x -= offset
    
    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)
    
    def trail(self):
        tral = Bal(self, self.spins)
        tral.rect.x = self.mball.x
        tral.rect.y = self.mball.y
        self.trails.append(tral)

class Ball(Sprite):
    """Makes ball"""

    def __init__(self, bounce, new=False, war_crime=False, chain=False):
        super().__init__()
        self.chain = chain
        self.war_crime = war_crime
        self.new = new
        self.bouncer = bounce
        self.dead = False
        self.dead_time = 100
        self.screen = bounce.screen
        self.screen_rect = self.screen.get_rect()
        self.recenter = False
        size = 15
        self.spangle = 0
        self.fly = 0
        if self.bouncer.main_spins:
            self.spinny = 1
        else:
            self.spinny = 0
        self.is_scale = (size,size)
        if self.war_crime:
            self.is_scale = (5,5)

        self.image = pygame.image.load(r("Marble.png")).convert_alpha()
        self.rotated_image = pygame.image.load(r("Marble.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.is_scale)
        self.fatal = []
        self.matlod = []
        self.rect = self.image.get_rect()
        if not new:
            self.rect.center = self.screen_rect.center
        elif new:
            self.rect.center = self.bouncer.mball.rect.center

        # Puts coordinates as floats
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        if not new:
            self.y += 200
            self.x -= 15
        elif new:
            pass

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.smoving_right = False
        self.fmoving_right = False
        self.moving_left = False
        self.smoving_left = False
        self.fmoving_left = False
        if new:
            self.moving_up = self.bouncer.mball.moving_up
            self.moving_down = self.bouncer.mball.moving_down
            self.moving_right = self.bouncer.mball.moving_right
            self.smoving_right = self.bouncer.mball.smoving_right
            self.fmoving_right = self.bouncer.mball.fmoving_right
            self.moving_left = self.bouncer.mball.moving_left
            self.smoving_left = self.bouncer.mball.smoving_left
            self.fmoving_left = self.bouncer.mball.fmoving_left
        self.spherage = pygame.sprite.Group()
        if not war_crime:
            self.spherage.add(self)
    
    def update(self):
        """Runs all collision checks for the bar, box and bricks as well as conducting the motion of the balls."""
        self.box_checks()
        self.brick_checks()
        self.bar_checks()
        if self.dead_time > 100:
            self.motion()
        self.dead_time += 1
        self.rot_center(self.image, self.spinny, self.rect.centerx, self.rect.centery)
        if self.dead:
            self.dead_time = 0
            self.dead = False
        #self.screen.blit(self.image, self.rect)
    
    def spin_inator(self, image_index):
        self.images = ["Arrow", "Marble", "Can_No_See"]
        self.image = pygame.image.load(r(f"{self.images[image_index%3]}.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.is_scale).convert_alpha()
    
    def rot_center(self, image, angle, x, y):
        if self.dead_time % 1 == 0:
            self.rotated_image = pygame.transform.rotate(image, self.spangle)
            self.spangle += self.spinny
        new_rect = self.rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        self.screen.blit(self.rotated_image, new_rect)
    
    def motion(self):
        """Does the moving where moving wants doing?"""
        if self.war_crime:
            if self.moving_up:
                self.y -= 25
            elif self.moving_down:
                self.y += 25
            if self.moving_left:
                self.x -= 25
            elif self.moving_right:
                self.x += 25
        else:
            if self.moving_up:
                self.y -= 2.5
            elif self.moving_down:
                self.y += 2.5
            if self.moving_left:
                if self.smoving_left:
                    self.x -= 2.5
                elif self.fmoving_left:
                    self.x -= 3.5
            elif self.moving_right:
                if self.smoving_right:
                    self.x += 2.5
                elif self.fmoving_right:
                    self.x += 3.5
        
        self.rect.y = self.y
        self.rect.x = self.x
        if self.chain:
            self.fly += 1
        if self.fly > 2:
            self.kill()
        if self.recenter:
            self.recenters()
    
    def box_checks(self):
        """Checks for screen side collisions."""
        if self.rect.top <= self.screen_rect.top and self in self.bouncer.shrapnel:
            self.kill()
        elif self.rect.top <= self.screen_rect.top:
            self.moving_up = False
            self.moving_down = True
        if self.rect.top >= self.screen_rect.bottom and self in self.bouncer.shrapnel:
            self.kill()
        elif self.rect.top >= self.screen_rect.bottom:
            if self.new:
                self.kill()
            self.recenter = True
            self.moving_down = True
            self.moving_up = False
            self.moving_left = False
            self.moving_right = True
            self.fmoving_right = True
            if len(self.bouncer.livess.sprites()) > 0:
                if not self.new:
                    first_sprite = self.bouncer.livess.sprites()[-1]
                    first_sprite.kill()
            else:
                pygame.quit()
                sys.exit()
        if self.rect.left <= self.screen_rect.left and self in self.bouncer.shrapnel:
            self.kill()
        elif self.rect.left <= self.screen_rect.left:
            self.moving_left = False
            self.moving_right = True
            if self.smoving_left:
                self.smoving_right = True
                self.smoving_left = False
                self.fmoving_right = False
                self.fmoving_left = False
            elif self.fmoving_left:
                self.fmoving_right = True
                self.fmoving_left = False
                self.smoving_right = False
                self.smoving_left = False
            # self.smoving_left = False
            # self.fmoving_left = False
            # self.moving_right = True
        if self.rect.right >= self.screen_rect.right and self in self.bouncer.shrapnel:
            self.kill()
        elif self.rect.right >= self.screen_rect.right:
            self.moving_right = False
            self.moving_left = True
            if self.smoving_right:
                self.smoving_left = True
                self.smoving_right = False
                self.fmoving_left = False
                self.fmoving_right = False
            elif self.fmoving_right:
                self.fmoving_left = True
                self.fmoving_right = False
                self.smoving_left = False
                self.smoving_right = False
            # self.smoving_right = False
            # self.fmoving_right = False
            # self.moving_left = True
    
    def bar_checks(self):
        """Checks and acts on collisions of sphere and bar"""
        self.rcollisions = pygame.sprite.collide_rect(self, self.bouncer.rightbreaker)
        self.frcollisions = pygame.sprite.collide_rect(self, self.bouncer.farrightbreaker)
        self.lcollision = pygame.sprite.collide_rect(self, self.bouncer.leftbreaker)
        self.flcollision = pygame.sprite.collide_rect(self, self.bouncer.farleftbreaker)
        self.collisioned = pygame.sprite.collide_rect(self, self.bouncer.middlebreaker)
        collistion = [self.frcollisions, self.flcollision]
        if self.bouncer.joystick:# and self.bouncer.rumbles:
            for list in collistion:
                if list:
                    self.bouncer.joystick.rumble(100,150,50)
        if self.collisioned:
            self.moving_down = False
            self.moving_up = True
        if self.frcollisions:
            self.moving_down = False
            self.moving_up = True
            if not self.moving_right:
                self.moving_right = True
                self.smoving_right = False
                self.fmoving_right = True   
                self.moving_left = False
            self.moving_right = True  
        elif self.rcollisions:
            self.moving_down = False
            self.moving_up = True
            if not self.moving_right:
                self.moving_right = True
                self.smoving_right = True
                self.fmoving_right = False
                self.moving_left = False
            self.moving_right = True               
        elif self.flcollision:
            self.moving_down = False
            self.moving_up = True
            if not self.moving_left:
                self.moving_left = True
                self.smoving_left = False
                self.fmoving_left = True
                self.moving_right = False
            self.moving_left = True   
        elif self.lcollision:
            self.moving_down = False
            self.moving_up = True
            if not self.moving_left:
                self.moving_left = True
                self.smoving_left = True
                self.fmoving_left = False 
                self.moving_right = False 
            self.moving_left = True                 
        elif self.bouncer.shielded < 10000 and self.y + (self.rect.height-10) > self.bouncer.middlebreaker.rect.y:
            self.moving_down = False
            self.moving_up = True
        
    def brick_checks(self):
        """Checks for and acts on contacts of sphere and brick."""
        self.brick_broken = pygame.sprite.groupcollide(self.bouncer.can_update, self.spherage, False, False)
        self.brik_broken = pygame.sprite.groupcollide(self.bouncer.can_upadte, self.spherage, False, False)
        self.bomb_breaker = pygame.sprite.groupcollide(self.bouncer.bricks, self.bouncer.shrapnel, True, True)
        self.brock_broken = pygame.sprite.groupcollide(self.bouncer.can_upadte, self.bouncer.bricks, False, False)
        self.relayer = pygame.sprite.groupcollide(self.bouncer.bricks, self.bouncer.can_upadte, False, False)
        # self.special_bricks()
        if self.brik_broken:
            if self.moving_left:
                self.moving_left = False
                self.moving_right = True
                if self.smoving_left:
                    self.smoving_right = True
                    self.smoving_left = False
                    self.fmoving_right = False
                    self.fmoving_left = False
                elif self.fmoving_left:
                    self.fmoving_right = True
                    self.fmoving_left = False
                    self.smoving_right = False
                    self.smoving_left = False
            elif self.moving_right:
                self.moving_left = True
                self.moving_right = False
                if self.smoving_right:
                    self.smoving_left = True
                    self.smoving_right = False
                    self.fmoving_left = False
                    self.fmoving_right = False
                elif self.fmoving_right:
                    self.fmoving_left = True
                    self.fmoving_right = False
                    self.smoving_left = False
                    self.smoving_right = False
            self.brik_broken.clear()
        elif self.brick_broken:
            if self.moving_up:
                self.moving_up = False
                self.moving_down = True
            elif self.moving_down:
                self.moving_up = True
                self.moving_down = False
        if self.bomb_breaker:
            self.bouncer.borders()
            self.bouncer.borderes()
        self.special_bricks()
        self.phylactery()
        self.brick_broken.clear()
        self.extra_clear(self.brock_broken)

    def phylactery(self):
        for lich in self.brick_broken:
            if lich not in self.bouncer.locked:
                if lich not in self.bouncer.undamaged:
                    lich.kill()
                    try:
                        self.bouncer.brick_dict.pop(lich)
                    except KeyError:
                        pass
                    self.bouncer.borders()
                    self.bouncer.borderes()
                if lich in self.bouncer.undamaged:
                    self.bouncer.undamaged.remove(lich)
                    lich.damage()
        for lich in self.bomb_breaker:
            if lich not in self.bouncer.undamaged:
                lich.kill()
                try:
                    self.bouncer.brick_dict.pop(lich)
                except KeyError:
                    pass
                self.bouncer.borders()
                self.bouncer.borderes()
            if lich in self.bouncer.undamaged:
                self.bouncer.undamaged.remove(lich)
                lich.damage()
    
    def special_bricks(self):
        """Runs special brick comparisons."""
        if self.chain:
            time_save = self.bomb_breaker
        else:
            time_save = pygame.sprite.Group()
        if True:#not self.chain:
            for shard in self.brick_broken or time_save:
                if shard in self.bouncer.locked:
                    #self.bouncer.bricks.add(shard)
                    pass
                elif shard in self.bouncer.keys:
                    for padlock in self.bouncer.locked:
                        if padlock not in self.bouncer.unbreakable:
                            padlock.open()
                        else:
                            self.matlod.append(padlock)
                    for immutable in self.matlod:
                        self.bouncer.locked.append(immutable)
                    self.matlod.clear()
                elif shard in self.bouncer.plus:
                    self.bouncer.plus.remove(shard)
                    self.bouncer.spring_ball()
                elif shard in self.bouncer.bomb:
                    self.bouncer.bomb.remove(shard)
                    x = shard.rect.x
                    y = shard.rect.y
                    shard.kill()
                    self.bouncer.brick_dict.pop(shard)
                    self.bouncer.borders()
                    self.bouncer.borderes()
                    self.bouncer.explode(x,y)
                elif shard in self.bouncer.doppelbomb:
                    self.bouncer.doppelbomb.remove(shard)
                    x = shard.rect.x
                    y = shard.rect.y
                    shard.kill()
                    self.bouncer.brick_dict.pop(shard)
                    self.bouncer.borders()
                    self.bouncer.borderes()
                    self.bouncer.doppelexplode(x,y)
                elif shard in self.bouncer.new_begin:
                    self.bouncer.kinds()
                    self.bouncer.new_began = True
                    for sphere in self.spherage:
                        sphere.recenters()
                elif shard in self.bouncer.lotus:
                    for cat in range(1,21):
                        self.bouncer.horcrux()
                elif shard in self.bouncer.shiny:
                    self.bouncer.star_up()
                elif shard in self.bouncer.sealing:
                    self.y = 25
                elif shard in self.bouncer.cardinal:
                    victory = False
                    while not victory:
                        victory = self.magnet(shard)
                elif shard in self.bouncer.barrier:
                    self.bouncer.shielded = 0
                elif shard in self.bouncer.acidic:
                    for material in self.bouncer.undamaged:
                        material.damage()
                    self.bouncer.undamaged.clear()
                elif shard in self.bouncer.accelerate:
                    self.bouncer.sped_up = 0
                elif shard in self.bouncer.will_expand:
                    shard.bar_expand()
                    self.bouncer.unbreakable.append(shard)
                    self.bouncer.locked.append(shard)
                elif shard in self.bouncer.adoored:
                    self.bouncer.next = True
                self.keye(shard)
                if self.bouncer.shined < 10000:
                    x = shard.rect.x
                    y = shard.rect.y
                    shard.kill()
                    try:
                        self.bouncer.brick_dict.pop(shard)
                        self.bouncer.borders()
                        self.bouncer.borderes()
                    except KeyError:
                        pass
                    if self not in self.bouncer.launched:
                        self.bouncer.doppelexplode(x,y)
                if shard in self.bouncer.expand:
                    self.bouncer.unbreakable.append(shard)
                    self.bouncer.locked.append(shard)
                    self.excalibur(shard)
            for shard in self.bouncer.keys:
                if shard in self.bomb_breaker:
                    for padlock in self.bouncer.locked:
                        if padlock not in self.bouncer.unbreakable:
                            padlock.open()
                        else:
                            self.matlod.append(padlock)
            for shard in self.brik_broken:
                if shard in self.bouncer.undamaged:
                    shard.damage()
                    if not shard in self.bouncer.locked:
                        self.bouncer.undamaged.remove(shard)
                    self.bouncer.brickes.add(shard)

    def recenters(self):
        """Returns the ball to the center"""
        self.rect.center = self.screen_rect.center
        self.rect.y += 200
        self.rect.x -= 20
        self.y = self.rect.y
        self.x = self.rect.x
        self.recenter = False
        self.dead = True
    
    def extra_clear(self, brock_broken):
        for brickoge in self.bouncer.can_upadte:
            if brickoge not in brock_broken:
                brickoge.kill()
                try:
                    self.bouncer.bricke_dict.pop(brickoge)
                except KeyError:
                    print("Inner key error")
                self.bouncer.borders()
                self.bouncer.borderes()
        for brick in self.bouncer.unlocked:
            if brick in self.bouncer.locked:
                self.bouncer.locked.remove(brick)
    
    def keye(self, shard):
        if shard in self.bouncer.vermillion:
            for carf in self.bouncer.vermillionlock:
                carf.open()
        elif shard in self.bouncer.phthalo:
            for carf in self.bouncer.phthalolock:
                carf.open()
        elif shard in self.bouncer.sapphire:
            for carf in self.bouncer.sapphirelock:
                carf.open()
        elif shard in self.bouncer.royal:
            for carf in self.bouncer.royallock:
                carf.open()
    
    def excalibur(self, shard):
        if shard in self.bouncer.expand1:
            shard.bar_damage1()
            self.bouncer.borders()
            self.bouncer.borderes()
            self.bouncer.expand1.remove(shard)
        elif shard in self.bouncer.expand2:
            shard.bar_damage2()
            self.bouncer.borders()
            self.bouncer.borderes()
            self.bouncer.expand2.remove(shard)
        elif shard in self.bouncer.expand3:
            shard.bar_damage3()
            self.bouncer.borders()
            self.bouncer.borderes()
            self.bouncer.expand3.remove(shard)
        elif shard in self.bouncer.expand4:
            shard.bar_damage4()
            self.bouncer.borders()
            self.bouncer.borderes()
            self.bouncer.expand4.remove(shard)
        elif shard in self.bouncer.expand5:
            self.bouncer.doubar()
            self.bouncer.expand5.remove(shard)
            self.bouncer.unbreakable.remove(shard)
            self.bouncer.locked.remove(shard)
            shard.kill()
            self.bouncer.brick_dict.pop(shard)
            self.bouncer.borders()
            self.bouncer.borderes()
            self.bouncer.next = True
            self.easy_start = open("Start_clause.txt.txt", 'w')
            self.easy_start.write("True")
            self.easy_start.close()
    
    def magnet(self, shard):
        directions = ['Never', 'Never', 'Eat', 'Eat', 'Eat', 'Eat', 'Shredded', 'Wheat', 'Wheat', 'Wheat', 'Wheat']
        direction = random.choice(directions)
        victory = False
        for pole in self.bouncer.bricks:
            if direction == 'Never':
                if pole.rect.x == shard.rect.x and pole.rect.y < shard.rect.y:
                    pole.kill()
                    victory = True
            elif direction == 'Eat':
                if pole.rect.y == shard.rect.y and pole.rect.x > shard.rect.x:
                    pole.kill()
                    victory = True
            elif direction == 'Shredded':
                if pole.rect.x == shard.rect.x and pole.rect.y > shard.rect.y:
                    pole.kill()
                    victory = True
            elif direction == 'Wheat':
                if pole.rect.y == shard.rect.y and pole.rect.x < shard.rect.x:
                    pole.kill()
                    victory = True
        for poles in self.bouncer.bricks:
            poles.update()
        for pol in self.bouncer.brickes:
            if direction == 'Never':
                if pol.rect.x == shard.rect.x and pol.rect.y < shard.rect.y:
                    pol.up_outer()
                    pol.update()
            elif direction == 'Eat':
                if pol.rect.y-3 == shard.rect.y and pol.rect.x > shard.rect.x:
                    pol.right_outer()
                    pol.update()
            elif direction == 'Shredded':
                if pol.rect.x == shard.rect.x and pol.rect.y > shard.rect.y:
                    pol.down_outer()
                    pol.update()
            elif direction == 'Wheat':
                if pol.rect.y-3 == shard.rect.y and pol.rect.x < shard.rect.x:
                    pol.left_outer()
                    pol.update()
        pygame.display.flip()
        self.bouncer.clock.tick(self.bouncer.frame_rate)
        return(victory)

class Bal(Sprite):
    """Spoofs a ball for lives."""
    def __init__(self, bounce, spins=False, loom=False, screct=True):
        """Does it all."""
        super().__init__()
        self.bouncer = bounce
        self.loom = loom
        self.spins = spins
        self.screen = self.bouncer.screen
        is_scale = (15,15)
        self.image = pygame.image.load(r("Marble.png")).convert_alpha()
        if not self.loom:
            if self.bouncer.started:
                self.image = self.bouncer.mball.image
        self.image = pygame.transform.scale(self.image, is_scale)
        self.rect: pygame.Rect = self.image.get_rect()
        if self.loom and screct:
            self.rect = self.bouncer.player.screct
    
    def update(self, opacity=1):
        if not self.loom:
            if self.spins:
                self.image = self.bouncer.mball.rotated_image.convert_alpha()
            else:
                self.image = self.bouncer.mball.image.convert_alpha()
            self.blit_alpha(self.screen, self.image, (self.rect.x, self.rect.y), opacity)
        else:
            self.bouncer.screen.blit(self.image, self.rect)
    
    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)
    
class Star(Sprite):
    """Creates the star sprite for powerup bar"""
    def __init__(self, bounce):
        """Does it all."""
        super().__init__()
        self.bouncer = bounce
        self.screen = self.bouncer.screen
        is_scale = (20,20)
        self.image = pygame.image.load(r("Star_Icon_Small.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, is_scale)
        self.rect = self.image.get_rect()
    
    def update(self):
        self.screen.blit(self.image, self.rect)

class Brick(Sprite):
    """Creates the bricks out of which one must break."""
    
    def __init__(self, bouncer=Bouncing, width=10, height=10, inner=False):
        """Initialise the basic attributes of the bricks."""
        super().__init__()
        self.inner = inner
        self.bouncer = bouncer
        self.screen = bouncer.screen
        self.screen_rect = self.screen.get_rect()
        self.scaled = (width,height)
        self.image = pygame.image.load(r("RedBrickWide.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load(r("Seafoam.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        self.rect = self.image.get_rect()
        self.leest = []
        self.los = []
        for cat in range(0,50):
            self.los.append(cat*width)
        for cat in range(50,19,-1):
            self.leest.append(cat)
        for cat in range(19,50):
            self.leest.append(cat)
    
    def update(self):
        """Updates the bricks."""
        # self.timer = self.bouncer.timer
        # self.timer = round(self.timer/(len(self.bouncer.bricks)/5))
        # self.image.fill((0, self.leest[self.timer%len(self.leest)], self.leest[self.timer%len(self.leest)]))
        self.screen.blit(self.image, self.rect)
        # if self.timer % 6 == 0:
        #     if self.xount < 20:
        #         self.xount += 1
        #     else:
        #         self.xount = 0
    
    # Brick sprite changes and list appends for special bricks.

    def reinforce(self):
        self.image = pygame.image.load(r("BlueBorderBrickWide.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.rect.height < self.bouncer.brick_height:
            self.image = pygame.image.load(r("BlueBrickWide.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load(r("Seafoam.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        self.bouncer.undamaged.append(self)
    
    def gunpowder(self):
        self.image = pygame.image.load(r("BombBrickWide.png")).convert_alpha()
        self.innervate()
        self.bouncer.bomb.append(self)

    def doppelgunpowder(self):
        self.image = pygame.image.load(r("DoppelBombBrickWide.png")).convert_alpha()
        self.innervate()
        self.bouncer.doppelbomb.append(self)
    
    def smolgunpowder(self):
        self.image = pygame.image.load(r("BombBrickSmol.png")).convert_alpha()
        self.innervate()
        self.bouncer.doppelbomb.append(self)

    def lock(self):
        self.image = pygame.image.load(r("HardBrickWide.png")).convert_alpha()
        self.innervate()
        self.bouncer.locked.append(self)
        self.bouncer.lockaged.add(self)

    def key(self):
        self.image = pygame.image.load(r("KeyWide.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load(r("Seafoam.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        self.bouncer.keys.append(self)
    
    def open(self):
        if self in self.bouncer.bomb:
            self.image = pygame.image.load(r("BombBrickWide.png")).convert_alpha()
        elif self in self.bouncer.bomb:
            self.image = pygame.image.load(r("BombBrickWide.png")).convert_alpha()
        elif self in self.bouncer.doppelbomb:
            self.image = pygame.image.load(r("DoppelBombBrickWide.png")).convert_alpha()
        elif self in self.bouncer.lotus:
            self.image = pygame.image.load(r("Lotus.png")).convert_alpha()
        elif self in self.bouncer.new_begin:
            self.image = pygame.image.load(r("RedoBrick.png")).convert_alpha()
        else:
            self.image = pygame.image.load(r("HardGreenBrickWide.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load(r("Seafoam.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        self.bouncer.unlocked.append(self)

    def unbreak(self):
        self.image = pygame.image.load(r("UnbrickMoss.png")).convert_alpha()
        self.innervate()
        self.bouncer.unbreakable.append(self)
        self.bouncer.locked.append(self)
        self.bouncer.lockaged.add(self)
    
    def redo(self):
        self.image = pygame.image.load(r("RedoBrick.png")).convert_alpha()
        self.innervate()
        self.bouncer.new_begin.append(self)

    def star(self):
        self.image = pygame.image.load(r("YeStarBrickWide.png")).convert_alpha()
        self.innervate()
        self.bouncer.shiny.append(self)
    
    def plus_one(self):
        self.image = pygame.image.load(r("PlusOneWide.png")).convert_alpha()
        self.innervate()
        self.bouncer.plus.append(self)
    
    def homicide(self):
        self.image = pygame.image.load(r("Lotus.png")).convert_alpha()
        self.innervate()
        self.bouncer.lotus.append(self)
    
    def bar_expand(self):
        self.image = pygame.image.load(r("MonsterBrickKind.png")).convert_alpha()
        self.innervate()
        self.bouncer.expand.append(self)
        self.bouncer.expand1.append(self)
        self.bouncer.expand2.append(self)
        self.bouncer.expand3.append(self)
        self.bouncer.expand4.append(self)
        self.bouncer.expand5.append(self)
    
    def bar_damage1(self):
        self.image = pygame.image.load(r("MonsterBrick.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def bar_damage2(self):
        self.image = pygame.image.load(r("MonsterBrickAngry.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def bar_damage3(self):
        self.image = pygame.image.load(r("MonsterBrickInjured.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def bar_damage4(self):
        self.image = pygame.image.load(r("MonsterBrickDying.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def mystiry(self):
        self.image = pygame.image.load(r("Mystiry.png")).convert_alpha()
        self.innervate()
        fortuna = [
            self.bouncer.plus,
            self.bouncer.bomb,
            self.bouncer.doppelbomb,
            self.bouncer.new_begin,
            self.bouncer.lotus,
            self.bouncer.will_expand]
        fortune = random.choice(fortuna)
        fortune.append(self)
    
    def ceiling(self):
        self.image = pygame.image.load(r("BarExpand.png")).convert_alpha()
        self.innervate()
        self.bouncer.sealing.append(self)
    
    def compass(self):
        self.image = pygame.image.load(r("MappedCompass.png")).convert_alpha()
        self.innervate()
        self.bouncer.cardinal.append(self)
    
    def shield(self):
        self.image = pygame.image.load(r("Shield_Brick.png")).convert_alpha()
        self.innervate()
        self.bouncer.barrier.append(self)
    
    def gradient(self, colour, shade):
        try:
            self.image = pygame.image.load(r(f"{colour}{shade}.png")).convert_alpha()
        except FileNotFoundError:
            self.image = pygame.image.load(r(f"{colour}1.png")).convert_alpha()
            print("GraphicsFileError")
            self.bouncer.grad = self.bouncer.base_grad
        self.image.fill((0,shade,shade))
        self.image.blit(pygame.image.load(r("See_Through_Wide.png")), (0,0))
        self.innervate()
    
    def up_outer(self):
        self.image = pygame.image.load(r("RemnantUp.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def right_outer(self):
        self.image = pygame.image.load(r("RemnantRight.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def down_outer(self):
        self.image = pygame.image.load(r("RemnantDown.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def left_outer(self):
        self.image = pygame.image.load(r("RemnantLeft.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def acid(self):
        self.image = pygame.image.load(r("Acid_Brick.png")).convert_alpha()
        self.innervate()
        self.bouncer.acidic.append(self)
    
    def paint_stripe(self):
        self.image = pygame.image.load(r("Fast_Clock.png")).convert_alpha()
        self.innervate()
        self.bouncer.accelerate.append(self)
    
    def fancekey(self, colour):
        try:
            self.image = pygame.image.load(r("KeyWide.png")).convert_alpha()
        except FileNotFoundError:
            pass
        self.innervate()
        getattr(self.bouncer, f"{colour.lower()}").append(self)
    
    def coulock(self, colour):
        try:
            self.image = pygame.image.load(r("HardBrickWide.png")).convert_alpha()
        except FileNotFoundError:
            print("DASD")
        self.innervate()
        getattr(self.bouncer, f"{colour.lower()}lock").append(self)
        self.bouncer.locked.append(self)
    
    def soul_sale(self):
        self.image = pygame.image.load(r("Door.png")).convert_alpha()
        self.innervate()
        self.bouncer.adoored.append(self)

    def damage(self):
        """Switches to the damaged sprite."""
        self.image = pygame.image.load(r("BlueBrickWide.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load(r("Seafoam.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
    
    def innervate(self):
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load(r("Seafoam.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        if self in self.bouncer.undamaged:
            self.bouncer.undamaged.remove(self)
    
class Button(Sprite):
    """Attempts to create pause screen buttons"""

    def __init__(self, bouncer, width, height, x, y, image):
        super().__init__()
        self.scale = (width, height)
        self.bouncer = bouncer
        self.screen = self.bouncer.screen
        self.image = pygame.image.load(r(f"{image}.png"))
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.screen.blit(self.image, self.rect)

################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

class Yarn:
    """Attempts to create an inner game."""

    def __init__(self, bouncer):
        self.bouncer = bouncer
        self.undamaged = []
        self.cat = 0

    def real_init(self):
        self.bouncer.frame_rate = 0
        self.down_timer = 0
        self.leap = 0
        self.gravity = 0.5
        self.base_gravity = self.gravity
        self.brick_width = 64
        self.brick_height = 64
        self.apparence = 1000
        self.predicts_length = 80
        self.quick_fall = False
        self.attack = False
        self.clickage = False
        self.x_pressed = False
        self.Φ = False
        self.Φ_held = 0
        self.traline = False
        self.jump_hold = False
        self.stick = False
        self.paused = False
        self.fade = False
        self.linear = False
        self.trail_stop = False
        self.predicting: bool = False
        self.visible: bool = False
        file = open(r("Relevents1.pickle"), 'rb')
        self.full_run = pickle.load(file)
        print(self.full_run)
        self.timer = '0'
        self.hides = []
        self.clock = pygame.time.Clock()
        self.current_level = [0,0]
        self.screen = screen
        self.screen.blit(pygame.transform.scale(pygame.image.load(r("MonsterBrickKind.png")), (1280,720)), self.screen.get_rect())
        pygame.display.flip()
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Bouncing Gimmick")
        iconic = pygame.image.load(r("MonsterBrick.png"))
        pygame.display.set_icon(iconic)
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(self.joystick.get_power_level())
        else:
            self.joystick = False
        self.sword_swipe = pygame.rect.Rect(0, 0, 50, 35)
        self.sword = self.listerine("Sword_Sheet.png", 50, 50)
        self.unpause = Button(self, 50, 50, self.screen_rect.centerx-25, self.screen_rect.centery-25, "Unpause")
        self.swipe_time = 0

        self.player: Player = Player(self)
        self.parab()
        self.evils: Group[Smart_Goblin] = pygame.sprite.Group()
        self.can_hit = pygame.sprite.Group()
        try:
            self.level = open("LEVEL.txt", 'r')
            home_1 = self.level.readline(-4).rstrip("\n")
            home_2 = self.level.readline(-3).rstrip("\n")
            home_dirp = self.level.readline(-2).rstrip("\n")
            home_derp = self.level.readline(-1).rstrip("\n")
        except FileNotFoundError:
            self.level = open("LEVEL.txt", 'w')
            self.level.write("0\n0\n32\n576")
            home_1 = 0
            home_2 = 0
            home_dirp = 32
            home_derp = 576
            premiere(1)
        home_dir = [0,0]
        home_dir[0] = int(home_dirp)
        home_dir[1] = int(home_derp)
        print(home_dir)
        self.current_level[0], self.current_level[1] = int(home_1), int(home_2)
        self.walls = pygame.sprite.Group()
        try:
            self.toil = Toim_Chart(r(f"Chared{home_1}_{home_2}.tmj"), loom=self, started=False)
        except FileNotFoundError:
            self.toil = Toim_Chart(f'UTL/UTL/Chared0_0.csv', self)
        self.level.close()
        self.tiles = self.toil.tiles
        self.brick_x_plus = 0
        self.brick_y_plus = 0
        self.catch_plat = Brick(self, 72/game_scale,22/game_scale)
        self.left_pole = Brick(self, 20/game_scale,20/game_scale)
        self.left_pole.rect.x = 100/game_scale
        self.left_pole.rect.y = -20/game_scale
        self.right_pole = Brick(self, 20/game_scale,20/game_scale)
        self.right_pole.rect.x = 300/game_scale
        self.right_pole.rect.y = -20/game_scale
        self.players = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.beejees = pygame.sprite.Group()
        self.trails = pygame.sprite.Group()
        self.bricks.add(self.left_pole)
        self.bricks.add(self.right_pole)
        for bg in range(0,20):
            brick = Brick(self, 1,1)
            brick.image = pygame.image.load(r("MappedCompassbackBluck.png")).convert_alpha()
            brick.rect = brick.image.get_rect()
            brick.rect.x = (0 + bg*brick.rect.width - bg*2)/game_scale
            brick.rect.y -= (brick.rect.height/2)/game_scale
            self.beejees.add(brick)
        self.cant_update = []

        self.catch_plat.rect.x, self.catch_plat.rect.y = self.player.rect.x, self.player.rect.y + self.player.rect.height
        self.players.add(self.player)
        self.bricks.add(self.catch_plat)

        self.times = 0
        self.player.rect.y, self.player.rect.x = self.toil.start_y, self.toil.start_x
        self.player.rect.y, self.player.rect.x = home_dir[1], home_dir[0]
        self.toil.start_y, self.toil.start_x = home_dir[1], home_dir[0]
        self.borders()
        self.listerine()
        self.predicts: Group = pygame.sprite.Group()
        for cat in range(0, self.predicts_length):
            bal: Bal = Bal(self, loom=True, screct=False)
            bal.rect.x = 0
            bal.rect.y = 0
            self.predicts.add(bal)
        self.kings = self.hides.copy()
        cat = 0
        self.hidden_areas = []
        for fresh in self.kings:
            setattr(self, f"hidden_area{cat}", fresh.spread(True))
            self.hidden_areas.append(getattr(self, f"hidden_area{cat}"))
            cat += 1
        self.run_game()
    
    def run_game(self):
        while True:
            if not self.paused:
                self.update_screen()
            else:
                self.unpause.update()
                pygame.display.flip()
            self.check_events()
            self.clock.tick(60)
    
    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)
        
    def update_screen(self):
        self.screen.fill((0, 60, 0))
        if self.visible:
            for brick in self.beejees:
                scroll_block = brick.rect.copy()
                scroll_block.x -= (self.player.scroll[0]/2)
                scroll_block.y = 0
                self.screen.blit(brick.image, scroll_block)
            for brick in self.beejees:
                scroll_block = brick.rect.copy()
                scroll_block.x -= (self.player.scroll[0]/1.5)
                scroll_block.y = 0
                self.screen.blit(brick.image, scroll_block)
            for brick in self.bricks:
                scroll_block = brick.rect.copy()
                scroll_block.x -= self.player.scroll[0]
                scroll_block.y -= self.player.scroll[1]
                self.screen.blit(brick.image, scroll_block)
        for wall in self.walls:
            wall.update()
        for tractor in self.toil.tractors:
            tractor.update()
        if self.predicting:
            points = self.player.predictive()
        else:
            points = []
        loist = []
        currnet = 0
        for bal in self.predicts:
            if currnet < len(points)-3:
                point = points[currnet]
                bal.rect.x = point[0]
                bal.rect.y = point[1]
                scroll_block = bal.rect.copy()
                scroll_block.x -= self.player.scroll[0]
                scroll_block.y -= self.player.scroll[1]
                if self.visible:
                    self.screen.blit(bal.image, scroll_block)
                loist.append(scroll_block.center)
            currnet += 1
        if self.visible:
            scroll_block = self.toil.map_surface.get_rect().copy()
            scroll_block.x -= self.player.scroll[0]
            scroll_block.y -= self.player.scroll[1]
            self.screen.blit(self.toil.map_surface, scroll_block)
        for tile in self.hides:
            tile.update()
        for tile in self.can_hit:
            if self.sword_swipe.colliderect(tile.rect):
                self.can_hit.remove(tile)
                tile.life -= 5
                # self.attack = False
                if tile.rect.x > self.player.rect.x:
                    tile.rect.x += 50
                elif tile.rect.x < self.player.rect.x:
                    tile.rect.x -= 50
                self.clock.tick(57)
                break
                # tile.kill()
        for wall in self.walls:
            if wall not in self.tiles:
                self.can_update.add(wall)
            if self.sword_swipe.colliderect(wall.spare_rect):
                wall.life -= 10
                self.sword_swipe.x = 0
                self.sword_swipe.y = 0
                self.attack = False
                self.clock.tick(57)
                break
        if pygame.sprite.groupcollide(self.evils, self.players, False, False):
            self.player.recenters()
            pass
        for enemy in self.evils:
            enemy.update()
        for player in self.players:
            player.update()
        if self.attack:
            self.swipe()
            if self.swipe_time > 5:
                self.attack = False
                self.swipe_time = 0
                self.sword_swipe.x = 0
                self.sword_swipe.y = 0
        self.unhide()
        if self.fade:
            self.apparence -= 20
        self.swipe_time += 1
        if self.traline:
            if not self.trail_stop:
                bal = Bal(self, loom=True, screct=False)
                bal.rect.topleft = self.player.rect.copy().topleft
                self.trails.add(bal)
            for bal in self.trails:
                if self.visible:
                    scroll_block = bal.rect.copy()
                    scroll_block.x -= self.player.scroll[0]
                    scroll_block.y -= self.player.scroll[1]
                    self.screen.blit(bal.image, scroll_block)
                loist.append(scroll_block.copy().center)
        if self.Φ:
            self.Φ_held += 1
        else:
            self.Φ_held = 0
        if self.linear:
            for foe in self.evils:
                if foe.mobile:
                    pygame.draw.line(self.screen, 'red', (self.player.screct.center), (foe.screct.center), 1)
            for tile in self.can_update:
                if tile.rect.centerx < self.player.rect.centerx + 128 and tile.rect.centerx > self.player.rect.centerx - 128:
                    if tile.rect.centery < self.player.rect.centery + 128 and tile.rect.centery > self.player.rect.centery - 128:
                        scroll_block = tile.rect.copy()
                        scroll_block.x -= self.player.scroll[0]
                        scroll_block.y -= self.player.scroll[1]
                        pygame.draw.line(self.screen, 'blue', (self.player.screct.center), (scroll_block.center), 1)
            for point in loist:
                pygame.draw.line(self.screen, 'green', (self.player.screct.center), point, 1)
        self.times += 1
        self.leap += 0.25
        self.frame_count()
        self.collides()

        pygame.display.flip()
    
    def collides(self):
        if pygame.sprite.spritecollide(self.player, self.toil.rgates, False):
            self.current_level[0] += 1
            self.collodes('r')
        elif pygame.sprite.spritecollide(self.player, self.toil.lgates, False):
            self.current_level[0] -= 1
            self.collodes('l')
        elif pygame.sprite.spritecollide(self.player, self.toil.ldgates, False):
            self.current_level[1] += 1
            self.collodes('ld')
        elif pygame.sprite.spritecollide(self.player, self.toil.lugates, False):
            self.current_level[1] -= 1
            self.collodes('lu')
        elif pygame.sprite.spritecollide(self.player, self.toil.rdgates, False):
            self.current_level[1] += 1
            self.collodes('rd')
        elif pygame.sprite.spritecollide(self.player, self.toil.rugates, False):
            self.current_level[1] -= 1
            self.collodes('ru')
    
    def collodes(self, dir):
        # try:
        self.toil = Toim_Chart(r(f'Chared{self.current_level[0]}_{self.current_level[1]}.tmj'), self)
        # except FileNotFoundError:
        #     self.toil = Toim_Chart(f'UTL/UTL/Chared{self.current_level[0]}_{self.current_level[1]}.csv', self)
        self.tiles = self.toil.tiles
        self.toil.start_x = getattr(self.toil, f"{dir}start_x")
        self.toil.start_y = getattr(self.toil, f"{dir}start_y")
        self.player.update(dir)
        self.player.recenters(dir)
        self.kings = self.hides.copy()
        cat = 0
        self.hidden_areas = []
        for fresh in self.kings:
            setattr(self, f"hidden_area{cat}", fresh.spread(True))
            self.hidden_areas.append(getattr(self, f"hidden_area{cat}"))
            cat += 1
        self.borders()
    
    def borders(self):
        self.cant_update.clear()
        self.can_update = pygame.sprite.Group()
        for key, value in self.toil.tile_dict.items():
            temp = [value[0] + 32, value[1]]
            temps = [value[0] - 32, value[1]]
            tem = [value[0], value[1] + 32]
            tmp = [value[0], value[1] - 32]
            if temp in self.toil.tile_dict.values() and temps in self.toil.tile_dict.values() and tem in self.toil.tile_dict.values() and tmp in self.toil.tile_dict.values():
                self.cant_update.append(key)
        for tile in self.toil.tile_dict.keys():
            if tile not in self.cant_update:
                    self.can_update.add(tile)
    
    def parab(self):
        self.player.points = []
        for x in range(-9, 8, 1):
            y = (x**2+2*x+2)*1.25
            self.player.points.append(y)
        for num in range(0, 8):
            self.player.points[num] = -abs(self.player.points[num])
        self.player.points.remove(1.25)
        self.player.points.remove(2.5)
        self.player.points.remove(-2.5)
        self.player.points.remove(6.25)
        self.player.points.remove(-6.25)
    
    def swipe(self):
        if self.player.dir:
            self.sword_swipe.left = self.player.rect.right-10
        elif not self.player.dir:
            self.sword_swipe.right = self.player.rect.left+10
        else:
            self.sword_swipe.centerx = self.player.rect.right
        self.sword_swipe.centery = self.player.rect.centery
        scroll_block = self.sword_swipe.copy()
        scroll_block.x -= self.player.scroll[0]
        scroll_block.y -= self.player.scroll[1]
        image = self.sword[self.swipe_time%len(self.sword)]
        if not self.player.dir:
            image = pygame.transform.flip(image, True, False)
        self.screen.blit(image, scroll_block)
    
    def check_events(self):
        for event in pygame.event.get():
            if not self.paused:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        try:
                            self.level = open("LEVEL.txt", 'w')
                        except FileNotFoundError:
                            self.level = open("UTL/UTL/LEVEL.txt", 'w')
                        self.level.write(f"{self.current_level[0]}\n")
                        self.level.write(f"{self.current_level[1]}\n")
                        self.level.write(f"{int(self.toil.start_x)}\n{int(self.toil.start_y)}")
                        self.level.close()
                        with open(r("Relevents1.pickle"), 'wb') as file:
                            pickle.dump(self.full_run, file)
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_j:
                        self.foe_reset()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.player.air_time < 5:
                            self.parab()
                            self.player.up = True
                            self.player.in_air = True
                            self.player.jump_x = 0
                            self.leap = 0
                        else:
                            self.jump_hold = True
                        self.player.up_timer = 0
                    if event.key == pygame.K_DOWN:
                        self.player.gravitate = True
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.left = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.right = True
                    if event.key == pygame.K_SPACE and self.swipe_time > 15 and not self.Φ:
                        self.attack = True
                        self.can_hit = self.evils.copy()
                        self.swipe_time = 0
                        self.Φ = True
                    if event.key == pygame.K_r:
                        self.player.recenters()
                    if event.key == pygame.K_t:
                        self.traline = True
                        self.trail_stop = False
                        self.trails = pygame.sprite.Group()
                    if event.key == pygame.K_y:
                        self.traline = False
                        self.trail_stop = True
                        self.trails = pygame.sprite.Group()
                    if event.key == pygame.K_n:
                        self.red = open("Start_clause.txt.txt", 'w')
                        self.red.close()
                    if event.key == pygame.K_l:
                        if self.linear:
                            self.linear = False
                        else:
                            self.linear = True
                    if event.key == pygame.K_u:
                        if self.trail_stop:
                            self.trail_stop = False
                        else:
                            self.trail_stop = True
                    if event.key == pygame.K_p:
                        if self.predicting:
                            self.predicting = False
                        else:
                            self.predicting = True
                    if event.key == pygame.K_v:
                        if self.visible:
                            self.visible = False
                        else:
                            self.visible = True
                    if event.key == pygame.K_ESCAPE and not self.stick:
                        if self.paused:
                            self.paused = False
                        elif not self.paused:
                            self.paused = True
                    else:
                        self.stick = False
                    for cat in range(0,10):
                        if event.key == getattr(pygame, f"K_{cat}"):
                            self.player.max_speed = cat
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.left = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.right = False
                    if event.key == pygame.K_DOWN:
                        self.player.gravitate = False
                    if event.key == pygame.K_UP:
                        if self.player.down_vel < -2 and self.gravity > 0:
                            self.player.down_vel = 0
                    if event.key == pygame.K_SPACE:
                        self.Φ = False
                elif self.joystick:
                    if self.joystick.get_axis(0) < -0.1:
                        self.player.left = True
                        self.player.right = False
                    elif self.joystick.get_axis(0) > 0.1:
                        self.player.right = True
                        self.player.left = False
                    else:
                        self.player.right = False
                        self.player.left = False
                    if self.joystick.get_button(0) and not self.x_pressed:
                        if self.player.air_time < 5:
                            self.parab()
                            self.player.up = True
                            self.player.in_air = True
                            self.player.jump_x = 0
                            self.leap = 0
                        else:
                            self.jump_hold = True
                        self.x_pressed = True
                        self.player.up_timer = 0
                    if not self.joystick.get_button(0) and self.x_pressed != self.joystick.get_button(0):
                        self.x_pressed = False
                        if self.player.down_vel < -2 and self.gravity > 0:
                            self.player.down_vel = 0
                    if self.joystick.get_button(2) and self.swipe_time > 15 and not self.Φ:
                        self.attack = True
                        self.can_hit = self.evils.copy()
                        self.swipe_time = 0
                        self.Φ = True
                    elif not self.joystick.get_button(2):
                        self.Φ = False
                        if self.Φ_held > 200:
                            for foe in self.evils:
                                foe.life -= 100
                    if self.joystick.get_button(6) and not self.stick:
                        if self.paused:
                            self.paused = False
                        elif not self.paused:
                            self.paused = True
                        self.stick = True
                    if not self.joystick.get_button(6):
                        self.stick = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not self.stick:
                        if self.paused:
                            self.paused = False
                        elif not self.paused:
                            self.paused = True
                    else:
                        self.stick = False
                if self.joystick:
                    if self.joystick.get_button(6) and not self.stick:
                        if self.paused:
                            self.paused = False
                        elif not self.paused:
                            self.paused = True
                        self.stick = True
                    if not self.joystick.get_button(6):
                        self.stick = False
                if pygame.mouse.get_pressed()[0]:
                    if self.unpause.rect.collidepoint(pygame.mouse.get_pos()):
                        self.paused = False
        if self.player.up_timer > 7:
            self.jump_hold = False 
        if self.jump_hold: 
            if not self.player.in_air:
                self.player.up = True
            else:
                self.player.up = False
                
            
    def placey(self):
        if self.clickage:
            platform = Brick(self, self.brick_width/game_scale, self.brick_height/game_scale)
            platform.rect.x = self.player.rect.x
            platform.rect.y = self.player.rect.y+self.player.rect.height
            platform.update()
            if pygame.sprite.spritecollide(platform, self.bricks, False):
                platform.kill()
            else:
                self.bricks.add(platform)
    
    def listerine(self,image="See_Through.png", scalx=32, scaly=32):
        lost = []
        rect = pygame.rect.Rect(0,0,scalx,scaly)
        imoge = pygame.image.load(r(image))
        for cat in range(imoge.get_height()//scaly):
            for fish in range(imoge.get_width()//scalx):
                rect.x = fish*scalx
                rect.y = cat*scaly
                sub = imoge.subsurface(rect)
                new_image = pygame.Surface((scalx,scaly))
                new_image.blit(sub, (0,0))
                new_image.set_colorkey((0,0,0))
                lost.append(new_image)
        return(lost)
    
            
    def frame_count(self):
        self.colourWHITE = (250,250,250)
        if float(self.timer) < self.player.down_vel:
            self.timer = str(self.player.down_vel)
        myFont = pygame.font.SysFont('none', 40)
        self.counter = myFont.render(self.timer, False, self.colourWHITE, (0,0,0))
        self.counterect = self.counter.get_rect()
        self.screen.blit(self.counter, (0,0))

    def unhide(self):
        if len(self.hidden_areas) > 0:
            for area in self.hidden_areas:
                for boo in area:
                    if self.player.rect.colliderect(boo):
                        for boo in area:
                            boo.fading = True
    
    def foe_reset(self):
        for key in self.full_run.keys():
            if "foe" in key:
                self.full_run[key] = True
                print(key)


class Player(Sprite):
    """Makes the player for game 2"""

    def __init__(self, loom=Yarn):
        super().__init__()
        self.loom: Yarn = loom
        self.screen: pygame.Surface = self.loom.screen
        self.screen_width = self.loom.screen_width
        self.screen_height = self.loom.screen_height
        self.up_timer = 0
        self.down_timer = 0
        self.jump_x = 0
        self.collie = 0
        self.air_time = 0
        self.max_speed = 6
        self.gravitate = True
        self.in_air = False
        self.recenter = False
        self.coll = False
        self.screct = False
        self.dir = False
        self.cling = False
        self.clinging = False
        self.richtig = 10
        self.left_cling = False
        self.right_cling = False

        self.scroll = [32, 0]
        self.movement = []
        self.points = []

        # New
        self.down_vel = 0

        # Movement flags
        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.scales = 32
        self.image = pygame.image.load(r("Marble.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.scales,48))
        self.imag = pygame.image.load(r("Foe.pnh.png")).convert_alpha()
        self.imag = pygame.transform.scale(self.imag, (self.scales,48))
        self.ima = pygame.image.load(r("Marble.png")).convert_alpha()
        self.ima = pygame.transform.scale(self.ima, (self.scales,48))
        self.rect = self.image.get_rect()

    def update(self, level=''):
        if pygame.sprite.spritecollide(self, self.loom.toil.tractors, False):
            self.loom.gravity = -0.1
            if self.down_vel > 5:
                self.down_vel = 0
            self.down = False
        else:
            self.loom.gravity = self.loom.base_gravity
        self.scroll_stops()
        self.movement = [0,0]

        if self.down_vel+self.loom.gravity < 43:
            self.down_vel += self.loom.gravity

        self.motion()

        self.level_scroll(level)

        player_scroll_rect = self.rect.copy()
        player_scroll_rect.x -= self.scroll[0]
        player_scroll_rect.y -= self.scroll[1]
        self.screct = player_scroll_rect
        self.screen.blit(self.image, player_scroll_rect)
        
        self.up_timer += 1
        self.air_time += 1
        self.richtig += 1
        if self.right:
            self.dir = True
        elif self.left:
            self.dir = False
    
    def recenters(self, dir=''):
        self.rect.x = getattr(self.loom.toil, f'{dir}start_x')
        self.rect.y = getattr(self.loom.toil, f'{dir}start_y')
        self.level = open("LEVEL.txt", 'w')
        self.level.write(f"{self.loom.current_level[0]}\n")
        self.level.write(f"{self.loom.current_level[1]}\n")
        self.level.write(f"{int(self.loom.toil.start_x)}\n{int(self.loom.toil.start_y)}")
        self.level.close()
        self.down_timer = 0
        self.down_vel = 0
        self.up, self.down, self.right, self.left = False, False, False, False
    
    def scroll_stops(self):
        """Does both the scroll stopping and the slow snap to the sides of the map."""
        # Stops for x adjustments
        if (self.rect.left - 32) - (self.screen_width/2) > self.screen.get_rect().left and (self.rect.centerx + 32) + (self.screen_width/2) - 16 < self.loom.toil.map_surface.get_rect().right:
            self.scroll[0] += (self.rect.x - self.scroll[0] - (self.screen_width/2))//3
        # Snaps to the right
        elif self.rect.centerx + (self.screen_width/2) > self.loom.toil.map_surface.get_rect().right and (self.rect.left - 32) - (self.screen_width/2) > self.screen.get_rect().left:
            if self.scroll[0] < self.loom.toil.map_surface.get_rect().right - (self.screen_width+32):
                self.scroll[0] += 1
            elif self.scroll[0] > self.loom.toil.map_surface.get_rect().right - (self.screen_width+32):
                self.scroll[0] -= 1
        # Snaps to the left
        elif self.rect.centerx - (self.screen_width/2) < self.loom.toil.map_surface.get_rect().left and (self.rect.centerx + 32) + (self.screen_width/2) - 16 < self.loom.toil.map_surface.get_rect().right:
            if self.scroll[0] > 32:
                self.scroll[0] -= 1
            elif self.scroll[0] < 32:
                self.scroll[0] += 1
        # Stops for y adjustments
        if (self.rect.y) > self.screen.get_rect().top+24+(self.screen_height/2) and self.rect.bottom < self.loom.toil.map_surface.get_rect().bottom+20-(self.screen_height/2):
            self.scroll[1] += (self.rect.y - self.scroll[1] - (self.screen_height/2))//3
        # Snaps to the bottom
        elif self.rect.centery + (self.screen_height/2) > self.loom.toil.map_surface.get_rect().bottom and (self.rect.y) > self.screen.get_rect().top+24+(self.screen_height/2):
            if self.scroll[1] < self.loom.toil.map_surface.get_rect().bottom - (self.screen_height+32):
                self.scroll[1] += 1
            elif self.scroll[1] > self.loom.toil.map_surface.get_rect().bottom - (self.screen_height+32):
                self.scroll[1] -= 1
        # Snaps to the top
        elif self.rect.centery - (self.screen_height/2) < self.loom.toil.map_surface.get_rect().top and self.rect.bottom < self.loom.toil.map_surface.get_rect().bottom+20-(self.screen_height/2):
            if self.scroll[1] > 32:
                self.scroll[1] -= 1
            elif self.scroll[1] < 32:
                self.scroll[1] += 1
    
    def level_scroll(self, level: str):
        """Enacts appropriate scroll adjustments for level changes."""
        if level == 'r':
            self.scroll[0] = 0 + 32
            self.scroll[1] = self.loom.toil.start_y - (self.screen_height-96)#(self.loom.toil.map_surface.get_rect().height - self.loom.toil.start_y + 64)# + self.screen_height/2
            if self.scroll[1]+(self.screen_height/2)<0:
                self.scroll[1] = 32
        elif level == 'l':
            self.scroll[0] = self.loom.toil.map_surface.get_rect().width - self.screen_width - 32
            self.scroll[1] = self.loom.toil.start_y - (self.screen_height-96)#self.loom.toil.map_surface.get_rect().height - self.loom.toil.start_y + 64
            if self.scroll[1]+(self.screen_height/2)<0:
                self.scroll[1] = 32
        elif level == 'ld':
            self.scroll[1] = 0 + 32
            self.scroll[0] = 0 + 32
        elif level == 'rd':
            self.scroll[1] = 0 + 32
            self.scroll[0] = self.loom.toil.map_surface.get_rect().width - self.screen_width - 32
        elif level == 'lu':
            self.scroll[1] = self.loom.toil.map_surface.get_rect().height - self.screen_height - 32
            self.scroll[0] = 0 + 32
        elif level == 'ru':
            self.scroll[1] = self.loom.toil.map_surface.get_rect().height - self.screen_height - 32
            self.scroll[0] = 0 + 32

    def motion(self):
        """Runs both motion commands for ease of reading"""
        self.calculate_motion()
        self.do_motion()

    def calculate_motion(self):
        """Does the calculation for motion"""
        if not self.loom.joystick:
            if self.right:
                self.movement[0] += self.max_speed
            if self.left:
                self.movement[0] -= self.max_speed
        else:
            if self.right:
                self.movement[0] += round((self.loom.joystick.get_axis(0))*self.max_speed)
            elif self.left:
                self.movement[0] += round((self.loom.joystick.get_axis(0))*self.max_speed)
        if self.richtig < 10:
            self.movement[0] = 0
            if self.left_cling:
                self.movement[0] += 4
            elif self.right_cling:
                self.movement[0] -= 4
        else:
            self.left_cling = False
            self.right_cling = False
        if self.up:
            self.down_vel = -13
            self.up = False

    def do_motion(self):
        """Conducts actual motion and primarily corrects for brick intersection"""
        self.rect.x += self.movement[0]
        self.wall_hop = False
        while pygame.sprite.groupcollide(self.loom.can_update, self.loom.players, False, False) or pygame.sprite.groupcollide(self.loom.walls, self.loom.players, False, False):
            if self.movement[0] > 0:
                self.rect.x -= 1
            else:
                self.rect.x += 1
            if self.in_air:
                if self.down_vel > 4:
                    self.down_vel = 4
                    # self.wall_hop = True
                    self.cling = True
        self.rect.y += self.down_vel
        collide = pygame.sprite.groupcollide(self.loom.can_update, self.loom.players, False, False)
        if collide:
            while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                    cat = pygame.sprite.spritecollide(self, self.loom.can_update, False)
                    if self.rect.y < cat[0].rect.y:
                        self.rect.y -= 1
                        self.in_air = False
                        self.cling = False
                        self.air_time = 0
                        # self.image = self.ima
                    else:
                        self.rect.y += 1
        else:
            self.in_air = True
            # self.image = self.imag
        self.cling_calc()
        if self.wall_hop == True:
            self.in_air = False
        if collide:
            self.down_vel = 0
        self.collie = len(collide.keys())
    
    def cling_calc(self):
        if self.cling:
            self.clinging = False
            for tile in self.loom.can_update:
                if tile.rect.collidepoint((self.rect.left-2,self.rect.y)):
                    self.left_cling = True
                    self.clinging = True
                elif tile.rect.collidepoint((self.rect.left-2,self.rect.bottom)):
                    self.left_cling = True
                    self.clinging = True
                elif tile.rect.collidepoint((self.rect.left-2,self.rect.centery)):
                    self.left_cling = True
                    self.clinging = True
                elif tile.rect.collidepoint((self.rect.right+2, self.rect.y)):
                    self.right_cling= True
                    self.clinging = True
                elif tile.rect.collidepoint((self.rect.right+2, self.rect.bottom)):
                    self.right_cling= True
                    self.clinging = True
                elif tile.rect.collidepoint((self.rect.right+2, self.rect.centery)):
                    self.right_cling= True
                    self.clinging = True
            if not self.clinging:
                self.cling = False
            else:
                if self.down_vel > 2:
                    self.down_vel = 4
                    self.wall_hop = True
            if self.down_vel < 1:
                self.richtig = 0
    
    def predictive(self):
        if self.in_air and self.loom.times%3 == 0:
            if self.movement[0] > 0:
                current_x = self.rect.right
            else:
                current_x = self.rect.left
            current_y = self.rect.centery
            current_vel = self.down_vel
            speed = self.movement[0]
            self.point_list = []
            ying = True
            for cat in range(0,self.loom.predicts_length):
                if cat % 3 == 0:
                    self.point_list.append([current_x,current_y])
                current_x += speed
                if ying:
                    current_y += current_vel
                if self.down_vel != 0 or self.in_air:
                    current_vel += self.loom.gravity
                if self.movement[0] == 0 and not self.in_air:
                    current_y = self.rect.y
                if cat % 3 == 0:
                    if len(self.point_list) > 0:
                        for rect in self.loom.can_update:
                            if rect.rect.collidepoint(self.point_list[-1]):
                                # return point_list
                                if rect.rect.y > self.rect.centery:
                                    current_y = rect.rect.y - 48
                                    # if self.movement[0] > 0:
                                    #     current_x -= 10
                                    # else:
                                    #     current_x += 10
                                    ying = False
                                    for cat in range(1,3):
                                        if len(self.point_list) > 0:
                                            self.point_list[-cat][1] = current_y
                                        else:
                                            break
                                else:
                                    ying = True
                                    self.point_list.remove(self.point_list[-1])
                                    return(self.point_list)
                                break
        elif self.in_air:
            return self.point_list
        else:
            self.point_list = []
        return self.point_list

class Base_Foe(Sprite):
    """Attempts to create a basic template for an enemy"""

    def __init__(self, loom: Yarn, x=0, y=0, level_point=0, width=32, height=32, image="Enemy1.png"):
        super().__init__()
        self.loom = loom
        self.level_point = level_point
        self.up = False
        self.motion = [0,0]
        self.down_vel = 0
        self.in_air = False
        self.screen = self.loom.screen
        self.image = pygame.image.load(r(image)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width,height))
        self.blit_image = self.image
        self.rect = self.image.get_rect()
        self.right = False
        self.left = True
        self.horizontal = 2
        self.can_jump = False
        self.floor_turn = False
        self.jump_height = 18
        self.switchx = [20,25] 
        self.proximity = 640
        self.life = 20
        self.rect.x = x
        self.rect.y = y
        self.screct = self.rect.copy()
        self.mobile = False

    def basics(self):
        self.motion = [0,0]
        if self.down_vel+self.loom.gravity < 43:
            self.down_vel += self.loom.gravity
        if self.loom.player.rect.x > self.rect.x - self.proximity and self.loom.player.rect.x < self.rect.x + self.proximity:
            self.motions()
            self.x_move()
            if self.can_jump:
                self.y_move_up()
            else:
                self.y_move()
            if self.floor_turn:
                self.safe_turn()
            self.mobile = True
        else:
            self.mobile = False
        if self.life < 1:
            self.kill()
            self.loom.full_run[self.level_point] = False
        self.show()

    def motions(self):
        if self.left:
            self.motion[0] -= self.horizontal
        elif self.right:
            self.motion[0] += self.horizontal
        if self.up:
            if self.can_jump:
                self.down_vel = -self.jump_height
            self.up = False
    
    def show(self):
        scroll_block = self.rect.copy()
        scroll_block.x -= self.loom.player.scroll[0]
        scroll_block.y -= self.loom.player.scroll[1]
        self.screct = scroll_block.copy()
        if self.motion[0] < 0:
            self.blit_image = pygame.transform.flip(self.image, True, False)
        else:
            self.blit_image = self.image
        if self.loom.visible:
            self.screen.blit(self.blit_image, scroll_block)

    
    def y_move_up(self):
        if self.rect.top > self.loom.player.rect.bottom and self.in_air == False and self.loom.times % random.randint(1,30) == 0:
            self.up = True
            for tile in self.loom.can_update:
                if tile.rect.collidepoint(self.rect.x, self.rect.y-50) or tile.rect.collidepoint(self.rect.right, self.rect.y-50):
                    self.up = False
                    break
        self.rect.y += self.down_vel
        if pygame.sprite.spritecollide(self, self.loom.can_update, False):
            if self.down_vel < 0:
                while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                    self.rect.y += 1
                self.rect.y += 1
            elif self.down_vel > 0:
                while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                    self.rect.y -= 1
                self.in_air = False
            self.down_vel = 0
        else:
            self.in_air = True
    
    def y_move(self):
        self.rect.y += self.down_vel
        if pygame.sprite.spritecollide(self, self.loom.can_update, False):
            while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                self.rect.y -= 1
            self.in_air = False
            self.down_vel = 0
        else:
            self.in_air = True
    
    def x_move(self):
        if self.loom.times % random.randint(self.switchx[0],self.switchx[1]) == 0:
            if self.rect.centerx < self.loom.player.rect.centerx:
                self.right = True
                self.left = False
            else:
                self.left = True
                self.right = False
        self.rect.x += self.motion[0]
        if pygame.sprite.spritecollide(self, self.loom.can_update, False):
            if self.left:
                self.left = False
                self.right = True
                while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                    self.rect.x += 1
                self.rect.x += 1
            elif self.right:
                self.right = False
                self.left = True
                while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                    self.rect.x -= 1
                self.rect.x -= 1
    
    def safe_turn(self):
        colleftded = False
        corrighted = False
        for tile in self.loom.can_update:
            if tile.rect.collidepoint(((self.rect.left),(self.rect.bottom+10))):
                colleftded = True
            if tile.rect.collidepoint(((self.rect.right),(self.rect.bottom+10))):
                corrighted = True
        if not colleftded or not corrighted:
            if self.left:
                self.left = False
                self.right = True
            elif self.right:
                self.left = True
                self.right = False

    def listerine(self, sheet="EnemySheet.png", width=32, height=32):
        lost = []
        rect = pygame.rect.Rect(0,0,width,height)
        imoge = pygame.image.load(r(sheet))
        for cat in range(imoge.get_height()//height):
            for fish in range(imoge.get_width()//width):
                rect.x = fish*width
                rect.y = cat*height
                sub = imoge.subsurface(rect)
                new_image = pygame.Surface((width,height))
                new_image.blit(sub, (0,0))
                new_image.set_colorkey((0,0,0))
                lost.append(pygame.transform.scale(new_image, (self.rect.width,self.rect.height)))
        return lost

class Toil(Sprite):
    """Tries to make a tile."""

    def __init__(self, image, x, y, dex, ful, loom: Yarn, started: bool=True):
        """Initialises everything"""
        super().__init__()
        self.loom = loom
        self.type = image
        self.image = pygame.image.load(r(f"{image}"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        if not started:
            percente = dex/ful
            percente = percente*100
            screen.fill((0,percente*2,percente))
            screen.blit(pygame.transform.scale(pygame.image.load(r("MonsterBrickKindLoad.png")), (1280,720)).convert_alpha(), screen.get_rect())
            pygame.display.flip()
    
    def draw(self, surface, num=0):
        # if not self.type == "Half_Blue.png":
        #     self.image.fill((0, (num%100)+1, (num%100)+1))
        self.image.blit(pygame.image.load(r(f"{self.type}")), self.image.get_rect())
        self.image = self.image
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

class Trouble(Toil):
    """Attempts a pre-imaged tile."""

    def __init__(self, image, x, y, dex, ful, loom=Yarn, started=True):
        super().__init__("See_through.png", x, y, dex, ful, loom=loom, started=started)
        self.image = image
    
    def draw(self, surface, num=0):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Toim_Chart:
    """Makes the tile map"""

    def __init__(self, filename, loom: Yarn, started=True):
        """Initialises everything"""
        self.tile_size = 64/game_scale
        self.loom = loom
        self.started = started
        for tile in self.loom.evils:
            tile.kill()
        for tile in self.loom.walls:
            tile.kill()
        self.tractors = []
        for tractor in self.tractors:
            tractor.kill()
        for hide in self.loom.hides:
            hide.kill()
            self.loom.hides = []
        self.start_x = 0
        self.start_y = 0
        self.lstart_x = 0
        self.lstart_y = 0
        self.rstart_x = 0
        self.rstart_y = 0
        self.lustart_x = 0
        self.rustart_y = 0
        self.ldstart_x = 0
        self.rdstart_y = 0
        self.rgates = pygame.sprite.Group()
        self.lgates = pygame.sprite.Group()
        self.lugates = pygame.sprite.Group()
        self.ldgates = pygame.sprite.Group()
        self.rugates = pygame.sprite.Group()
        self.rdgates = pygame.sprite.Group()
        self.gates = pygame.sprite.Group()
        self.evils = pygame.sprite.Group()
        self.tiles = self.load_tiles(filename)
        self.tile_dict = {}
        for tile in self.tiles:
            self.tile_dict[tile] = [tile.rect.x, tile.rect.y]
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        for toil in self.tiles:
            toil.draw(self.map_surface, self.tiles.index(toil))
        self.tile = pygame.sprite.Group()
        self.beams = pygame.sprite.Group()
        for cat in self.tiles:
            self.tile.add(cat)
        for beam in self.tractors:
            self.beams.add(beam)
        self.tiles = self.tile
        self.tractors = self.beams
    
    def update(self, screen):
        screen.blit(self.map_surface, (0,0))
    
    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = json.load(data)#, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def read_json(self, filename):
        map: list[list] = []
        with open(os.path.join(filename)) as data:
            diction = dict(json.load(data))
            data = diction['layers'][0]['data']
            height = int(diction['layers'][0]['height'])
            length = int(diction['layers'][0]['width'])
            for cat in range(0, height):
                map.append(list(data[cat*length:(cat*length)+length]))
            # for row in data:
            #     map.append(list(row))
        with open("Cheque.txt", 'w') as pay:
            for row in map:
                pay.write(f"{str(row)}\n")
        return map

    def listerine(self, sheet="EnemySheet.png", width=32, height=32):
        lost = []
        rect = pygame.rect.Rect(0,0,width,height)
        imoge = pygame.image.load(r(sheet))
        for cat in range(imoge.get_height()//height):
            for fish in range(imoge.get_width()//width):
                rect.x = fish*width
                rect.y = cat*height
                sub = imoge.subsurface(rect)
                new_image = pygame.Surface((width,height))
                new_image.blit(sub, (0,0))
                new_image.set_colorkey((0,0,0))
                lost.append(new_image)
        return lost

# 7 = Up
# 10 = Left
# 5 = Left Down
# 6 = Left Right
# 17 = Right Up
# 18 = Right Down


    def load_tiles(self, filename):
        self.tiles = []
        map = self.read_json(filename)
        foe_count = 1
        wall_count = 1
        hide_count = 1
        self.points = []
        x_count = 0
        y_count = 0
        x,y = 0,0
        grax = self.listerine("sprite-0003.png", width=32, height=32)
        for row in map:
            x = 0
            for tile in row:
                tile = str(int(tile)-1)
                if tile == '-1':
                    self.points.append((x*self.tile_size, y*self.tile_size))
                elif tile == '0':
                    self.tiles.append(Toil('grazz.png', x * self.tile_size, y * self.tile_size, dex=y, ful=len(map)+1, loom=self.loom, started=self.started))
                elif tile == '2':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                    x_count, y_count = x * self.tile_size, y * self.tile_size
                elif tile == '5':
                    new_tile = Toil('Verical_No_See.png', x * self.tile_size, y * self.tile_size, dex=y, ful=len(map)+1, loom=self.loom, started=self.started)
                    self.ldgates.add(new_tile)
                elif tile == '6':
                    new_tile = Toil('Horizontal_No_See.png', x * self.tile_size, y * self.tile_size, dex=y, ful=len(map)+1, loom=self.loom, started=self.started)
                    self.rgates.add(new_tile)
                elif tile == '7':
                    new_tile = Toil('Verical_No_See.png', x * self.tile_size, y * self.tile_size, dex=y, ful=len(map)+1, loom=self.loom, started=self.started)
                    self.lugates.add(new_tile)
                elif tile == '10':
                    new_tile = Toil('Horizontal_No_See.png', x * self.tile_size, y * self.tile_size, dex=y, ful=len(map)+1, loom=self.loom, started=self.started)
                    self.lgates.add(new_tile)
                elif tile == '11':
                    self.lstart_x, self.lstart_y = x * self.tile_size, y * self.tile_size
                elif tile == '12':
                    self.rstart_x, self.rstart_y = x * self.tile_size, y * self.tile_size
                elif tile == '13':
                    self.lustart_x, self.lustart_y = x * self.tile_size, y * self.tile_size
                elif tile == '14':
                    self.ldstart_x, self.ldstart_y = x * self.tile_size, y * self.tile_size
                elif tile == '15':
                    self.rustart_x, self.rustart_y = x * self.tile_size, y * self.tile_size
                elif tile == '16':
                    self.rdstart_x, self.rdstart_y = x * self.tile_size, y * self.tile_size
                elif tile == '17':
                    new_tile = Toil('Verical_No_See.png', x * self.tile_size, y * self.tile_size, dex=y, ful=len(map)+1, loom=self.loom, started=self.started)
                    self.rdgates.add(new_tile)
                elif tile == '18':
                    new_tile = Toil('Verical_No_See.png', x * self.tile_size, y * self.tile_size, dex=y, ful=len(map)+1, loom=self.loom, started=self.started)
                    self.rugates.add(new_tile)
                elif tile == '19':
                    tractor = Tractor(96, (len(map))*32, x*self.tile_size, y*self.tile_size, self.loom)#41
                    self.tractors.append(tractor)
                    self.points.append((x*self.tile_size, y*self.tile_size))
                elif tile == '20':
                    attimpt = f"foe{self.loom.current_level[0]}_{self.loom.current_level[1]}_{foe_count}"
                    if attimpt in self.loom.full_run.keys():
                        if self.loom.full_run[attimpt]:
                            foe = Smart_Goblin(self.loom, x*self.tile_size, y*self.tile_size, attimpt)
                            self.loom.evils.add(foe)
                    foe_count += 1
                elif tile == '21':
                    attimpt = f"wall{self.loom.current_level[0]}_{self.loom.current_level[1]}_{wall_count}"
                    if attimpt in self.loom.full_run.keys():
                        if self.loom.full_run[attimpt]:
                            wall = Wall(x*self.tile_size, y *self.tile_size, self.loom, level_point=attimpt)
                            self.loom.walls.add(wall)
                    wall_count += 1
                elif tile == '22':
                    attimpt = f"wall{self.loom.current_level[0]}_{self.loom.current_level[1]}_{wall_count}"
                    if attimpt in self.loom.full_run.keys():
                        if self.loom.full_run[attimpt]:
                            wall = Wall(x*self.tile_size, y *self.tile_size, self.loom, True, level_point=attimpt)
                            self.loom.walls.add(wall)
                    wall_count += 1
                elif tile == '23':
                    attimpt = f"hide{self.loom.current_level[0]}_{self.loom.current_level[1]}_{hide_count}"
                    if attimpt in self.loom.full_run.keys():
                        if self.loom.full_run[attimpt]:
                            self.loom.hides.append(Hidden(x * self.tile_size, y * self.tile_size, loom=self.loom, dex=y, ful=len(map)+1, started=self.started, level_point=attimpt))
                    hide_count += 1
                elif int(tile) in range(25,68):
                    self.tiles.append(Trouble(grax[int(tile)-25], x * self.tile_size, y * self.tile_size, dex=y, ful=len(map)+1, started=self.started))
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return self.tiles

class Hidden(Toil):
    """Creates a hidden space."""

    def __init__(self, x, y, dex, ful, loom=Yarn, started=True, level_point=0):
        image = 'See_Through.png'
        super().__init__(image, x, y, dex, ful, loom, started)
        self.started = started
        self.level_point = level_point
        self.image.fill((0,3,0))
        self.apparence = 1000
        self.dex = 10
        self.fading = False
        self.loist = []
    
    def spread(self, hive_king=False):
        pupae = 0
        if hive_king:
            others = self.loom.hides.copy()
            hive = []
        if (self.rect.x-32, self.rect.y) in self.loom.toil.points:
            pupil = (Hidden(self.rect.x-32, self.rect.y, loom=self.loom, dex=self.dex, ful=10, started=self.started))
            self.loom.hides.append(pupil)
            self.loist.append(pupil)
            self.loom.toil.points.remove((self.rect.x-32, self.rect.y))
            pupae += 1
        if (self.rect.x, self.rect.y-32) in self.loom.toil.points:
            pupal = (Hidden(self.rect.x, self.rect.y-32, loom=self.loom, dex=self.dex, ful=10, started=self.started))
            self.loom.hides.append(pupal)
            self.loist.append(pupal)
            self.loom.toil.points.remove((self.rect.x, self.rect.y-32))
            pupae += 1
        if (self.rect.x+32, self.rect.y) in self.loom.toil.points:
            pupol = (Hidden(self.rect.x+32, self.rect.y, loom=self.loom, dex=self.dex, ful=10, started=self.started))
            self.loom.hides.append(pupol)
            self.loist.append(pupol)
            self.loom.toil.points.remove((self.rect.x+32, self.rect.y))
            pupae += 1
        if (self.rect.x, self.rect.y+32) in self.loom.toil.points:
            pupel = (Hidden(self.rect.x, self.rect.y+32, loom=self.loom, dex=self.dex, ful=10, started=self.started))
            self.loom.hides.append(pupel)
            self.loist.append(pupel)
            self.loom.toil.points.remove((self.rect.x, self.rect.y+32))
            pupae += 1
        for grad in self.loist:
            grad.spread()
        if hive_king:
            for new in self.loom.hides:
                if new not in others:
                    hive.append(new)
            hive.append(self)
        if hive_king:
            return hive

    def update(self):
        if self.apparence > 0:
            if self.fading:
                self.apparence -= 20
            scroll_block = self.rect.copy()
            scroll_block.x -= self.loom.player.scroll[0]
            scroll_block.y -= self.loom.player.scroll[1]
            self.blit_alpha(self.loom.screen, self.image, scroll_block, self.apparence)
        elif self.level_point != 0:
            self.loom.full_run[self.level_point] = False

class Wall(Sprite):
    """Creates a breakable wall."""

    def __init__(self, x, y, loom=Yarn, rightward=False, level_point=0):
        super().__init__()
        self.loom = loom
        self.level_point = level_point
        self.screen = self.loom.screen
        self.image = pygame.image.load(r("RightBreakable.png"))
        if rightward:
            self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.spare_rect = pygame.rect.Rect(x,y,self.rect.width/2,self.rect.height)
        self.rect.x = x
        self.rect.y = y
        self.life = 50
        if not rightward:
            self.spare_rect.x += self.rect.width/2
    
    def update(self):
        if self.life < 1:
            self.kill()
            self.loom.full_run.pop(self.level_point)
        scroll_block = self.rect.copy()
        scroll_block.x -= self.loom.player.scroll[0]
        scroll_block.y -= self.loom.player.scroll[1]
        scrill_block = self.spare_rect.copy()
        scrill_block.x -= self.loom.player.scroll[0]
        scrill_block.y -= self.loom.player.scroll[1]
        self.screen.blit(self.image, scroll_block)

class Tractor(Sprite):
    """Creates the tractor beams."""

    def __init__(self, width, height, x, y, loom=Yarn):
        super().__init__()
        self.loom = loom
        self.screen = self.loom.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load(r("Half_Blue.png"))
        self.image = pygame.transform.scale(self.image, (width,height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        scroll_block = self.rect.copy()
        scroll_block.x -= self.loom.player.scroll[0]
        scroll_block.y -= self.loom.player.scroll[1]
        self.screen.blit(self.image, scroll_block)
        self.screen.blit(self.image, scroll_block)
        self.screen.blit(self.image, scroll_block)

class Goblin(Base_Foe):
    """Creates those green chaps"""

    def __init__(self, loom=Yarn, x=0, y=0, level_point=0):
        super().__init__(loom, x, y, level_point, 32, 32)
        self.lost = self.listerine("EnemySheet.png", 32, 32)
    
    def update(self):
        self.image = self.lost[round((self.loom.times / 8) % 6)]
        self.basics()

class Jump_Goblin(Base_Foe):
    """Creates jumping green chaps"""

    def __init__(self, loom=Yarn, x=0, y=0, level_point=0):
        super().__init__(loom, x, y, level_point, 32, 32)
        self.lost = self.listerine("EnemySheet.png", 32, 32)
        self.can_jump = True
        self.jump_height = 13
    
    def update(self):
        self.image = self.lost[round((self.loom.times / 8) % 6)]
        self.basics()

class Smart_Goblin(Base_Foe):
    """Creates a green chap to jump a gap"""

    def __init__(self, loom=Yarn, x=0, y=0, level_point=0):
        super().__init__(loom, x, y, level_point, 32, 32)
        self.lost = self.listerine("Sprite-0001-sheet.png", 16, 16)
        self.can_jump = True
        self.jump_height = 13
    
    def update(self):
        self.image: pygame.surface.Surface = self.lost[round((self.loom.times / 8) % 6)]
        self.basics()
    
    def y_move_up(self):
        if self.loom.times%5 == 0:
            colleftded = False
            corrighted = False
            turned = False
            if not self.in_air:# and not self.up:
                for tile in self.loom.can_update:
                    if tile.rect.collidepoint(((self.rect.left),(self.rect.bottom+10))):
                        colleftded = True
                    if tile.rect.collidepoint(((self.rect.right),(self.rect.bottom+10))):
                        corrighted = True
                if not colleftded:
                    for tile in self.loom.can_update:
                        if self.rect.collidepoint(tile.rect.x, tile.rect.y-1):
                            if [tile.rect.x-96,tile.rect.y] in self.loom.toil.tile_dict.values():
                                self.up = True
                                turned = True
                                break
                elif not corrighted:
                    for tile in self.loom.can_update:
                        if self.rect.collidepoint(tile.rect.right, tile.rect.y-1):
                            if [tile.rect.x+96,tile.rect.y] in self.loom.toil.tile_dict.values():
                                self.up = True
                                turned = True
                                break
                if not turned and not corrighted or not turned and not colleftded:
                    if self.left:
                        self.left = False
                        self.right = True
                    elif self.right:
                        self.left = True
                        self.right = False
            if self.up:
                for tile in self.loom.can_update:
                    if tile.rect.collidepoint(self.rect.x, self.rect.y-50) or tile.rect.collidepoint(self.rect.right, self.rect.y-50):
                        self.up = False
                        break

        self.rect.y += self.down_vel
        if pygame.sprite.spritecollide(self, self.loom.can_update, False):
            if self.down_vel < 0:
                while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                    self.rect.y += 1
                self.rect.y += 1
            elif self.down_vel > 0:
                while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                    self.rect.y -= 1
                self.in_air = False
            self.down_vel = 0
        else:
            self.in_air = True

class Fast_Goblin(Base_Foe):
    """Creates a swift green chap"""

    def __init__(self, loom=Yarn, x=0, y=0, level_point=0):
        super().__init__(loom, x, y, level_point, 32, 32)
        self.horizontal = 4
        self.switchx = [1,1]
        self.floor_turn = True
        self.lost = self.listerine("EnemySheet.png", 32, 32)
    
    def update(self):
        self.image = self.lost[round((self.loom.times / 8) % 6)]
        self.basics()

class Sky_Goblin(Base_Foe):
    """Creates a green chap...of the sky"""
    def __init__(self, loom=Yarn, x=0, y=0, level_point=0):
        super().__init__(loom, x, y, level_point, 32, 32)
        self.down = False
        self.lost = self.listerine("Sprite-0001-sheet.png", 16, 16)
        self.proximity = 320
        self.horizontal = 4
        self.vertical = 4

    def update(self):
        self.image: pygame.surface.Surface = self.lost[round((self.loom.times / 8) % 6)]
        self.image.set_colorkey((0,0,0))
        if self.loom.player.rect.x > self.rect.x - self.proximity and self.loom.player.rect.x < self.rect.x + self.proximity:
            self.proximity = 960
        self.basics()

    def y_move(self):
        self.down_vel = 0
        if self.rect.y > self.loom.player.rect.y+3:
            self.down_vel -= self.vertical
        elif self.rect.y < self.loom.player.rect.y-3:
            self.down_vel += self.vertical
        self.rect.y += self.down_vel
        if pygame.sprite.spritecollide(self, self.loom.can_update, False):
            if self.down_vel < 0:
                while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                    self.rect.y += 1
                self.rect.y += 1
            elif self.down_vel > 0:
                while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                    self.rect.y -= 1
                self.in_air = False
            self.down_vel = 0
        else:
            self.in_air = True
    
    def x_move(self):
        if self.loom.times % random.randint(1,20) == 0:
            if self.rect.centerx < self.loom.player.rect.centerx-3:
                self.right = True
                self.left = False
            elif self.rect.centerx > self.loom.player.rect.centerx+3:
                self.left = True
                self.right = False
        self.rect.x += self.motion[0]
        if pygame.sprite.spritecollide(self, self.loom.can_update, False):
            if self.left:
                while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                    self.rect.x += 2
                self.rect.x += 1
                self.left = False
                self.right = True
            elif self.right:
                while pygame.sprite.spritecollide(self, self.loom.can_update, False):
                    self.rect.x -= 2
                self.rect.x -= 1
                self.right = False
                self.left = True

if __name__ == "__main__":
    bounces = Bouncing()
    bounces.run_game()
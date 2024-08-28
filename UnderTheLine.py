import pygame
from pygame.sprite import Group, Sprite
import sys
import os
import random

from Breakers import *

os.chdir("C:/Users/isaac")

class Bouncing:
    """Attempts to make one of those bouncing square in a square things."""

    def __init__(self):
        """Initialise what needs it"""
        pygame.init()
        pygame.joystick.init()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
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


        self.timer = 0
        self.shielded = 10000
        self.shined = 10000
        self.sped_up = 15000
        self.bordereded = 0
        self.bardereded = 0
        self.left_bricks = 0
        self.extras = 0
        self.rightbreaker = RightBreaker(self)
        self.farrightbreaker = FarRightBreaker(self)
        self.leftbreaker = LeftBreaker(self)
        self.farleftbreaker = FarLeftBreaker(self)
        self.middlebreaker = MiddleBreaker(self)
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
        self.backgrund_image = pygame.image.load("Graphics/Shield.png").convert_alpha()
        self.background_image = pygame.image.load("Graphics/MappedCompassBack.png").convert_alpha()
        self.started = False
        self.inner = True
        self.alter = False
        self.lalter = False
        self.new_began = False
        self.paused = False
        self.swift = True
        self.rumbles = False
        self.dev = False
        self.track_mouse = False
        self.left_mouse = False
        self.right_mouse = False
        self.star = False
        self.dos = False
        self.tres = False
        self.cuatro = False

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
                self.clock.tick(150)
            else:
                self.clock.tick(100)
    
    def update_screen(self):
        """Runs all screen base updates."""
        self.screen.fill((38, 142, 202))
        if self.shielded < 10000:
            self.screen.blit(self.backgrund_image, (0, self.middlebreaker.rect.y + 10))
        self.screen.blit(self.background_image, (0,0))
        for sphere in self.spherage:
            sphere.update()
        for spere in self.livess:
            spere.update()
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
        self.left_bricks = len(self.bricks)
        pygame.display.flip()
    
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
            self.create_wall(4)
            self.cuatro = True
            self.borders()
            self.borderes()
    
    def pause_screen(self):
        """Creates the pause screen."""
        self.screen.fill((38, 142, 102))
        is_not_scaled = (self.screen_width, self.screen_height)
        self.pause_background_image = pygame.image.load("Graphics/Backgrounf.png").convert_alpha()
        self.pause_background_image = pygame.transform.scale(self.pause_background_image, is_not_scaled)
        self.background_rect = self.pause_background_image.get_rect()
        #self.blit_alpha(self.screen, self.pause_background_image, (0, 0), 128)
        self.screen.blit(self.pause_background_image, (0,0))
        pygame.display.flip()

    def check_events(self):
        """Check keyboard events."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:# or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    if self.paused == True:
                        self.paused = False
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
                if pygame.mouse.get_pressed()[0]:
                    self.left_mouse = True
                elif pygame.mouse.get_pressed()[2]:
                    self.right_mouse = True
            if self.track_mouse:
                mouse_pos = pygame.mouse.get_pos()
                if self.left_mouse:
                    for brack in self.bricks:
                        if brack.rect.collidepoint(mouse_pos):
                            self.dev_bricks.add(brack)
                elif self.right_mouse:
                    for brack in self.bricks:
                        if brack.rect.collidepoint(mouse_pos):
                            self.dev_bricks.remove(brack)
            if event.type == pygame.MOUSEBUTTONUP:
                self.track_mouse = False
                if not pygame.mouse.get_pressed()[0]:
                    self.left_mouse = False
                if not pygame.mouse.get_pressed()[2]:
                    self.right_mouse = False
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
                    self.display(self.current_x, self.current_y, 64, 25, self.bricks)
                    self.display(self.current_x, self.current_y+3, 64, 20, self.brickes, inner=self.inner)
                    self.current_y = 300
                    self.current_x = self.screen_width
                elif level == 1:
                    self.level_one(self.current_x, self.current_y, 64, 25, self.bricks)
                    self.level_one(self.current_x, self.current_y+3, 64, 20, self.brickes, inner=self.inner)
                elif level == 2:
                    self.level_two(self.current_x, self.current_y, 64, 25, self.bricks)
                    self.level_two(self.current_x, self.current_y+3, 64, 20, self.brickes, inner=self.inner)
                elif level == 3:
                    self.level_three(self.current_x, self.current_y, 64, 25, self.bricks)
                    self.level_three(self.current_x, self.current_y+3, 64, 20, self.brickes, inner=self.inner)
                elif level == 4:
                    self.level_four(self.current_x, self.current_y, 64, 25, self.bricks)
                    self.level_four(self.current_x, self.current_y+3, 64, 20, self.brickes, inner=self.inner)
                self.current_x += 64
            self.current_x = 0
            self.current_y += 25
            self.reinforce += 1
    
    def borders(self):
        """So think france"""
        self.bordered = 0
        self.cant_update.clear()
        self.can_update = pygame.sprite.Group()
        for key, value in self.brick_dict.items():
            #print(key, value)
            temp = [value[0] + 64, value[1]]
            temps = [value[0] - 64, value[1]]
            tem = [value[0], value[1] + 25]
            tmp = [value[0], value[1] - 25]
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
            print(self.bordered)
        self.bordereded = self.bordered

    def borderes(self):
        """So think france"""
        self.bardered = 0
        self.cant_upadte.clear()
        self.can_upadte = pygame.sprite.Group()
        for key, value in self.bricke_dict.items():
            #print(key, value)
            temp = [value[0] + 64, value[1]]
            temps = [value[0] - 64, value[1]]
            tem = [value[0], value[1] + 25]
            tmp = [value[0], value[1] - 25]
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
            print(self.bardered)
        self.bardereded = self.bardered

    def lay_brick(self, x_position, y_position, width, height, holder, inner=False):
        """Creates a brick to be broken.""" 
        if not inner:
            new_brick = Brick(self, width, height)
        else:
            new_brick = Brick(self, width, height, True)
        new_brick.rect.x = x_position
        new_brick.rect.y = y_position
        if self.reinforce % 2 == 0:
            new_brick.reinforce()
        if self.current_y == 400 and self.current_x == 576:
            new_brick.key()
        if self.current_y == 250 and self.current_x == 576:
            if height == 25:
                new_brick.mystiry()
        elif self.current_y == 250:
            if height == 25:
                new_brick.doppelgunpowder()
            new_brick.lock()
        holder.add(new_brick)
    
    def display(self, x_position, y_position, width, height, holder, inner=False):
        """Creates the admin display."""
        self.star = False
        if height >= 25:
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
                    new_brick.star()
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
                x_position += 64
            if self.grad_up:
                if self.grad >= 180:
                    self.grad = self.base_grad
            else:
                if self.grad <= 1:
                    self.grad = self.base_grad
            x_position = 0
            y_position += 25
                
    
    def level_one(self, x_position, y_position, width, height, holder, inner=False):
        """Creates all breaking bricks for level one."""
        self.star = False
        new_brick = self.brick_base(width, height, inner, x_position, y_position)
        new_brick.gradient("Blue", int(self.grad))
        if self.grad_up:
            self.grad += 0.5
        else:
            self.grad -= 0.5
        new_brick.rect.x = x_position
        new_brick.rect.y = y_position
        holder.add(new_brick)
    
    def level_two(self, x_position, y_position, width, height, holder, inner=False):
        """Creates all breaking bricks for level two."""
        #self.rebar()
        self.star = False
        if self.current_y <= 200:
            new_brick = self.brick_base(width, height, inner, x_position, y_position)
            if self.current_y % 2 == 0:
                new_brick.reinforce()
            new_brick.rect.x = x_position
            new_brick.rect.y = y_position
            holder.add(new_brick)
    
    def level_three(self, x_position, y_position, width, height, holder, inner=False):
        """Creates all breaking bricks for level three."""
        #self.rebar()
        self.star = False
        new_brick = self.brick_base(width, height, inner, x_position, y_position)
        if x_position == 256 and y_position == 200:
            new_brick.key()
        if y_position == 100:
            new_brick.gunpowder()
        if x_position == 1024 and y_position == 200:
            new_brick.homicide()
        x_list = [960, 1024, 1088]
        y_list = [175, 200, 225]
        if x_position in x_list and y_position in y_list:
            if x_position == 1024 and y_position == 200:
                pass
            else:
                new_brick.lock()
        new_brick.rect.x = x_position
        new_brick.rect.y = y_position
        holder.add(new_brick)
    
    def level_four(self, x_position, y_position, width, height, holder, inner=False):
        """Creates all rbeaking bricks for level four."""
        #self.rebar()
        self.star = False
        new_brick = self.brick_base(width, height, inner, x_position, y_position)
        new_brick.rect.x = x_position
        new_brick.rect.y = y_position
        holder.add(new_brick)

    def brick_base(self, width, height, inner, x, y):
        self.shrapnel.empty()
        for sphere in self.spherage:
            sphere.recenters()
        new_brick = Brick(self, width, height, inner)
        if height >= 25:
            self.brick_dict[new_brick] = [x, y]
        elif height < 25:
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
        self.clock.tick(60)
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
        is_scale = (size,size)
        if self.war_crime:
            is_scale = (5,5)

        self.image = pygame.image.load("Graphics/Marble.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, is_scale)
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
        if self.dead:
            self.dead_time = 0
            self.dead = False
        self.screen.blit(self.image, self.rect)
    
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
            if self.fmoving_left:
                self.fmoving_right = True
                self.fmoving_left = False
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
            if self.fmoving_right:
                self.fmoving_left = True
                self.fmoving_right = False
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
                elif self.fmoving_left:
                    self.fmoving_right = True
                    self.fmoving_left = False
            elif self.moving_right:
                self.moving_left = True
                self.moving_right = False
                if self.smoving_right:
                    self.smoving_left = True
                    self.smoving_right = False
                elif self.fmoving_right:
                    self.fmoving_left = True
                    self.fmoving_right = False
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
                        print("Lich key error:Brick Broken")
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
                    print("Lich key error:Bomb Breaker")
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
                    self.bouncer.locked.clear()
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
                if self.bouncer.shined < 10000:
                    x = shard.rect.x
                    y = shard.rect.y
                    shard.kill()
                    self.bouncer.brick_dict.pop(shard)
                    self.bouncer.borders()
                    self.bouncer.borderes()
                    if self not in self.bouncer.launched:
                        self.bouncer.doppelexplode(x,y)
                if shard in self.bouncer.expand:
                    self.bouncer.unbreakable.append(shard)
                    self.bouncer.locked.append(shard)
                    self.excalibur(shard)
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
                    #print("CAT")
            elif direction == 'Eat':
                if pol.rect.y-3 == shard.rect.y and pol.rect.x > shard.rect.x:
                    pol.right_outer()
                    pol.update()
                    #print("CAT")
            elif direction == 'Shredded':
                if pol.rect.x == shard.rect.x and pol.rect.y > shard.rect.y:
                    pol.down_outer()
                    pol.update()
                    #print("CAT")
            elif direction == 'Wheat':
                if pol.rect.y-3 == shard.rect.y and pol.rect.x < shard.rect.x:
                    pol.left_outer()
                    pol.update()
                    #print("CAT")
        pygame.display.flip()
        self.bouncer.clock.tick(100)
        return(victory)

class Bal(Sprite):
    """Spoofs a ball for lives."""
    def __init__(self, bounce):
        """Does it all."""
        super().__init__()
        self.bouncer = bounce
        self.screen = self.bouncer.screen
        is_scale = (15,15)
        self.image = pygame.image.load("Graphics/Marble.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, is_scale)
        self.rect = self.image.get_rect()
    
    def update(self):
        self.screen.blit(self.image, self.rect)
    
class Star(Sprite):
    """Creates the star sprite for powerup bar"""
    def __init__(self, bounce):
        """Does it all."""
        super().__init__()
        self.bouncer = bounce
        self.screen = self.bouncer.screen
        is_scale = (20,20)
        self.image = pygame.image.load("Graphics/Star_Icon_Small.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, is_scale)
        self.rect = self.image.get_rect()
    
    def update(self):
        self.screen.blit(self.image, self.rect)

class Brick(Sprite):
    """Creates the bricks out of which one must break."""
    
    def __init__(self, bouncer, width, height, inner=False):
        """Initialise the basic attributes of the bricks."""
        super().__init__()
        self.inner = inner
        self.bouncer = bouncer
        self.screen = bouncer.screen
        self.screen_rect = self.screen.get_rect()
        self.scaled = (width,height)
        self.image = pygame.image.load("Graphics/RedBrickWide.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load("Graphics/Seafoam.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        self.rect = self.image.get_rect()
    
    def update(self):
        """Updates the bricks."""
        self.screen.blit(self.image, self.rect)
    
    # Brick sprite changes and list appends for special bricks.

    def reinforce(self):
        self.image = pygame.image.load("Graphics/BlueBorderBrickWide.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.rect.height < 25:
            self.image = pygame.image.load("Graphics/BlueBrickWide.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load("Graphics/Seafoam.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        self.bouncer.undamaged.append(self)
    
    def gunpowder(self):
        self.image = pygame.image.load("Graphics/BombBrickWide.png").convert_alpha()
        self.innervate()
        self.bouncer.bomb.append(self)

    def doppelgunpowder(self):
        self.image = pygame.image.load("Graphics/DoppelBombBrickWide.png").convert_alpha()
        self.innervate()
        self.bouncer.doppelbomb.append(self)

    def lock(self):
        self.image = pygame.image.load("Graphics/HardBrickWide.png").convert_alpha()
        self.innervate()
        self.bouncer.locked.append(self)
        self.bouncer.lockaged.add(self)

    def key(self):
        self.image = pygame.image.load("Graphics/KeyWide.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load("Graphics/Seafoam.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        self.bouncer.keys.append(self)
    
    def open(self):
        if self in self.bouncer.bomb:
            self.image = pygame.image.load("Graphics/BombBrickWide.png").convert_alpha()
        elif self in self.bouncer.bomb:
            self.image = pygame.image.load("Graphics/BombBrickWide.png").convert_alpha()
        elif self in self.bouncer.doppelbomb:
            self.image = pygame.image.load("Graphics/DoppelBombBrickWide.png").convert_alpha()
        elif self in self.bouncer.lotus:
            self.image = pygame.image.load("Graphics/Lotus.png").convert_alpha()
        elif self in self.bouncer.new_begin:
            self.image = pygame.image.load("Graphics/RedoBrick.png").convert_alpha()
        else:
            self.image = pygame.image.load("Graphics/HardGreenBrickWide.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load("Graphics/Seafoam.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        #self.bouncer.locked.remove(self)

    def unbreak(self):
        self.image = pygame.image.load("Graphics/UnbrickMoss.png").convert_alpha()
        self.innervate()
        self.bouncer.unbreakable.append(self)
        self.bouncer.locked.append(self)
        self.bouncer.lockaged.add(self)
    
    def redo(self):
        self.image = pygame.image.load("Graphics/RedoBrick.png").convert_alpha()
        self.innervate()
        self.bouncer.new_begin.append(self)

    def star(self):
        self.image = pygame.image.load("Graphics/YeStarBrickWide.png").convert_alpha()
        self.innervate()
        self.bouncer.shiny.append(self)
    
    def plus_one(self):
        self.image = pygame.image.load("Graphics/PlusOneWide.png").convert_alpha()
        self.innervate()
        self.bouncer.plus.append(self)
    
    def homicide(self):
        self.image = pygame.image.load("Graphics/Lotus.png").convert_alpha()
        self.innervate()
        self.bouncer.lotus.append(self)
    
    def bar_expand(self):
        self.image = pygame.image.load("Graphics/MonsterBrickKind.png").convert_alpha()
        self.innervate()
        self.bouncer.expand.append(self)
        self.bouncer.expand1.append(self)
        self.bouncer.expand2.append(self)
        self.bouncer.expand3.append(self)
        self.bouncer.expand4.append(self)
        self.bouncer.expand5.append(self)
    
    def bar_damage1(self):
        self.image = pygame.image.load("Graphics/MonsterBrick.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def bar_damage2(self):
        self.image = pygame.image.load("Graphics/MonsterBrickAngry.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def bar_damage3(self):
        self.image = pygame.image.load("Graphics/MonsterBrickInjured.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def bar_damage4(self):
        self.image = pygame.image.load("Graphics/MonsterBrickDying.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def mystiry(self):
        self.image = pygame.image.load("Graphics/Mystiry.png").convert_alpha()
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
        self.image = pygame.image.load("Graphics/BarExpand.png").convert_alpha()
        self.innervate()
        self.bouncer.sealing.append(self)
    
    def compass(self):
        self.image = pygame.image.load("Graphics/MappedCompass.png").convert_alpha()
        self.innervate()
        self.bouncer.cardinal.append(self)
    
    def shield(self):
        self.image = pygame.image.load("Graphics/Red/Shield_Brick.png").convert_alpha()
        self.innervate()
        self.bouncer.barrier.append(self)
    
    def gradient(self, colour, shade):
        try:
            self.image = pygame.image.load(f"Graphics/{colour}{shade}.png").convert_alpha()
        except FileNotFoundError:
            self.image = pygame.image.load(f"Graphics/{colour}1.png").convert_alpha()
            print("CAT")
            self.bouncer.grad = self.bouncer.base_grad
        self.innervate()
    
    def up_outer(self):
        self.image = pygame.image.load("Graphics/RemnantUp.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def right_outer(self):
        self.image = pygame.image.load("Graphics/RemnantRight.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def down_outer(self):
        self.image = pygame.image.load("Graphics/RemnantDown.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def left_outer(self):
        self.image = pygame.image.load("Graphics/RemnantLeft.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
    
    def acid(self):
        self.image = pygame.image.load("Graphics/Acid_Brick.png").convert_alpha()
        self.innervate()
        self.bouncer.acidic.append(self)
    
    def paint_stripe(self):
        self.image = pygame.image.load("Graphics/Fast_Clock.png").convert_alpha()
        self.innervate()
        self.bouncer.accelerate.append(self)

    def damage(self):
        """Switches to the damaged sprite."""
        self.image = pygame.image.load("Graphics/BlueBrickWide.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load("Graphics/Seafoam.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
    
    def innervate(self):
        self.image = pygame.transform.scale(self.image, self.scaled)
        if self.inner:
            self.image = pygame.image.load("Graphics/Seafoam.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, self.scaled)
        if self in self.bouncer.undamaged:
            self.bouncer.undamaged.remove(self)



bounces = Bouncing()
bounces.run_game()
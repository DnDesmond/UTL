import pygame
import sys
import os
from pygame.sprite import Sprite
from math import sqrt

# os.chdir("UTL")

def eqs(point, point_2):
    x1,y1 = point
    x2,y2 = point_2
    slope = (y2-y1)/(x2-x1)
    coy = 1
    if slope%1 != 0:
        mult = 1
        while True:
            if (slope*mult)%1 == 0:
                slope = slope*mult
                y1 = y1*mult
                coy = mult
                break
            mult+=1
    slope = round(slope)
    eq = {"coy":coy, "cofx":-slope, "c":round((-y1)+(slope*x1))}
    # print(f"{coy}y +{eq['cofx']}x + {eq["c"]} = 0")
    return eq

def sides(point:tuple, point_2:tuple, eq:dict):
    x1, y1 = point
    x2, y2 = point_2
    a,b,c = eq.values()
    distance = (a*x1)+(b*y1)+c/sqrt((a**2)+(b**2))
    distance_2 = (a*x2)+(b*y2)+c/sqrt((a**2)+(b**2))
    if distance > 0 and distance_2 > 0:
        print("Same")
    elif distance < 0 and distance_2 < 0:
        print("Same")
    else:
        print("Different")

def simuls(static_1:dict, static_2:dict):
    a1,b1,c1 = static_1.values()
    a2,b2,c2 = static_2.values()
    if a1 != a2:
        t = a1
        a1 *= a2
        b1 *= a2
        c1 *= a2
        a2 *= t
        b2 *= t
        c2 *= t
    if a1 > 0 and a2 > 0:
        a1 *= -1
        b1 *= -1
        c1 *= -1
        
    x = b1+b2
    if x != 0:
        valx = (-c1-c2)/x
    else:
        valx = 0
    valy = (-c1-(valx*b1))/a1
    
    # print(valx)
    # print(valy)

    col = (valx, valy)

    return col

def length(point, point_2):
    x1,y1 = point
    x2,y2 = point_2
    tot = sqrt(((x2-x1)**2)+((y2-y1)**2))
    return tot

def dotxline(point, cap, cap_2):
    full = length(cap, cap_2)
    half = length(cap, point)
    halved = length(cap_2, point)
    if half + halved >= full-1 and half + halved <= full+1:
        return True
    else:
        return False


class Game:
    """Creates a game or at least tries its best"""

    def __init__(self):
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height#
        self.char = Block(self)
        self.clock = pygame.time.Clock()
        self.colly = False
        # self.line_caps = [(501,700),(700,700)]
        self.temps = []
        self.lines = [((501,700),(700,700)),((801,600),(1000,600))]
    
    def run_game(self):
        while True:
            self.update_screen()
            self.check_events()
            self.clock.tick(60)

    def update_screen(self):
        if self.colly:
            self.screen.fill((123+10,49+10,78+10))
        else:
            self.screen.fill((40,234,123))
        # self.colls()
        self.char.update()
        # pygame.draw.line(self.screen, (4,4,4), self.screen_rect.center, self.char.rect.center)
        for line in self.lines:
            pygame.draw.line(self.screen, (4,4,4), line[0], line[1])
        if len(self.temps) > 0:
            pygame.draw.line(self.screen, (4,4,4), self.temps[0], pygame.mouse.get_pos())
        pygame.display.flip()
    
    def colls(self):
        self.char.lineate()
        for line in self.lines:
            for linec in self.char.lines:
                self.colly = self.actuolls(line[0], line[1], linec[0], linec[1])
                if self.colly == True:
                    # print("TRUE")
                    break
            if self.colly == True:
                break
        
    
    def actuolls(self, point, point_2, point_3, point_4):
        try:
            eq = eqs(point, point_2)
            eq1 = eqs(point_3, point_4)
            col = simuls(eq, eq1)
            colly = dotxline(col, point, point_2) and dotxline(col, point_3, point_4)
        except ZeroDivisionError:
            colly = False
        return colly

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                   pygame.quit()
                   sys.exit()
                if event.key == pygame.K_UP:
                    self.char.down = 0
                    self.char.down -= 17
                if event.key == pygame.K_RIGHT:
                    self.char.richtig = True
                if event.key == pygame.K_LEFT:
                    self.char.falsch = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.char.richtig = False
                if event.key == pygame.K_LEFT:
                    self.char.falsch = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.temps.append(pygame.mouse.get_pos())
                if len(self.temps) > 1:
                    self.lines.append(self.temps)
                    self.temps = []
                   
class Block(Sprite):
    """Attempts a block"""

    def __init__(self,game:Game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.screen_width = self.game.screen_rect.width
        self.screen_height = self.game.screen_rect.height
        self.image = pygame.image.load("Rot.png")
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (30,30))
        self.width = self.rect.width
        self.height = self.rect.height
        self.richtig = False
        self.falsch = False
        self.floored = False
        self.x_1, self.y_1 = self.game.screen_rect.center
        self.exos = self.rect.center
        self.deley = 0

        self.down = 0
        self.right = 0

    def update(self):
        self.lines = [(self.rect.topleft,(self.rect.bottomleft[0]+1,self.rect.bottomleft[1])),(self.rect.topright,(self.rect.bottomright[0]+1,self.rect.bottomright[1]))]#,(self.rect.topright,(self.rect.bottomright[0],self.rect.bottomright[1]+1))]
        self.motion()
        self.screen.blit(self.image, (self.rect.x,self.rect.y))
    
    def lineate(self):
        self.lines = [(self.rect.topleft,(self.rect.bottomleft[0]+1,self.rect.bottomleft[1])),(self.rect.topright,(self.rect.bottomright[0]+1,self.rect.bottomright[1]))]
    
    def motion(self):
        self.rect.y += round(self.down)
        self.colls()
        self.exos = self.rect.center
        self.rect.x += round(self.right)
        if self.richtig and self.right < 12:
            self.right += 1
        if self.falsch and self.right > -12:
            self.right -= 1
        if self.right > 0:
            self.right -= 0.5
        if self.right < 0:
            self.right += 0.5
        
        if self.down < 15:
            self.down += 1
    
    def colls(self):
        self.game.colls()
        if self.rect.bottom > self.screen_height:
            if self.down > 0:
                self.down = 0
            self.rect.y = self.screen_height-self.height
        if self.game.colly:
            self.down = 0
            if self.exos[1] < self.rect.centery:
                while self.game.colly:
                    self.rect.y -= 1
                    self.game.colls()
            if self.exos[1] > self.rect.centery:
                while self.game.colly:
                    self.rect.y += 1
                    self.game.colls()
                

        

class Fruit(Sprite):
    """Obstacle?"""

    def __init__(self,game):
        super().__init__()
        

game = Game()
game.run_game()
# # eqs((4,5),(6,8))
# x1 = int(input("Please enter x1: "))
# y1 = int(input("Please enter y1: "))
# point = (x1,y1)
# x2 = int(input("Please enter x2: "))
# y2 = int(input("Please enter y2: "))
# point_2 = (x2,y2)

# point = (14,14)
# point_2 = (-14,-14)

# eq = eqs(point, point_2)

# x1 = int(input("Please enter x1: "))
# y1 = int(input("Please enter y1: "))
# point = (x1,y1)
# x2 = int(input("Please enter x2: "))
# y2 = int(input("Please enter y2: "))
# point_2 = (x2,y2)

# point = (-14,14)
# point_2 = (14,-14)

# eq2 = eqs(point, point_2)

# simuls(eq, eq2)
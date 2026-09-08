import sys
import math
import csv
import random

from RP import resource_path as rp # type:ignore
import pygame
pygame.init()

print(pygame.font.get_fonts())

class Keane:
    """Central class to game"""

    def __init__(self):
        self.screen = pygame.display.set_mode((800,400))
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = self.screen_rect.width, self.screen_rect.height
        self.field = Field(self)
        self.clock = pygame.time.Clock()
    
    def run_game(self):
        while True:
            self.check_events()
            self.update_screen()
            self.clock.tick(60)
    
    def update_screen(self):
        self.screen.fill((76,153,47))
        self.field.update()
        pygame.display.flip()
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.keydowns(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def keydowns(self, event):
        if event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    def mices(self):
        pass

class Field:
    """Creates the actual map object"""

    def __init__(self, author:Keane):
        self.game = author
        self.screen = self.game.screen
        self.image = pygame.surface.Surface((300,300))
        self.image.fill((20,20,20))
        self.imaged = pygame.surface.Surface((300,300))
        self.imaged.fill((20,20,20))
        self.square = pygame.surface.Surface((20,20))
        self.square.fill((12,183,12))
        self.unfortunate_square = pygame.surface.Surface((20,20))
        self.unfortunate_square.fill((183,12,12))
        self.blue_square = pygame.surface.Surface((20,20))
        self.blue_square.fill((12,12,183))
        dire = pygame.font.match_font("comicsansms")
        font = pygame.font.Font(dire, 14)
        for num in range(1,10):
            temp = pygame.surface.Surface((20,20))
            temp.fill((243,147,13))
            num = str(num)
            if num == "1":
                temp.blit(font.render("M", False, (2,2,2)), (0,0))
            elif num == "9":
                temp.blit(font.render("1", False, (2,2,2)), (0,0))
            else:
                temp.blit(font.render(num, False, (2,2,2)), (0,0))
            setattr(self, f"num{num}", temp.copy())
        self.rows = []
        row = []
        self.chance = 0.8
        self.maps()
        self.olds = []
        for row in self.rows:
            pare = []
            print(f"{row}")
            for x in row.copy():
                pare.append(int(x))
            self.olds.append(pare.copy())
        print("\n")
        self.stuck()
        for row in self.rows:
            print(f"{row}")

    def maps(self):
        # rowdy = [0 for x in range(15)]
        # self.rows.append(rowdy)
        for y in range(0, (self.image.get_height()//20-2)):
            row = []
            for x in range(0,(self.image.get_width()//20-2)):
                row.append(random.choice([0 for x in range(0,int(self.chance*100))]+[1 for x in range(0,int((1-self.chance)*100))]))
            # row.append(0)
            # print(len(row))
            self.rows.append(row.copy())
        # self.rows.append(rowdy)

    
    def update(self):
        x,y = [0 for x in range(0,2)]
        for row in self.rows:
            x = 0
            for tile in row:
                if tile == 0:
                    self.image.blit(self.square, (x*20,y*20))
                elif tile == 1:
                    self.image.blit(self.unfortunate_square, (x*20,y*20))
                for num in range(1,10):
                    if tile == num:
                        self.image.blit(getattr(self, f"num{num}"), (x*20,y*20))
                x += 1
            y += 1
        self.screen.blit(self.image, (50,50))
        x,y = [0 for x in range(0,2)]
        for row in self.olds:
            x = 0
            for tile in row:
                tile = int(tile)
                if tile == 0:
                    self.imaged.blit(self.square, (x*20,y*20))
                elif tile == 1:
                    self.imaged.blit(self.unfortunate_square, (x*20,y*20))
                # for num in range(1,9):
                #     if tile == num:
                #         self.image.blit(getattr(self, f"num{num}"), (x*20,y*20))
                x += 1
            y += 1
        self.screen.blit(self.imaged, (400,50))

    def tiler(self):
        sheet = pygame.image.load(rp("sprites.png"))
        height = sheet.get_height()
        self.tiles = []
        for y in range(0,2):
            for x in range(0,0):
                pass
    
    def stuck(self):
        cope_rows = []
        cope_row = []
        up_portents = [-1,0,1]
        portents = [-1,1]
        down_portents = [-1,0,1]
        row = self.rows[0]
        for x in range(len(row)):
            if x != 0 and x != len(row):
                x += row[x-1]
                x += row[x+1]
            elif x != 0:
                x += row[-2]
            else:
                x += row[1]
            cope_row.append(x)
        cope_rows.append(cope_row.copy())
        self.rows = cope_rows.copy()

    
    def checkers(self, row, coef, cur):
        tile = 0
        try:
            tile += row[cur+coef]
        except:
            pass
        return tile

                

        




if __name__ == "__main__":
    game = Keane()
    game.run_game()
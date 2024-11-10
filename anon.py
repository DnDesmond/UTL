import sys
import pygame
from pygame.sprite import Sprite, Group
from RP import resource_path as r
from non import translator, letters, decoder, from_a_stone, coder

class Converter:
    """Attempts to create the front end for the converter."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_width: int = self.screen.get_width()
        self.screen_height: int = self.screen.get_height()
        self.screen_rect: pygame.rect.Rect = self.screen.get_rect()
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.buttons: Group[Button] = pygame.sprite.Group()
        self.buttons_2: Group[Button] = pygame.sprite.Group()
        self.base_a: int = 2
        self.base_b: int = 2
        self.blit_number: str = "1"
        self.number: str = "1"
        self.lest: list[str] = [self.number]
        self.times: int = 0
        self.deleting: bool = False
        self.shifted: bool = False
        self.auto_update: bool = False
        self.ralted: bool = False
        for cat in range(0, 31):
            button: Button = Button(self, (40,20), (cat*40,0), cat+1)
            if cat == 15:
                button.rect.x += 20
            elif cat > 15:
                button.rect.x += 40
            if button.number == 2:
                button.hit = True
            self.buttons.add(button)
        for cat in range(0, 31):
            button: Button = Button(self, (40,20), (cat*40,0), cat+32)
            if cat == 15:
                button.rect.x += 20
            elif cat > 15:
                button.rect.x += 40
            button.rect.y += 20
            self.buttons.add(button)
        for cat in range(0, 31):
            button: Button = Button(self, (40,20), (cat*40,0), cat+1)
            if cat == 15:
                button.rect.x += 20
            elif cat > 15:
                button.rect.x += 40
            if button.number == 2:
                button.hit = True
            button.rect.y = 680
            self.buttons_2.add(button)
        for cat in range(0, 31):
            button: Button = Button(self, (40,20), (cat*40,0), cat+32)
            if cat == 15:
                button.rect.x += 20
            elif cat > 15:
                button.rect.x += 40
            button.rect.y = 680
            button.rect.y += 20
            self.buttons_2.add(button)
    
    def runs(self):
        while True:
            self.update_screen()
            self.check_events()
            self.clock.tick(60)
    
    def update_screen(self):
        self.screen.fill((0,0,0))#((25,25,25))
        for button in self.buttons:
            button.update()
        for button in self.buttons_2:
            button.update()
        self.texts(self.blit_number, (self.screen_rect.centerx,self.screen_rect.centery+(self.screen_height/4)), 40)
        self.texts(str(self.number), (self.screen_rect.centerx,self.screen_rect.centery-(self.screen_height/4)), 40)
        self.texts("↓", self.screen_rect.center, 60)
        if self.deleting:
            if self.times % 5 == 0:
                self.number = self.number[:-1]
        self.times += 1
        pygame.display.flip()
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and self.ralted:
                    pygame.quit()
                    sys.exit()
                for num in range(0,10):
                    if event.key == getattr(pygame, f"K_{num}"):
                        self.number += str(num)
                for num in letters:
                    if event.key == getattr(pygame, f"K_{num}"):
                        if not self.shifted:
                            self.number += str(num)
                        else:
                            self.number += str(num).upper()
                if event.key == pygame.K_BACKSPACE:
                    if not self.shifted:
                        self.deleting = True
                    if self.shifted:
                        self.lest = [self.number]
                if event.key == pygame.K_PAGEUP:
                    self.lest.append(self.number)
                if event.key == pygame.K_RETURN:
                    if not self.shifted:
                        self.results()
                    else:
                        try:
                            self.blit_number = from_a_stone(decoder(self.lest, self.base_a))
                        except:
                            pass
                if event.key == pygame.K_INSERT:
                    self.blit_number = from_a_stone(coder(self.number, self.base_b), delimeter=" ")
                if event.key == pygame.K_LSHIFT:
                    self.shifted = True
                if event.key == pygame.K_RALT:
                    self.ralted = True
                if event.key == pygame.K_PAGEDOWN:
                    if self.auto_update:
                        self.auto_update = False
                    else:
                        self.auto_update = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.deleting = False
                if event.key == pygame.K_LSHIFT:
                    self.shifted = False
                if event.key == pygame.K_RALT:
                    self.ralted = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for check in self.buttons:
                    if check.number != 1:
                        if check.rect.collidepoint(pygame.mouse.get_pos()):
                            check.hit = True
                            for button in self.buttons:
                                if button != check:
                                    button.hit = False
                            self.base_a = check.number
                            break
                for check in self.buttons_2:
                    if check.number != 1:
                        if check.rect.collidepoint(pygame.mouse.get_pos()):
                            check.hit = True
                            for button in self.buttons_2:
                                if button != check:
                                    button.hit = False
                            self.base_b = check.number
                            if self.auto_update:
                                self.results()
                            break
        
    def texts(self, string: str, centerpoint: tuple[int, int], font_size: int):
        font: pygame.font.Font = pygame.font.Font("times.ttf", font_size)
        text = font.render(string, True, (255,255,255))
        text_rect = text.get_rect()
        text_rect.center = centerpoint
        self.screen.blit(text, text_rect)

    def results(self):
        can_blit = False
        for num in self.number:
            if num != "0":
                can_blit = True
        if can_blit:
            self.blit_number = translator(self.number, self.base_a, self.base_b)

class Button(Sprite):
    """Attempts to create the basic buttons."""

    def __init__(self, convert: Converter, size: tuple[int,int], x_y: tuple[int,int], number: int=1):
        super().__init__()
        self.number = number
        self.convert: Converter = convert
        self.screen: pygame.display = self.convert.screen
        self.image = pygame.image.load(r("Not_Clicked.png"))
        self.image_2 = pygame.image.load(r("Clicked.png"))
        self.image = pygame.transform.scale(self.image, (size))
        self.image_2 = pygame.transform.scale(self.image_2, (size))
        self.rect = self.image.get_rect()
        self.rect.x = x_y[0]
        self.rect.y = x_y[1]
        self.hit: bool = False
        self.current_image = self.image.copy()
        font: pygame.font.Font = pygame.font.Font('times.ttf', 20)
        if len(str(number))>1:
            text = font.render(f"{number}", 0, (0,3,0))
        else:
            text = font.render(f" {number}", 0, (0,3,0))
        self.image.set_colorkey((0,0,0))
        self.image_2.set_colorkey((0,0,0))
        self.image.blit(text, ((self.rect.width/2)-(text.get_rect().width/2),0))
        self.image_2.blit(text, ((self.rect.width/2)-(text.get_rect().width/2),0))
        if self.number == 1:
            self.image = pygame.image.load(r("Star_Icon.png"))
            self.image_2 = pygame.image.load(r("Star_icon.png"))
            self.image = pygame.transform.scale(self.image, (size))
            self.image_2 = pygame.transform.scale(self.image_2, (size))
    
    def update(self):
        if self.hit:
            self.current_image = self.image_2
        else:
            self.current_image = self.image
        self.screen.blit(self.current_image, self.rect)

converts: Converter = Converter()
converts.runs()
import pygame


class MiddleBreaker:
    """Makes that bar thing that bounces the breaker spheres."""
    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (27,10)

        self.image = pygame.image.load("Graphics/MiddleMudBar.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.y += 250
        self.rect.x -= 15

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.left > 23:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-23:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

class RightBreaker:
    """Makes that bar thing that bounces the breaker spheres to the right."""

    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (15,10)

        self.image = pygame.image.load("Graphics/RightMudBar.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x += 21
        self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 50:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-8:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

class FarRightBreaker:
    """Makes that bar thing that bounces the breaker spheres to the right."""

    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (8,10)

        self.image = pygame.image.load("Graphics/FarRightMudBar.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x += 33
        self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 65:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)
    
class LeftBreaker:
    """Makes that bar thing that bounces the breaker spheres to the left."""
    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (15,10)

        self.image = pygame.image.load("Graphics/LeftMudBar.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x -= 21.5
        self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 8:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-50:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

class FarLeftBreaker:
    """Makes that bar thing that bounces the breaker spheres to the left."""
    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (8,10)

        self.image = pygame.image.load("Graphics/FarLeftMudBar.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x -= 32
        self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 0:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-65:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

class BigMiddleBreaker:
    """Makes that bar thing that bounces the breaker spheres."""
    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (54,10)

        self.image = pygame.image.load("Graphics/MiddleMudBarMonster.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.y += 250
        #self.rect.x -= 15

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.left > 46:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-46:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

class BigRightBreaker:
    """Makes that bar thing that bounces the breaker spheres to the right."""

    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (30,10)

        self.image = pygame.image.load("Graphics/RightMudBarMonster.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x += 42
        #self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 100:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-16:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

class BigFarRightBreaker:
    """Makes that bar thing that bounces the breaker spheres to the right."""

    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (16,10)

        self.image = pygame.image.load("Graphics/FarRightMudBarMonster.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x += 65
        #self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 130:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)
    
class BigLeftBreaker:
    """Makes that bar thing that bounces the breaker spheres to the left."""
    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (30,10)

        self.image = pygame.image.load("Graphics/LeftMudBarMonster.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x -= 42
        #self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 16:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-100:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

class BigFarLeftBreaker:
    """Makes that bar thing that bounces the breaker spheres to the left."""
    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (16,10)

        self.image = pygame.image.load("Graphics/FarLeftMudBarMonster.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x -= 65
        #self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 0:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-130:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

class SmallMiddleBreaker:
    """Makes that bar thing that bounces the breaker spheres."""
    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (54,10)

        self.image = pygame.image.load("Graphics/Blue_Square.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.y += 250
        #self.rect.x -= 15

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.left > 46:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-46:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

class SmallRightBreaker:
    """Makes that bar thing that bounces the breaker spheres to the right."""

    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (30,10)

        self.image = pygame.image.load("Graphics/Red_Square.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x += 42
        #self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 100:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-16:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

class SmallFarRightBreaker:
    """Makes that bar thing that bounces the breaker spheres to the right."""

    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (16,10)

        self.image = pygame.image.load("Graphics/Blue_Square.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x += 65
        #self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 130:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)
    
class SmallLeftBreaker:
    """Makes that bar thing that bounces the breaker spheres to the left."""
    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (30,10)

        self.image = pygame.image.load("Graphics/Red_Square.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x -= 42
        #self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 16:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-100:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

class SmallFarLeftBreaker:
    """Makes that bar thing that bounces the breaker spheres to the left."""
    def __init__(self, bounce):
        """Initialises everything"""
        super().__init__()
        self.screen = bounce.screen
        self.bouncer = bounce
        self.screen_rect = self.screen.get_rect()
        self.bar_scale = (16,10)

        self.image = pygame.image.load("Graphics/Blue_Square.png")
        self.image = pygame.transform.scale(self.image, self.bar_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x -= 65
        #self.rect.x -= 15
        self.rect.y += 250

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Updates all aspects of the bar."""
        if self.bouncer.moving_left and self.rect.x > 0:
            self.x -= 5
        elif self.bouncer.moving_right and self.rect.right < self.bouncer.screen_width-130:
            self.x += 5
        self.rect.x = self.x
        self.screen.blit(self.image, self.rect)

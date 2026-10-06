import sys
import random
import pygame

pygame.init()
# It's a Tamsyn Muir reference
class Game:
    """Creates the main class for the game"""

    def __init__(self):
        self.screen = pygame.display.set_mode((400,600))
        self.screen_rect = self.screen.get_rect()
        self.bricks:list[Brick] = []
        self.toops = ["tee","right_s","left_s","el","jay","square","line"]
        for x in range(0,6):
            self.bricks.append(Brick(self, toop=random.choice(self.toops)))
            # self.bricks.append(Brick(self, toop=random.choice(self.toops)))
        self.tiles:list[Tile] = []
        self.live_brick = self.bricks[0]
        self.timer = 0
        self.clock = pygame.time.Clock()

    def run_game(self):
        while True:
            self.check_events()
            self.update_screen()
            self.timer += 1
            self.clock.tick(60)

    def update_screen(self):
        self.screen.fill((4,4,4))
        self.live_brick.update()
        for tile in self.tiles:
            self.screen.blit(tile.image, tile.rect)
        if self.timer % 20   == 0:
            self.live_brick.down()
            for y in range(20,self.screen_rect.height,20):
                if [tile.pos[1] for tile in self.tiles].count(y) >= self.screen_rect.width//20:
                    for tile in self.tiles.copy():
                        if tile.pos[1] == y:
                            self.tiles.remove(tile)
                    for tile in self.tiles:
                        if tile.pos[1] < y:
                            tile.pos[1] += 20
                    for tile in self.tiles:
                        tile.position()
                    break 
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._keydowns(event)
            elif event.type == pygame.QUIT:
                self._ends()

    def _keydowns(self, event):
        if event.key == pygame.K_q:
            self._ends()
        elif event.key == pygame.K_DOWN:
            temp = self.live_brick
            while self.live_brick == temp:
                self.live_brick.down()
                self.live_brick = self.bricks[0]
        elif event.key == pygame.K_RIGHT:
            self.live_brick.right()
        elif event.key == pygame.K_LEFT:
            self.live_brick.left()
        elif event.key == pygame.K_UP:
            self.live_brick.spin()
        elif event.key == pygame.K_r:
            self.tiles = []

    def _ends(self):
        pygame.quit()
        sys.exit()

class Brick:
    """Creates one of the 4 tile Tetris shapes"""

    def __init__(self, game:Game, toop="tee"):
        self.game = game
        self.screen = self.game.screen
        self.tiles = [Tile(self) for x in range(0,4)]
        colour = self.game.toops.index(toop)
        for tile in self.tiles:
            tile.image.fill((40*colour,130,114))
        self.shape(toop)
        self.toop = toop
        self.halted = False

    def shape(self, toop="tee"):
        if toop == "left_s":
            self.tiles[0].pos[0] += 20
            self.tiles[0].pos[1] += 0
            self.tiles[1].pos[0] += 20
            self.tiles[1].pos[1] += 20
            self.tiles[2].pos[0] += 40
            self.tiles[2].pos[1] += 20
        elif toop == "right_s":
            self.tiles[0].pos[0] += 20
            self.tiles[0].pos[1] += 20
            self.tiles[1].pos[1] += 20
            self.tiles[2].pos[0] += 40
            self.tiles[3].pos[0] += 20
        elif toop == "line":
            self.tiles[0].pos[1] += 20
            self.tiles[1].pos[0] += 20
            self.tiles[1].pos[1] += 20
            self.tiles[2].pos[0] += 40
            self.tiles[2].pos[1] += 20
            self.tiles[3].pos[0] += 60
            self.tiles[3].pos[1] += 20
        elif toop == "tee":
            self.tiles[0].pos[0] += 20
            self.tiles[0].pos[1] += 20
            self.tiles[1].pos[0] += 20
            self.tiles[2].pos[1] += 20
            self.tiles[3].pos[0] += 40
            self.tiles[3].pos[1] += 20
        elif toop == "el":
            self.tiles[0].pos[1] += 20
            self.tiles[1].pos[0] += 20
            self.tiles[1].pos[1] += 20
            self.tiles[2].pos[0] += 40
            self.tiles[2].pos[1] += 20
            self.tiles[3].pos[0] += 40
        elif toop == "jay":
            self.tiles[0].pos[1] += 20
            self.tiles[1].pos[0] += 20
            self.tiles[1].pos[1] += 20
            self.tiles[2].pos[0] += 40
            self.tiles[2].pos[1] += 20
        elif toop == "square":
            self.tiles[0].pos[0] += 20
            self.tiles[1].pos[0] += 20
            self.tiles[1].pos[1] += 20
            self.tiles[2].pos[1] += 20
        self.base = [x.pos.copy() for x in self.tiles]

    def down(self):
        if not self.halted:
            for tile in self.tiles:
                tile.pos[1] += 20
            hit = False
            for tile in self.tiles:
                if tile.pos[1] >= self.game.screen_rect.height:
                    self.halted = True
                    self.terminate()
                    self.game.live_brick = self.game.bricks[0]
                    hit = True
                    break
            if not hit:
                for toil in self.game.tiles:
                    for tile in self.tiles:
                        if toil.rect.collidepoint(tile.pos):
                            self.halter = True
                            self.terminate()
                            self.game.live_brick = self.game.bricks[0]
                            hit = True
                            break
                    if hit:
                        break

    def right(self):
        for tile in self.tiles:
            tile.pos[0] += 20
        hit = False
        for tile in self.tiles:
            if tile.pos[0] >= self.game.screen_rect.width:
                hit = True
            for toil in self.game.tiles:
                if toil.rect.collidepoint(tile.pos):
                    hit = True
                    break
            if hit:
                for tile in self.tiles:
                    tile.pos[0] -= 20
                break

    def left(self):
        for tile in self.tiles:
            tile.pos[0] -= 20
        hit = False
        for tile in self.tiles:
            if tile.pos[0] < 0:
                hit = True
            for toil in self.game.tiles:
                if toil.rect.collidepoint(tile.pos):
                    hit = True
                    break
            if hit:
                for tile in self.tiles:
                    tile.pos[0] += 20
                break

    def spin(self):
        if self.toop == "square":
            return 
        elif self.toop == "line":
            self._linear()
        else:
            centre = self.tiles[self.base.index([20,20])].pos
            for tile in self.tiles:
                pos = tile.pos
                x_more = 0
                y_more = 0
                x_up = 0
                y_up = 0
                if pos[0] < centre[0]:
                    x_more = -1
                elif pos[0] > centre[0]:
                    x_more = 1
                if pos[1] < centre[1]:
                    y_more = -1
                elif pos[1] > centre[1]:
                    y_more = 1
                if x_more == -1 and y_more == -1:
                    x_up = 40
                elif x_more == 0 and y_more == -1:
                    x_up = 20
                    y_up = 20
                elif x_more == 1 and y_more == -1:
                    y_up = 40
                elif x_more == -1 and y_more == 0:
                    x_up = 20
                    y_up = -20
                elif x_more == 1 and y_more == 0:
                    x_up = -20
                    y_up = 20
                elif x_more == -1 and y_more == 1:
                    y_up = -40
                elif x_more == 0 and y_more == 1:
                    x_up = -20
                    y_up = -20
                elif x_more == 1 and y_more == 1:
                    x_up = -40
                tile.pos[0] += x_up
                tile.pos[1] += y_up

    def _linear(self):
        posse = [x.pos for x in self.tiles]
        if [x[1] for x in posse].count(posse[0][1]) == 4:
            for x in range(0,4):
                tile = self.tiles[self.base.index([x*20,20])]
                if x == 0:
                    tile.pos[0] += 20
                    tile.pos[1] -= 40
                elif x == 2:
                    tile.pos[0] -= 20
                    tile.pos[1] -= 20
                elif x == 3:
                    tile.pos[0] -= 40
                    tile.pos[1] += 20
        elif [x[0] for x in posse].count(posse[0][0]) == 4:
            for x in range(0,4):
                tile = self.tiles[self.base.index([x*20,20])]
                if x == 0:
                    tile.pos[0] -= 20
                    tile.pos[1] += 40
                elif x == 2:
                    tile.pos[0] += 20
                    tile.pos[1] += 20
                elif x == 3:
                    tile.pos[0] += 40
                    tile.pos[1] -= 20

    def update(self):
        for tile in self.tiles:
            tile.position()
            self.screen.blit(tile.image, tile.rect)
        pygame.display.flip()

    def terminate(self):
        for tile in self.tiles:
            tile.pos[1] -= 20
            tile.position()
            self.game.tiles.append(tile)
        self.game.bricks.pop(0)
        self.game.bricks.append(Brick(self.game, random.choice(self.game.toops)))

    # Have the bricks donate tiles to central repository and then dissolve the bricks as objects

class Tile:
    """Creates the tiles of which the bricks will be composed"""

    def __init__(self,brick:Brick):
        self.brick = brick
        self.image = pygame.surface.Surface((20,20))
        self.rect = self.image.get_rect()
        self.pos = [0,0]

    def position(self):
        self.rect.topleft = self.pos


if __name__ == "__main__":
    game = Game()
    game.run_game()
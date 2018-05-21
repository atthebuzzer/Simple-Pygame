import os
import pygame
import json
from player import *
from physics import *
from inputs import *
from graphics import *
from math import *
from Wall import *
from EndBlock import *
from Bot import *
from pygame.locals import *

class World(object):
    def __init__(self):
        self.entities = []
        self.platforms = []
        self.players = []
        self.lag = 0
        self.MS_PER_UPDATE = 16

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        pygame.display.set_caption("Simple Game")
        self.screen = pygame.display.set_mode((1280, 720),pygame.NOFRAME)
        pygame.joystick.init()
        self.level = 0
        self.loadAssets()

    def createLevel(self):
        self.entities.clear()
        self.players.clear()
        self.platforms.clear()
        x = y = 0
        square = 20
        rawImage = pygame.image.load('../assets/platform.png').convert()
        enemyImage = pygame.image.load('../assets/enemy.png').convert_alpha()
        currentX = 0
        currentY = 0
        wallCount = 0
        for row in self.CurrentLevel:
            for char in row:
                isWall = False
                if char == 'w':
                    isWall = True
                    wallCount += 1
                    if not currentX and not currentY:
                        currentX = x
                        currentY = y
                if char == 'e':
                    self.end = EndBlock(x, y, square, square)
                    self.end.graphics = EndGraphics(self.screen)
                    self.addEntity(self.end)
                if char == 's':
                    self.start = x, y
                if char == 'b':
                    bot = Bot(DumbBot(self), PhysicsComponent(self), GraphicsComponent(self.screen, enemyImage))
                    bot.rect.center = x, y
                    self.addEntity(bot)
                if currentX or currentY and not isWall:
                    self.platforms.append(Wall(None, None, GraphicsComponent(self.screen, rawImage),currentX,currentY,square * wallCount,square))
                    currentX = currentY = wallCount = 0
                x += square
            y += square
            x = 0
        player = Player(InputComponent2(), PhysicsComponent(self), PlayerGraphics(self.screen))
        player.rect.center = self.start
        self.addEntity(player)

    def loadLevel(self, number):
        f = open(self.data["levels"][number]["path"], "r")
        self.CurrentLevel = f.readlines()
        f.close()
        self.createLevel()

    def loadAssets(self):
        f = open("data.json", "r")
        self.data = json.load(f)
        f.close()

        self.loadLevel(self.level)
        rawImage = pygame.image.load('../assets/forest.jpg').convert()
        self.image = pygame.transform.scale(rawImage, (1280, 720))

    def run(self):
        total = 0
        running = True
        clock = pygame.time.Clock()
        while running:
            time = clock.get_time()
            self.screen.fill((0, 0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False

            if self.end.check(self.players[0]):
                self.level += 1
                self.loadLevel(self.level)
                self.players[0].rect.center = self.start


            if self.players[0].rect.y > 1280 or self.players[0].health <= 0:
                self.createLevel()
                self.players[0].health = 150
                self.players[0].rect.center = self.start

            self.input()
            self.physics(time)
            self.render()
            pygame.display.update()
            clock.tick(60)


    def input(self):
        for e in self.entities:
            e.handleInput()
    def physics(self, time):
        self.lag += time
        while self.lag >= self.MS_PER_UPDATE:
            for e in self.entities:
                e.update(time)
            self.lag -= self.MS_PER_UPDATE
    def render(self):
        self.screen.blit(self.image, (0,0))
        for e in self.entities:
            e.render()

        for platform in self.platforms:
            platform.render()

    def addEntity(self, Entity):
        if type(Entity) == Player:
            self.players.append(Entity)
            Entity.ID = len(self.players)

        self.entities.append(Entity)
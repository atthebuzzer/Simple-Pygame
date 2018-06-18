import os
import pygame
import json
from physics import *
from DumbBot import *
from player import *
from graphics import *
from math import *
from Wall import *
from EndBlock import *
from Bot import *
from KeyBoardInput import *
from GamePadInput import *
from pygame.locals import *
from Camera import *
import random

class World(object):
    def __init__(self):
        self.entities = []
        self.platforms = []
        self.players = []
        self.particles = []
        self.lag = 0
        self.MS_PER_UPDATE = 16

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.mixer.init()
        self.myfont = pygame.font.SysFont("monospace", 34, bold=True)

        pygame.display.set_caption("Simple Game")
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for stick in self.joysticks:
            stick.init()

        self.explosion = pygame.image.load('../assets/spritesheet.png').convert_alpha()
        self.explosionFrames = []
        self.explosionFrames.append(self.explosion.subsurface((0, 0, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((100, 0, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((200, 0, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((300, 0, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((400, 0, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((500, 0, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((600, 0, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((700, 0, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((800, 0, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((900, 0, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((0, 100, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((100, 100, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((200, 100, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((300, 100, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((400, 100, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((500, 100, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((600, 100, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((700, 100, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((800, 100, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((900, 100, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((0, 200, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((100, 200, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((200, 200, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((300, 200, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((400, 200, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((500, 200, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((600, 200, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((700, 200, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((800, 200, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((900, 200, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((0, 300, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((100, 300, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((200, 300, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((300, 300, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((400, 300, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((500, 300, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((600, 300, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((700, 300, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((800, 300, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((900, 300, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((0, 400, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((100, 400, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((200, 400, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((300, 400, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((400, 400, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((500, 400, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((600, 400, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((700, 400, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((800, 400, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((900, 400, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((0, 500, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((100, 500, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((200, 500, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((300, 500, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((400, 500, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((500, 500, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((600, 500, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((700, 500, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((800, 500, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((900, 500, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((0, 600, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((100, 600, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((200, 600, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((300, 600, 100, 100)).copy())
        self.explosionFrames.append(self.explosion.subsurface((400, 600, 100, 100)).copy())
        self.frameIndex = 0
        self.explosionRect = None

        self.loadAssets()
        self.camera = Camera(760, 720)

    def createLevel(self, x, y):
        placementx = x
        placementy = y
        square = 40
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
                        currentX = placementx
                        currentY = placementy
                if char == 'e':
                    self.end = EndBlock(placementx, placementy, square, square)
                    self.end.graphics = EndGraphics(self.screen)
                    self.addEntity(self.end)
                if char == 's':
                    self.start = placementx, placementy
                if char == 'b':
                    bot = Bot(DumbBot(self), PhysicsComponent(self), GraphicsComponent(self.screen, enemyImage))
                    bot.rect.center = placementx, placementy
                    self.addEntity(bot)
                if (currentX or currentY) and not isWall:
                    self.platforms.append(Wall(None, None, GraphicsComponent(self.screen, None),currentX,currentY,square * wallCount,square))
                    currentX = currentY = wallCount = 0
                placementx += square
            placementy += square
            placementx = x

    def loadLevel(self):
        f = open(self.data["start"][random.randint(0, len(self.data["start"]) - 1)]["path"], "r")
        self.CurrentLevel = f.readlines()
        f.close()
        self.entities.clear()
        self.players.clear()
        self.platforms.clear()
        self.platforms.append(Wall(None, None, GraphicsComponent(self.screen, None),0,0,1320,40))
        self.platforms.append(Wall(None, None, GraphicsComponent(self.screen, None),0,0,40,1320))
        self.platforms.append(Wall(None, None, GraphicsComponent(self.screen, None),1320,0,40,1320))

        self.createLevel(40, 40)
        for y in range(0,4):
            for x in range(0,4):
                f = open(self.data["transitional"][random.randint(0, len(self.data["transitional"]) - 1)]["path"], "r")
                self.CurrentLevel = f.readlines()
                f.close()
                self.createLevel(40 * (1 + 8 * x), 40 * (1 + 8 *y))

        player = Player(GamePadInput(self.joysticks[0]), PhysicsComponent(self), PlayerGraphics(self.screen))
        player.rect.center = self.start
        self.addEntity(player)

    def loadAssets(self):
        f = open("data.json", "r")
        self.data = json.load(f)
        f.close()

        self.loadLevel()
        rawImage = pygame.image.load('../assets/game_background_4.png').convert()
        self.image = pygame.transform.scale(rawImage, (1280, 720))


    def run(self):
        total = 0
        running = True
        paused = False
        clock = pygame.time.Clock()

        while running:
            time = clock.get_time()
            pygame.display.set_caption("{:.2f}".format(clock.get_fps()))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                    paused = not paused
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    if GameOver:
                        self.loadLevel()
                        self.players[0].rect.center = self.start
                        GameOver = False


            if len(self.players) and self.end.check(self.players[0]):
                self.loadLevel()
                self.players[0].rect.center = self.start



            if not paused:
                self.input()
                self.physics(time)
            self.camera.update(self.players)
            self.render()

            for player in self.players:
                if player.rect.y > 1320 or player.health <= 0:
                    self.players.remove(player)


            if not len(self.players):
                label = self.myfont.render("Game Over", 1, (255,255,255))
                self.screen.blit(label, (1280 // 2 - label.get_rect().right, 720 // 2 - label.get_rect().h))
                GameOver = True

            pygame.display.update()
            clock.tick(60)


    def input(self):
        for e in self.entities:
            e.handleInput()
            if e.health <= 0:
                self.explosionRect = e.rect
                self.entities.remove(e)
                self.particles.append(self.explosionFrames)
                self.frameIndex = 0
        for player in self.players:
            player.renew(self)

    def physics(self, time):
        self.lag += time
        while self.lag >= self.MS_PER_UPDATE:
            for e in self.entities:
                e.update(time)
            self.lag -= self.MS_PER_UPDATE
    def render(self):
        self.screen.blit(self.image, (0,0))
        for e in self.entities:
            e.render(self.camera)
        for platform in self.platforms:
            platform.render(self.camera)
        for particles in self.particles:
            self.explosionRect.size = particles[self.frameIndex].get_rect().size
            self.screen.blit(particles[self.frameIndex], self.explosionRect.move(self.camera.camera.topleft))
            self.frameIndex += 1
            if self.frameIndex == len(particles) - 1:
                self.particles.remove(particles)

        if len(self.players):
            for hitpoint in range(self.players[0].maxHealth):
                if hitpoint + 1 <= self.players[0].health:
                    pygame.draw.rect(self.screen, (255, 0, 0), (20 + hitpoint * 23, int(720 * 0.025), 20, 20))
                pygame.draw.rect(self.screen, (255, 255, 255), (20 + hitpoint * 23, int(720 * 0.025), 20, 20), 2)


    def addEntity(self, Entity):
        if type(Entity) == Player:
            self.players.append(Entity)
            Entity.ID = len(self.players)

        self.entities.append(Entity)
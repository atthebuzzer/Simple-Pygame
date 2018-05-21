
import pygame
import time
from math import *
from physics import *
from graphics import *
from entity import *

class Projectile(Entity):
    def __init__(self,  _input, _physics, _graphics, velocity):
        super(Projectile, self).__init__(_input, _physics, _graphics)
        self.velocity = velocity
        self.position = [0,0]
        self.rect = pygame.Rect(0,0,10,10)
        self.age = 200


class InputComponent(object):

    def __init__(self):
        self.isPressed = False
        self.held = False
        self.boost = False
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.joysticks[0].init()

    def update(self, Entity):
        key = pygame.key.get_pressed()
        button = self.joysticks[0].get_button(1)
        self.boost = False
        if not button:
            self.isPressed = False
            if Entity.velocity[1] < 0 and Entity.state == 1:
                Entity.velocity[1] *= 0.35

        if button and not self.isPressed:
            self.isPressed = True
            if Entity.state == 0:
                Entity.velocity[1] = Entity.jump
                Entity.state = 1
            elif Entity.state == 1:
                Entity.state = 2
                Entity.velocity[1] = -325
            else:
                pass


        if self.joysticks[0].get_axis(2) <= -0.85 and self.joysticks[0].get_axis(2) >= -1.0:
            self.boost = True

        if self.joysticks[0].get_axis(0) < -0.25:
            Entity.velocity[0] = -150
            if self.boost and Entity.velocity[0] > -280:
                Entity.velocity[0] *= 1.4

        if self.joysticks[0].get_axis(0) > 0.25:
            Entity.velocity[0] = 185
            if self.boost and Entity.velocity[0] < 280:
                Entity.velocity[0] *= 1.4

class InputComponent2(object):

    def __init__(self):
        self.isUpPressed = False
        self.isDashPressed = False
        self.state = 0
        self.DashTime = 0
        self.isFacingRight = True
        self.canDash = True

    def update(self, Entity):
        key = pygame.key.get_pressed()
        current = 0
        if not key[pygame.K_w]:
            self.isUpPressed = False
            if Entity.velocity[1] < 0 and Entity.state == 1:
                Entity.velocity[1] *= 0.35
        if not key[pygame.K_f]:
            self.isDashPressed = False


        if self.state == 1:
            if self.DashTime > 0:
                if not self.isFacingRight:
                    Entity.velocity = [-350, 0]
                else:
                    Entity.velocity = [350, 0]
            self.DashTime -= 1
            if self.DashTime <= 0:
                self.state = 0

        if Entity.state == 0: self.canDash = True
        if key[pygame.K_w] and not self.isUpPressed:
            self.isUpPressed = True
            if Entity.state == 0:
                Entity.velocity[1] = -350
                Entity.state = 1
            elif Entity.state == 1:
                Entity.velocity[1] = -325
                Entity.state = 2
            else:
                pass

        if key[pygame.K_a] and self.state != 1:
            Entity.velocity[0] = -150
            self.isFacingRight = False
        if key[pygame.K_d] and self.state != 1:
            Entity.velocity[0] = 150
            self.isFacingRight = True

        if key[pygame.K_f] and not self.isDashPressed and self.canDash:
            self.isDashPressed = True
            if self.state == 0:
                self.DashTime = 10
                self.state = 1
                self.canDash = False

class BotInput(object):
    def __init__(self, world, screen):
        self.world = world
        self.screen = screen
        self.magnitude = 8

    def update(self, Entity):
        for e in self.world.players:
            x = e.rect.centerx - Entity.rect.centerx
            y = e.rect.centery - Entity.rect.centery
            normalizer = sqrt(pow(x, 2) + pow(y, 2))
            if normalizer == 0:
                normalizer = 0.01
            if Entity.inRange:
                Entity.rect.centerx += (x / normalizer) * 2
                Entity.rect.centery += (y / normalizer) * 2
            if normalizer <= Entity.range:
                Entity.inRange = True

class DumbBot(object):
    def __init__(self, world):
        self.direction = 1
        self.players = world.players
        self.state = 0

    def update(self, Entity):

        Entity.velocity[0] = 100 * self.direction
        if Entity.state == 0:
            Entity.velocity[1] = -250
            Entity.state = 1
            self.direction = 1
            if Entity.rect.x > self.players[0].rect.x:
                self.direction = -1

        for player in self.players:
            if Entity.rect.colliderect(player.rect):
                player.health = 0
                time.sleep(0.25)

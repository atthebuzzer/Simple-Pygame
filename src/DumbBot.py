
import pygame
import time
from math import *
from physics import *
from graphics import *
from entity import *



class DumbBot(object):
    def __init__(self, world):
        self.direction = 1
        self.players = world.players
        self.state = 0
        self.hit = pygame.mixer.Sound("../assets/SFX_Hit03.ogg")

    def update(self, Entity):

        Entity.velocity[0] = 100 * self.direction
        if Entity.isOnGround:
            Entity.velocity[1] = -250
            if len(self.players) and abs(Entity.rect.centerx - self.players[0].rect.centerx) <= 300 and abs(Entity.rect.centery - self.players[0].rect.centery) <= 75:
                if Entity.rect.x > self.players[0].rect.x:
                    self.direction = -1
            else:
                self.direction *= -1


        for player in self.players:
            if Entity.rect.colliderect(player.rect) and not player.invincibility:
                player.health -= 1
                player.invincibility = 60
                player.velocity[1] = -150
                player.velocity[0] = 1600 * self.direction
                self.hit.play()
                break

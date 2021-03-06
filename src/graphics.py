import pygame


class GraphicsComponent(object):
    def __init__(self, screen, image):
        self.screen = screen
        self.image = image

    def update(self, Entity):
        newImage = pygame.transform.scale(self.image, (Entity.rect.w, Entity.rect.h))
        pygame.draw.rect(self.screen, (255, 200, 0), Entity.rect, 0)
        self.screen.blit(newImage, Entity.rect.topleft)

class PlayerGraphics(object):
    def __init__(self, screen):
        self.screen = screen
        self.color = (255,255,255)
    def update(self, Entity):
        green = Entity.health
        if green < 0:
            green = 0

        self.color = (150 - green, green, 0)
        pygame.draw.rect(self.screen, self.color, Entity.rect)



class BotGraphics(object):
    def __init__(self, screen):
        self.screen = screen
        self.area = True
        self.red = 155

    def update(self, Entity):
        if self.area:
            pygame.draw.circle(self.screen, (255,255,255), Entity.rect.center, Entity.range, 1)

        self.red = 155
        Entity.rect.w, Entity.rect.h = 5,5
        if Entity.inRange:
            self.red = 255

        pygame.draw.rect(self.screen, (self.red, 155, 155), Entity.rect, 0)
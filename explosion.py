import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):

    def __init__(self, ai_settings, screen, isalien, isufo):
        super(Explosion, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.isalien = isalien
        self.isufo = isufo

        self.image = pygame.image.load('images/explosion_01.png')

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

        self.frameCount = 0

    def blitme(self):
        # Draw the alien at its current location
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.isufo:
            self.x += self.ai_settings.alien_speed_factor
            self.rect.x = self.x
        elif self.isalien:
            self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
            self.rect.x = self.x

        self.frameCount = self.frameCount + 1

        if self.frameCount == 6:
            self.image = pygame.image.load('images/explosion_02.png')
        elif self.frameCount == 12:
            self.image = pygame.image.load('images/explosion_03.png')
        elif self.frameCount == 18:
            self.image = pygame.image.load('images/explosion_04.png')
        elif self.frameCount == 24:
            self.image = pygame.image.load('images/explosion_05.png')
        elif self.frameCount == 30:
            self.image = pygame.image.load('images/explosion_06.png')
        elif self.frameCount == 36:
            self.image = pygame.image.load('images/explosion_07.png')
        elif self.frameCount == 42:
            self.image = pygame.image.load('images/explosion_08.png')
        elif self.frameCount == 48:
            self.image = pygame.image.load('images/explosion_09.png')
        elif self.frameCount == 54:
            self.image = pygame.image.load('images/explosion_10.png')
        elif self.frameCount == 60:
            self.kill()

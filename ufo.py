import pygame
from pygame.sprite import Sprite


class Ufo(Sprite):

    def __init__(self, ai_settings, screen):
        # Initialize the alien and set its starting position
        super(Ufo, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/ufo.png')

        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        # Draw the alien at its current location
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        # Return True if alien is at edge of screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += self.ai_settings.alien_speed_factor
        self.rect.x = self.x

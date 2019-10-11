import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    # A class to represent a single alien in the fleet

    def __init__(self, ai_settings, screen, alientype):
        # Initialize the alien and set its starting position
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.alientype = alientype

        # Load the alien image and set its rect attribute

        # Alien.bmp taken from Python Crash Course book
        if alientype == "type1":
            self.imageString = "images/alien1.png"
            self.image = pygame.image.load('images/alien1.png')
        elif alientype == "type2":
            self.imageString = "images/alien2.png"
            self.image = pygame.image.load('images/alien2.png')
        else:
            self.imageString = "images/alien3.png"
            self.image = pygame.image.load('images/alien3.png')

        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

        self.frameCount = 0

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
        # Move the alien right or left
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.frameCount = self.frameCount + 1

        if self.frameCount >= 20:
            self.frameCount = 0
            if self.imageString == "images/alien1.png":
                self.imageString = "images/alien1alt.png"
            elif self.imageString == "images/alien1alt.png":
                self.imageString = "images/alien1.png"
            elif self.imageString == "images/alien2.png":
                self.imageString = "images/alien2alt.png"
            elif self.imageString == "images/alien2alt.png":
                self.imageString = "images/alien2.png"
            elif self.imageString == "images/alien3.png":
                self.imageString = "images/alien3alt.png"
            elif self.imageString == "images/alien3alt.png":
                self.imageString = "images/alien3.png"
            self.image = pygame.image.load(self.imageString)

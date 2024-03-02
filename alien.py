import pygame as pyg
from pygame.sprite import Sprite

class Alien(pyg.sprite.Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, screen, ai_settings, image):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pyg.image.load('img/aliens/' + image)
        self.rect = self.image.get_rect()
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the alien's exact position.
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        if self.rect.right >= self.screen.get_rect().right:
            return True
        elif self.rect.left <= 0:
            return True
        return False

    def update(self):
        """Move the alien to the right or left."""
        self.x += (self.ai_settings.alien_speed_factor *  self.ai_settings.fleet_direction)
        self.rect.x = int(self.x)

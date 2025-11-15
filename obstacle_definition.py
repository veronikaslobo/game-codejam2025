import pygame
from pygame.examples.cursors import image

# defining images
glacier_img = pygame.image.load("obstacles/glacier1.png")

class Obstacle:
    def __init__(self, image, x, y, obstacle_type, damage=1):
        self.image = image
        self.x = x              # Horizontal position
        self.y = y              # Vertical position
        self.width = OBSTACLE_WIDTH    # Width of the obstacle
        self.height = OBSTACLE_HEIGHT  # Height of the obstacle
        self.type = obstacle_type       # Type identifier (e.g., 'ice_spike', 'snowball')
        self.damage = damage           # Damage or effect on player
        self.active = True             # Whether the obstacle is active in the game

    def update(self, speed): # moves down (with game speed)
        self.y += speed

    def draw(self, screen):
        screen.blit(self.image, [self.x, self.y])

import pygame
import random

# initializing environment
pygame.init()

# CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50,50
PLAYER_WIDTH, PLAYER_HEIGHT = 50,50

# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (189,228,255)
PURPLE =(207,169,245)
YELLOW =(254,234,160)

# background


# obstacles

# creating obstacles array form pictures
glacier_img = pygame.image.load("obstacles/glacier1.png")

class Obstacle:
    def __init__(self, x, y, obstacle_type, damage=1):
        self.x = x              # Horizontal position
        self.y = y              # Vertical position
        self.width = OBSTACLE_WIDTH    # Width of the obstacle
        self.height = OBSTACLE_HEIGHT  # Height of the obstacle
        self.type = obstacle_type       # Type identifier (e.g., 'ice_spike', 'snowball')
        self.damage = damage           # Damage or effect on player
        self.active = True             # Whether the obstacle is active in the game

    def update(self, speed): # moves down (with game speed)
        self.y += speed

    def appearance(self, screen):
        random



# initialize environment
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


#running the game
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill(BLUE)

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, PURPLE, (250, 250), 75)


    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
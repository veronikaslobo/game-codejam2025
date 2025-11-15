import pygame
import random
from obstacle_definition import Obstacle, spawn_obstacle, obs_imgs, LANES

# initializing environment
pygame.init()

# CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (189, 228, 255)
PURPLE = (207, 169, 245)
YELLOW = (254, 234, 160)

# background


# initialize environment
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
obstacles = []
spawn_timer = 0
game_speed = 5

# running the game
running = True
while running:
    # clock and timer
    clock.tick(FPS)
    spawn_timer += 1

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white

    # generate obstacles
    # #pygame.draw.circle(screen, PURPLE, (250, 250), 75)
    if spawn_timer > 90:
        obstacles.append(spawn_obstacle())
        spawn_timer = 0
    # Update and draw obstacles
    for obs in obstacles:
        obs.update()
        obs.draw(screen)
    # Remove off-screen obstacles
    obstacles = [obs for obs in obstacles if obs.rect.top <= SCREEN_HEIGHT]

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
import pygame
import random
import player
from background import scroll_bg
from obstacle_definition import Obstacle, spawn_obstacle, obs_imgs, LANES
from background import scroll_bg

# initializing environment
pygame.init()
clock = pygame.time.Clock()

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


# initialize environment
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


#running the game
running = True
while running:
    # clock and timer
    clock.tick(FPS)
    spawn_timer += 1

    scroll_bg()

<<<<<<< HEAD
=======
    # Fill background
    scroll_bg()

    # generate obstacles
>>>>>>> e6cccbd8966e24f8c1939be6909ef1544aac1be4
    if spawn_timer > 100:
        obstacles.append(spawn_obstacle())
        spawn_timer = 0
        # Update and draw obstacles
    for obs in obstacles:
        obs.update()
        obs.draw(screen)
        # Remove off-screen obstacles
    obstacles = [obs for obs in obstacles if obs.rect.top <= SCREEN_HEIGHT]

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background

    # generate obstacles


    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
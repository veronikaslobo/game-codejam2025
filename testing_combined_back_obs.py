import pygame
import random
from player import Player,player_move
from combined_game_environment import Obstacle, spawn_obstacle, obs_imgs, LANES, scroll_bg, get_background

# initializing environment
pygame.init()

# CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60


# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (189,228,255)
PURPLE =(207,169,245)
YELLOW =(254,234,160)


# initialize environment
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
obstacles = []
spawn_timer = 0
GAME_SPEED = 5
bg = get_background()
scroll = 0
penguin = Player()


#running the game
running = True
while running:
    # clock and timer
    clock.tick(FPS)
    spawn_timer += 1

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    scroll = scroll_bg(screen, bg, scroll, GAME_SPEED)

    # adding the penguin movement
    player_move(penguin)
    penguin.update()
    penguin.draw(screen)

    # generate obstacles
    if spawn_timer > 90:
        obstacles.append(spawn_obstacle(GAME_SPEED))
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
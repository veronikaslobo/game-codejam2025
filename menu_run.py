import pygame
import random
import player
import threading
import sys
import math
import time

from button import Button
from combined_game_environment import Obstacle, spawn_obstacle, obs_imgs, LANES, scroll_bg, get_background
from loosing_screen import check_for_collision
from player import Player, player_move

# initialize environment
pygame.init()

# CONSTANTS and presetting values
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
obstacles = []
spawn_timer = 0
GAME_SPEED = 5
score = 0
scroll = 0
game_start_time = 0
survival_time = 0

# COLORS
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
BLUE   = (189, 228, 255)
PURPLE = (207, 169, 245)
YELLOW = (254, 234, 160)

# create base objects
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = get_background()
penguin = Player()

# initialize environment
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game name")

# menu background
menu_bg = pygame.image.load("images/babyblue.png")
menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# game background (scrolling)
BG_IMAGE = pygame.image.load("images/background.png").convert()
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
BG_HEIGHT = BG_IMAGE.get_height()

# avoid absolute path if possible
BUTTON_IMG = pygame.image.load("images/button.png").convert()
BUTTON_IMG = pygame.transform.scale(BUTTON_IMG, (150, 75))

scroll = 0  # vertical offset

font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)


def print_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def show_game_over_screen(current_score):
    """Block until user presses SPACE or closes the window."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # return to caller, which will reset the game

        screen.fill(BLACK)
        print_text('GAME OVER', font_big, WHITE, 130, 200)
        print_text('SCORE: ' + str(current_score) + ' m', font_big, WHITE, 130, 250)
        print_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)

        pygame.display.flip()
        clock.tick(FPS)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("images/font.ttf", size)


def play():
    global score, scroll, game_start_time
    game_start_time = pygame.time.get_ticks()

    # initial state for a run
    score = 0
    scroll = 0
    spawn_timer = 0
    obstacles = []
    collisions = 0
    damage_cooldown = 0.0
    is_game_over = False

    running = True
    while running:
        dt = clock.tick(FPS) /1000

        if damage_cooldown > 0:
            damage_cooldown -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not is_game_over:
            spawn_timer += 1

            # Fill background
            scroll = scroll_bg(screen, bg, scroll, GAME_SPEED)

            # adding the penguin movement
            player_move(penguin)
            penguin.update(dt)
            penguin.draw(screen)

            # generate obstacles
                        # generate obstacles
            if spawn_timer > 90:
                obstacles.append(spawn_obstacle(GAME_SPEED))
                spawn_timer = 0

            # Update, draw, and check collisions
            for obs in obstacles[:]:  # iterate over a copy so we can remove
                obs.update()
                obs.draw(screen)

                # only take damage if cooldown is over
                if damage_cooldown <= 0 and check_for_collision(penguin, obs):
                    collisions += 1
                    damage_cooldown = 1.0  # 1 second of invincibility
                    obstacles.remove(obs)  # remove that obstacle so it can't hit again

                    if collisions >= 3:
                        is_game_over = True
                        break  # no need to check other obstacles this frame

            # Remove off-screen obstacles
            obstacles = [obs for obs in obstacles if obs.rect.top <= SCREEN_HEIGHT]


            if is_game_over:
                survival_time = (pygame.time.get_ticks() - game_start_time) / 1000.0 #millisecodns divided to get seconds
                score = int(survival_time * 15) # Constant can be changed
                game_start_time = pygame.time.get_ticks()



            # Remove off-screen obstacles
            obstacles = [obs for obs in obstacles if obs.rect.top <= SCREEN_HEIGHT]

        else:
            # show game over screen, wait for space
            show_game_over_screen(score)
            # reset run
            score = 0
            scroll = 0
            obstacles.clear()
            collisions = 0
            is_game_over = False

        pygame.display.flip()


def menu():
    while True:
        screen.blit(menu_bg, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=BUTTON_IMG, x_pos=400, y_pos=250, text_input="PLAY")
        QUIT_BUTTON = Button(image=BUTTON_IMG, x_pos=400, y_pos=350, text_input="QUIT")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# running the game
menu()
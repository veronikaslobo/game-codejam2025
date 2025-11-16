import pygame
import random
import player
import threading
import sys
import math
import time

from button import Button
from obstacle_definition import Obstacle, spawn_obstacle, obs_imgs, LANES
from loosing_screen import check_for_collision

pygame.init()
clock = pygame.time.Clock()

game_start_time = 0
survival_time = 0

# CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
GAME_SPEED = 5

score = 0

# COLORS
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
BLUE   = (189, 228, 255)
PURPLE = (207, 169, 245)
YELLOW = (254, 234, 160)

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
        print_text('SCORE: ' + str(current_score), font_big, WHITE, 130, 250)
        print_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)

        pygame.display.flip()
        clock.tick(FPS)


def scroll_bg():
    global scroll
    scroll = (scroll + 5) % BG_HEIGHT
    screen.blit(BG_IMAGE, (0, scroll - BG_HEIGHT))
    screen.blit(BG_IMAGE, (0, scroll))


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("images/font.ttf", size)


def play():
    global score, scroll, game_start_time, survival_time

    # initial state for a run
    score = 0
    scroll = 0
    spawn_timer = 0
    obstacles = []
    collisions = 0
    is_game_over = False

    # TODO: create your player object here
    # e.g. player_obj = player.Player(...)

    running = True
    while running:
        game_start_time = pygame.time.get_ticks()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not is_game_over:
            # background
            scroll_bg()

            # TODO: update and draw player here
            # player_obj.update()
            # player_obj.draw(screen)

            # spawn obstacles
            spawn_timer += 1
            if spawn_timer > 100:
                obstacles.append(spawn_obstacle())
                spawn_timer = 0

            # update & draw obstacles
            for obs in obstacles:
                obs.update()
                obs.draw(screen)

            obstacles = [obs for obs in obstacles if obs.rect.top <= SCREEN_HEIGHT]

            # --- COLLISION CHECK (FIX THIS LINE TO MATCH YOUR FUNCTION SIGNATURE) ---
            # Example if your function expects (player_rect, obstacles):
            # if check_for_collision(player_obj.rect, obstacles):
            if check_for_collision():  # <-- REPLACE WITH REAL ARGS
                collisions += 1

            if collisions >= 3:
                is_game_over = True

            if is_game_over:
                survival_time = (pygame.time.get_ticks() - game_start_time) / 1000.0 #millisecodns divided to get seconds
                score = survival_time * 15 # Constant can be changed

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
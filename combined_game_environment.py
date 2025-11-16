import pygame
import math
import random


# initializing and constants
pygame.init()

LANES=[140, 600,350]
TARGET_SIZE_O =(100,100)

clock = pygame.time.Clock()
FPS = 60
scroll = 0

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# defining images --objects
glacier = pygame.image.load("images/glacier1.png").convert_alpha()
glacier_img = pygame.transform.scale(glacier,TARGET_SIZE_O)

glacier_puddle = pygame.image.load("images/glacier_puddle.png").convert_alpha()
ice_puddle_img = pygame.transform.scale(glacier_puddle,TARGET_SIZE_O)

snow = pygame.image.load("images/snow_pile.png").convert_alpha()
snow_pile_img = pygame.transform.scale(snow,TARGET_SIZE_O)

trees = pygame.image.load("images/trees.png").convert_alpha()
trees_img = pygame.transform.scale(trees,TARGET_SIZE_O)

moose = pygame.image.load("images/moose.png").convert_alpha()
moose_img = pygame.transform.scale(moose,TARGET_SIZE_O)

# obstacle images array
obs_imgs = [glacier_img,ice_puddle_img,moose_img,snow_pile_img,trees_img, ice_puddle_img, glacier_img]

#getting background image
def get_background():
    bg_image = pygame.image.load("images/background.png").convert()
    return pygame.transform.scale(bg_image, (800, 600))

def scroll_bg(screen,bg, scroll,GAME_SPEED):
    pygame.display.set_caption("Game name")

    bg_width = bg.get_width()
    bg_height = bg.get_height()

    tiles = math.ceil(SCREEN_HEIGHT / bg_width) + 1
    scroll = (scroll + GAME_SPEED) % bg_height

    screen.blit(bg, (0, scroll - bg_height))
    screen.blit(bg, (0, scroll))
    return scroll



class Obstacle:
    def __init__(self, image, x, y,speed):
        self.image = image
        self.rect = image.get_rect(topleft=(x,y))    # track image place by putting it on a rect object
        self.width = self.rect.width
        self.height = self.rect.height
        self.speed = speed
        self.active = True             # Whether the obstacle is active in the game

    def update(self): # moves down (with game speed)
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # maps image to rect position


def spawn_obstacle(GAME_SPEED):
    image = random.choice(obs_imgs)
    x = random.choice(LANES)
    y = -image.get_height()
    obstacle = Obstacle(image, x, y, GAME_SPEED)
    return obstacle


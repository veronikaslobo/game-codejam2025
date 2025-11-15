import pygame
import random

# initializing and constants
pygame.init()
LANES=[200, 400,300]
TARGET_SIZE =(100,100)
screen = pygame.display.set_mode((800, 600))

# defining images
glacier = pygame.image.load("images/glacier1.png").convert_alpha()
glacier_img = pygame.transform.scale(glacier,TARGET_SIZE)

glacier_puddle = pygame.image.load("images/glacier_puddle.png").convert_alpha()
ice_puddle_img = pygame.transform.scale(glacier_puddle,TARGET_SIZE)

# obstacle images array
obs_imgs = [glacier_img,ice_puddle_img]

class Obstacle:
    def __init__(self, image, x, y,speed):
        self.image = image
        self.rect = image.get_rect(topleft=(x,y))    # track image place by putting it on a rect object
        self.speed = speed #NEED TO DEFINE GAME SPEED
        self.active = True             # Whether the obstacle is active in the game

    def update(self): # moves down (with game speed)
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # maps image to rect position


def spawn_obstacle():
    image = random.choice(obs_imgs)
    x = random.choice(LANES) #NEED TO DEFINE X POSITIONS
    y = -image.get_height()
    obstacle = Obstacle(image, x, y, GAME_SPEED)
    return obstacle


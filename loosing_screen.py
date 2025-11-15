import pygame
from player import Player

class Obstacle:
    def __init__(self, image, x, y,speed):
        self.image = image
        self.rect = image.get_rect(topleft=(x,y))    # track image place by putting it on a rect object
        self.speed = speed
        self.active = True             # Whether the obstacle is active in the game

    def update(self): # moves down (with game speed)
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # maps image to rect position

def check_for_collision(player, obstacle):
    player_left = player.x_axis_position
    player_right = player.x_axis_position + player.width


    obstacle_left =
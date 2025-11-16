import pygame
from player import Player


collide = 0


class Obstacle:
    def __init__(self, image, x, y,speed):
        self.image = image
        self.rect = image.get_rect(topleft=(x,y))    # track image place by putting it on a rect object
        self.width = self.rect.width
        self.speed = speed
        self.active = True  # Whether the obstacle is active in the game

    def update(self): # moves down (with game speed)
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # maps image to rect position


def check_for_collision(player, obstacle):
    # Player bounding box
    player_left   = player.x_axis_position
    player_top    = player.y_axis_position
    player_right  = player_left + player.width
    player_bottom = player_top  + player.height

    # Obstacle bounding box, use rect directly
    rect = obstacle.rect
    obstacle_left   = rect.left
    obstacle_top    = rect.top
    obstacle_right  = rect.right
    obstacle_bottom = rect.bottom

    if (player_right  > obstacle_left and
        player_left   < obstacle_right and
        player_bottom > obstacle_top and
        player_top    < obstacle_bottom):
        return True

    return False


    # updates the collide variable

import pygame
from player import Player
from combined_game_environment import Obstacle


def check_for_collision(player, obstacle):
    player_left = player.x_axis_position
    player_right = player.x_axis_position + player.width
    player_top = player.y_axis_position
    player_bottom = player.y_axis_position + player.height

    obstacle_left = obstacle.rect.x
    obstacle_right = obstacle.rect.x + obstacle.width
    obstacle_top = obstacle.rect.y
    obstacle_bottom = obstacle.rect.y + obstacle.height

    if (player_right > obstacle_left and
        player_left < obstacle_right and
        player_bottom > obstacle_top and
        player_top < obstacle_bottom):
        return True

    return False

import pygame
import numpy
import math
import os

pygame.init()

# Test window for car
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Movement")
timer = pygame.time.Clock()
fps = 60

# Class of our car (can be smt else, decide later)
class Player:
    def __init__(self, x,, image_path):
        self.x_axis_position = x
        self.y_axis_position = HEIGHT / 10 # to see with the UI
        self.wi

# main game
def main():

# closes the game if the user presses on X
    run = True
    screen.fill('black')
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False



pygame.quit()



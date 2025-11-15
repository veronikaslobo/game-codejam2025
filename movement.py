import pygame
import numpy
import math

pygame.init()

# Test window for car
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Movement")
timer = pygame.time.Clock()
fps = 60

# Class of our car (can be smt else, decide later)
class Car:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y

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



import pygame
import numpy
import math

pygame.init()

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



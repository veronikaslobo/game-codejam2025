import pygame
import numpy
import math

pygame.init()



class Car:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y

# main game
def main():

# closes the game if the user presses on X
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False



pygame.quit()



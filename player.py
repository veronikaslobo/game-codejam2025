import pygame
import numpy
import math
import os
# import mediapipe as mp

pygame.init()

# Test window for car
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Movement")
timer = pygame.time.Clock()
fps = 60
LEFT_LANE_POSITION = 140
MIDDLE_LANE_POSITION = 350
RIGHT_LANE_POSITION = 600

# Class of our car (can be smt else, decide later)
class Player:
    def __init__(self):
        self.y_axis_position = 8.7 * HEIGHT / 10 # to see with the UI
        self.width = 75
        self.height = 75
        self.lane_width = WIDTH // 3
        self.current_lane = 1
        self.lane_positions = [LEFT_LANE_POSITION, MIDDLE_LANE_POSITION, RIGHT_LANE_POSITION]
        self.x_axis_position = self.lane_positions[self.current_lane]
        self.target_x = self.x_axis_position
        self.slide_speed = 0.07 # pixels/movement
        self.is_moving = False

        image_path = "player/penguin_image1.png"

        #Checks for filenotfound
        if not os.path.exists(image_path):
            print(f"Error: Could not find {image_path}")
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
        else:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    # Drawing itself on the map
    def draw(self, surface):
        surface.blit(self.image, (self.x_axis_position, self.y_axis_position))



    def move_right(self):
        if self.current_lane < 2 and not self.is_moving:
            self.current_lane += 1
            self.target_x = self.lane_positions[self.current_lane]
            self.is_moving = True


    def move_left(self):
        if self.current_lane > 0:
            self.current_lane -= 1
            self.target_x = self.lane_positions[self.current_lane]
            self.is_moving = True

    def update(self):
        self.x_axis_position += (self.target_x - self.x_axis_position) * self.slide_speed

        if abs(self.target_x - self.x_axis_position) < 0.5:
            self.x_axis_position = self.target_x
            self.is_moving = False


    # def accelerate(self):



def player_move(penguin):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                penguin.move_right()
            if event.key == pygame.K_LEFT:
                penguin.move_left()
    return False



# main game
#def main():
#
 #   peng = Player()
  #  game_over = False

# closes the game if the user presses on X
   # run = True


#    while run:
 #       for event in pygame.event.get():
  #          if event.type == pygame.QUIT:
   #             run = False
    #        if event.type == pygame.KEYDOWN:
     #           if event.key == pygame.K_RIGHT:
      #              peng.move_right()
       #         if event.key == pygame.K_LEFT:
        #            peng.move_left()

#        peng.update()
#        screen.fill((250,250,204))
#        peng.draw(screen)
#        pygame.display.flip()


#main()

#pygame.quit()



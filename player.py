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
LEFT_LANE_POSITION = 155
MIDDLE_LANE_POSITION = 400
RIGHT_LANE_POSITION = 630

class Player:
    def __init__(self):
        self.width = 75
        self.height = 75

        # x positions fro lane centers
        self.lane_positions = [LEFT_LANE_POSITION, MIDDLE_LANE_POSITION, RIGHT_LANE_POSITION]
        self.current_lane = 1

        # coords for player (spawned topleft)
        self.x_axis_position = self.lane_positions[self.current_lane] - self.width // 2
        self.y_axis_position = 8.7 * HEIGHT / 10

        # movement parameters
        self.slide_speed = 900   # increase for stronger sliding
        self.target_x = self.x_axis_position
        self.is_moving = False

        # dget img to draw
        image_path = "player/penguin_image1.png"
        if not os.path.exists(image_path):
            print(f"Error: Could not find {image_path}")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 0))
        else:
            img = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(img, (self.width, self.height))

    def draw(self, surface):
        surface.blit(self.image, (int(self.x_axis_position), int(self.y_axis_position)))

    def move_right(self):
        if not self.is_moving and self.current_lane < 2:
            self.current_lane += 1
            self.target_x = self.lane_positions[self.current_lane] - self.width // 2
            self.is_moving = True

    def move_left(self):
        if not self.is_moving and self.current_lane > 0:
            self.current_lane -= 1
            self.target_x = self.lane_positions[self.current_lane] - self.width // 2
            self.is_moving = True

    def update(self, dt):
        if self.is_moving:
            direction = self.target_x - self.x_axis_position
            move_step = self.slide_speed * dt

            if abs(direction) <= move_step:
                self.x_axis_position = self.target_x
                self.is_moving = False
            else:
                self.x_axis_position += move_step if direction > 0 else -move_step



def player_move(penguin):
    keys = pygame.key.get_pressed()

    # right move
    if keys[pygame.K_RIGHT]:
        penguin.move_right()

    # left move
    elif keys[pygame.K_LEFT]:
        penguin.move_left()

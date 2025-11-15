import pygame 

pygame.init()

clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game name")

run = True

bg = pygame.image.load

while run:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
pygame.quit()
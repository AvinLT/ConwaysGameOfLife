import pygame, sys
from pygame.locals import *

# import random

clock = pygame.time.Clock()  # initialize clock
pygame.init()  # initialize pygame

WINDOW_SIZE = (704, 512)  # window size
display = pygame.Surface((704, 512))  # what we display images on.
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize window

COLOR = [255, 255, 255]


class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y


while True:  # Main game loop

    display.fill((0, 0, 0))  # makes screen black

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # checks if window is closed
            pygame.quit()  # stops pygame
            sys.exit()  # stops script

    # start here

    # end here

    pygame.display.update()  # update display
    mainDisplay = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(mainDisplay, (0, 0))

    clock.tick(60)  # set frame rate

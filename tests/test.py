import pygame, sys
from pygame.locals import *
import random

clock = pygame.time.Clock()  # initialize clock
pygame.init()  # initialize pygame

WINDOW_SIZE = (704, 512)  # window size
display = pygame.Surface((704, 512))  # what we display images on.
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize window

COLOR = [255, 255, 255]

x = 250
y = 250
size = 50
testRect = pygame.Rect(x, y, 50, 50)
sideHit = False
rand = [1, 1]
mult = 3
tempx, tempy = 0, 0

print("HII")
while True:  # Main game loop

    display.fill((0, 0, 0))  # makes screen black

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # checks if window is closed
            pygame.quit()  # stops pygame
            sys.exit()  # stops script

    # start here
    if x + size > WINDOW_SIZE[0]:
        x = WINDOW_SIZE[0] - size
        sideHit = True
    elif x < 0:
        x = 0
        sideHit = True

    if y + size > WINDOW_SIZE[1]:
        y = WINDOW_SIZE[1] - size
        sideHit = True
    elif y < 0:
        y = 0
        sideHit = True

    if sideHit:
        rand = [(random.randint(-100, 100) / 100) * mult, (random.randint(-100, 100) / 100) * mult]
        sideHit = False

        COLOR = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    tempx += rand[0]
    tempy += rand[1]

    if abs(tempx) > 1:
        if tempx > 0:
            x += 1
            tempx -= 1
        else:
            x -= 1
            tempx += 1

    if abs(tempy) > 1:
        if tempy > 0:
            y += 1
            tempy -= 1
        else:
            y -= 1
            tempy += 1

    pygame.draw.rect(display, COLOR, (x, y, size, size))
    # end here

    pygame.display.update()  # update display
    mainDisplay = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(mainDisplay, (0, 0))

    clock.tick(60)  # set frame rate

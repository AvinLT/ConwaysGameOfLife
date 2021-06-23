import pygame, sys
from pygame.locals import *

# import random

clock = pygame.time.Clock()  # initialize clock
pygame.init()  # initialize pygame

WINDOW_SIZE = (770, 600)  # window size
display = pygame.Surface((770, 600))  # what we display images on.
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize window

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (15, 15, 20)
CONST_SIZE = 18
CONST_GRID_OFFSET = [65, 25]


# load map from GameMap.txt
def load_text_file(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(row.split(' '))
    return game_map


def make_grid(text_map):
    y = 0
    map = []
    for row in text_map:
        temp = []
        x = 0
        for _ in row:
            temp.append(Square(x * CONST_SIZE + CONST_GRID_OFFSET[0], y * CONST_SIZE + CONST_GRID_OFFSET[1]))
            x += 1
        map.append(temp)
        y += 1
    return map


def draw_grid(grid_squares):
    for row in grid_squares:
        for square in row:
            if square.touch_cursor:
                pygame.draw.rect(display, WHITE, square.rect)
            else:
                pygame.draw.rect(display, BLACK, square.rect)
            pygame.draw.rect(display, GREY, square.rect, 1)


def cursor_on_square(grid_squares, cursor_loc):
    for row in grid_squares:
        for square in row:
            if pygame.Rect.collidepoint(square.rect, cursor_loc):
                square.touch_cursor = True
            else:
                square.touch_cursor = False


class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 12
        self.alive = False
        self.rect = pygame.Rect(x, y, CONST_SIZE, CONST_SIZE)
        self.touch_cursor = False


text_output = load_text_file("GameMap")
grid = make_grid(text_output)

while True:  # Main game loop

    display.fill(BLACK)  # makes screen black

    mx, my = pygame.mouse.get_pos()  # gets cursor co-ords
    loc = [mx, my]

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # checks if window is closed
            pygame.quit()  # stops pygame
            sys.exit()  # stops script

    # start here
    cursor_on_square(grid, loc)
    draw_grid(grid)
    # end here

    pygame.display.update()  # update display
    mainDisplay = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(mainDisplay, (0, 0))

    clock.tick(60)  # set frame rate

import pygame
import sys
from pygame.locals import *

# import random

# GAME RULES
# 1)Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# 2)Any live cell with two or three live neighbours lives on to the next generation.
# 3)Any live cell with more than three live neighbours dies, as if by overpopulation.
# 4)Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

clock = pygame.time.Clock()  # initialize clock
pygame.init()  # initialize pygame

WINDOW_SIZE = (770, 600)  # window size
display = pygame.Surface((770, 600))  # what we display images on.
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize window

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (30, 30, 40)
CONST_SIZE = 18
CONST_GRID_OFFSET = [65, 25]

# GAME VAR
UNDER_THRESH = 2
OVER_THRESH = 3
REPR_THRESH = 3


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
        self.loc = [int((x - CONST_GRID_OFFSET[0]) / CONST_SIZE), int((y - CONST_GRID_OFFSET[1]) / CONST_SIZE)]
        self.alive = False
        self.rect = pygame.Rect(x, y, CONST_SIZE, CONST_SIZE)
        self.touch_cursor = False
        self.neighbors = 0

    def tot_neighbors(self, grid_squares):
        tot = 0
        for x in (-1, -1, 0, 1, 1, 1, 0, -1):
            for y in (0, 1, 1, 1, 0, -1, -1, -1):
                if grid_squares[self.loc[1] + y][self.loc[0] + x].alive:
                    tot += 1
        self.neighbors = tot

    def die_method(self):
        if self.neighbors < UNDER_THRESH:
            self.alive = False
        elif self.neighbors > OVER_THRESH:
            self.alive = False

    def alive_method(self):
        if self.neighbors == REPR_THRESH:
            self.alive = True


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

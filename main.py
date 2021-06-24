import pygame
import sys
from pygame.locals import *

# GAME RULES
# 1)Any live cell with fewer than two live neighbours dies, as if by underpopulation. UNDER_THRESH = 2
# 2)Any live cell with two or three live neighbours lives on to the next generation.
# 3)Any live cell with more than three live neighbours dies, as if by overpopulation. OVER_THRESH = 3
# 4)Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction. REPR_THRESH = 3

# GAME VARIABLES
UNDER_THRESH = 2
OVER_THRESH = 3
REPR_THRESH = 3

CONST_SIZE = 10  # square size
CONST_GRID_OFFSET = [30, 25]  # move entire grid by
CONST_EDGE_IGNORE = 1  # make outer squares on grid unusable, to enclose chain reaction

# RGB color codes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (30, 30, 40)
BLUE = (160, 240, 255)
GREEN = (127, 255, 212)

clock = pygame.time.Clock()  # initialize clock
pygame.init()  # initialize pygame

WINDOW_SIZE = (770, 600)  # window size
display = pygame.Surface((770, 600))  # what we display images on.
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize window


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
    len_y = len(text_map)
    len_x = len(text_map[0])
    edge = False
    map = []
    alive = False

    for y in range(len_y):
        temp = []
        x = 0
        for _ in range(len_x):
            if y < CONST_EDGE_IGNORE or y > len_y - CONST_EDGE_IGNORE - 1:
                edge = True
            if x < CONST_EDGE_IGNORE or x > len_x - CONST_EDGE_IGNORE - 1:
                edge = True
            if text_map[y][x] == '1':
                alive = True
            temp.append(
                Square(x * CONST_SIZE + CONST_GRID_OFFSET[0], y * CONST_SIZE + CONST_GRID_OFFSET[1], edge, alive))
            x += 1
            edge = False
            alive = False
        map.append(temp)
        y += 1
    return map


def draw_grid(grid_squares):
    for row in grid_squares:
        for square in row:
            if square.alive:
                pygame.draw.rect(display, WHITE, square.rect)
            else:
                pygame.draw.rect(display, BLACK, square.rect)
            if square.touch_cursor:
                pygame.draw.rect(display, WHITE, square.rect)
            pygame.draw.rect(display, GREY, square.rect, 1)


def cursor_on_square(grid_squares, cursor_loc, click):
    for row in grid_squares:
        for square in row:
            if pygame.Rect.collidepoint(square.rect, cursor_loc):
                square.touch_cursor = True
                if click:
                    square.alive = True
            else:
                square.touch_cursor = False


class Square:
    def __init__(self, x, y, edge_square, alive):
        self.x = x
        self.y = y
        self.width = 12
        self.loc = [int((x - CONST_GRID_OFFSET[0]) / CONST_SIZE), int((y - CONST_GRID_OFFSET[1]) / CONST_SIZE)]
        self.alive = alive
        self.rect = pygame.Rect(x, y, CONST_SIZE, CONST_SIZE)
        self.touch_cursor = False
        self.neighbors = 0
        self.grid_edge = edge_square

    def tot_neighbors(self, grid_squares):
        tot = 0
        for y, x in ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)):
            if not grid_squares[self.loc[1]][self.loc[0]].grid_edge:
                if grid_squares[self.loc[1] + y][self.loc[0] + x].alive:
                    tot += 1
        self.neighbors = tot

    def die_alive_method(self):
        if not self.grid_edge:
            if self.neighbors == REPR_THRESH:
                self.alive = True
            if self.neighbors < UNDER_THRESH:
                self.alive = False
            elif self.neighbors > OVER_THRESH:
                self.alive = False


text_output = load_text_file("GameMap")
grid = make_grid(text_output)
click_state = False

while True:  # Main game loop

    display.fill(BLACK)  # makes screen black

    mx, my = pygame.mouse.get_pos()  # gets cursor co-ords
    loc = [mx, my]

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # checks if window is closed
            pygame.quit()  # stops pygame
            sys.exit()  # stops script
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                click_state = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:  # left click
                click_state = False

    for row_of_squares in grid:
        for single_square in row_of_squares:
            single_square.tot_neighbors(grid)
    for row_of_squares in grid:
        for single_square in row_of_squares:
            single_square.die_alive_method()

    cursor_on_square(grid, loc, click_state)
    draw_grid(grid)
    # end here

    pygame.display.update()  # update display
    mainDisplay = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(mainDisplay, (0, 0))

    clock.tick(20)  # set frame rate

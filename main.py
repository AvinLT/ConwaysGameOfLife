import sys
from pygame.locals import *
from ImportImages import *
import random

# GAME RULES
# 1)Any live cell with fewer than two live neighbours dies, as if by underpopulation. UNDER_THRESH = 2
# 2)Any live cell with two or three live neighbours lives on to the next generation.
# 3)Any live cell with more than three live neighbours dies, as if by overpopulation. OVER_THRESH = 3
# 4)Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction. REPR_THRESH = 3

# GAME VARIABLES
UNDER_THRESH = 2
OVER_THRESH = 3
REPR_THRESH = 3

CONST_SIZE = 12  # square size
CONST_GRID_OFFSET = [0, 0]  # move entire grid by
CONST_EDGE_IGNORE = 1  # make outer squares on grid unusable, to enclose chain reaction

# RGB color codes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (30, 30, 40)
LIGHT_GREY = (206, 206, 206)
BLUE = (160, 240, 255)
GREEN = (127, 255, 212)

clock = pygame.time.Clock()  # initialize clock
pygame.init()  # initialize pygame

WINDOW_SIZE = (770, 600)  # window size
display = pygame.Surface((770, 600))  # what we display images on
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize window

CONTINUE = False

# rectangles for all the buttons
play_pause_rect = pygame.Rect(int(WINDOW_SIZE[0] / 2 - 35 / 2), 550, 32, 32)
zoom_in_rect = pygame.Rect(int(WINDOW_SIZE[0] / 2 - 35 / 2 + 45), 550, 32, 32)
zoom_out_rect = pygame.Rect(int(WINDOW_SIZE[0] / 2 - 35 / 2 + 90), 550, 32, 32)

right_rect = pygame.Rect(int(WINDOW_SIZE[0] / 2 - 35 / 2 - 45), 550, 32, 32)
left_rect = pygame.Rect(int(WINDOW_SIZE[0] / 2 - 35 / 2 - 90), 550, 32, 32)
up_rect = pygame.Rect(int(WINDOW_SIZE[0] / 2 - 35 / 2 - 135), 550, 32, 32)
down_rect = pygame.Rect(int(WINDOW_SIZE[0] / 2 - 35 / 2 - 180), 550, 32, 32)

clear_rect = pygame.Rect(int(WINDOW_SIZE[0] / 2 - 35 / 2 - 300), 550, 32, 32)
shuffle_rect = pygame.Rect(int(WINDOW_SIZE[0] / 2 - 35 / 2 - 345), 550, 32, 32)

# black bar at bottom, used for button organising buttons
buttons_area_rect = pygame.Rect(0, WINDOW_SIZE[1] - 57, WINDOW_SIZE[0], 62)


# load map from GameMap.txt
# splits the grid of 1's and 0's into into 2D list
def load_text_file(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(row.split(' '))
    return game_map


# makes a grid of Squares. If 1 occurs, make the Square alive, else it is not alive
# marks outer Squares, so that a Square won't 'scan' neighbors outside of grid
def make_grid(text_map):
    len_y = len(text_map)
    len_x = len(text_map[0])
    edge = False
    alive = False
    map = []

    global CONST_SIZE
    CONST_SIZE = int(WINDOW_SIZE[0] / len_x)

    off_x = int((WINDOW_SIZE[0] - len_x * CONST_SIZE) / 2)
    off_y = int((WINDOW_SIZE[1] - len_y * CONST_SIZE) / 2)

    global CONST_GRID_OFFSET  # how much to displace the grid
    CONST_GRID_OFFSET = [off_x, off_y]

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


# does not use text file
# the grid rows and cols can be changed easier
# all square will start off dead
def make_custom_grid(len_x, len_y):
    edge = False
    map = []

    global CONST_SIZE
    CONST_SIZE = int(WINDOW_SIZE[0] / len_x)

    off_x = int((WINDOW_SIZE[0] - len_x * CONST_SIZE) / 2)
    off_y = int((WINDOW_SIZE[1] - len_y * CONST_SIZE) / 2)

    global CONST_GRID_OFFSET  # how much to displace the grid
    CONST_GRID_OFFSET = [off_x, off_y]

    for y in range(len_y):
        temp = []
        x = 0
        for _ in range(len_x):
            if y < CONST_EDGE_IGNORE or y > len_y - CONST_EDGE_IGNORE - 1:
                edge = True
            if x < CONST_EDGE_IGNORE or x > len_x - CONST_EDGE_IGNORE - 1:
                edge = True
            temp.append(
                Square(x * CONST_SIZE + CONST_GRID_OFFSET[0], y * CONST_SIZE + CONST_GRID_OFFSET[1], edge, False))
            x += 1
            edge = False
        map.append(temp)
        y += 1
    return map


# draws grid of squares
# if cursor is on a square, light up the square, but it is not 'alive'
def draw_grid(grid_squares):
    for row in grid_squares:
        for square in row:
            if square.alive:
                pygame.draw.rect(display, WHITE, square.rect)
            else:
                pygame.draw.rect(display, BLACK, square.rect)
            if square.touch_cursor:
                pygame.draw.rect(display, WHITE, square.rect)
            pygame.draw.rect(display, GREY, square.rect, 1)  # black border around each square


# marks thr square which the cursor is on
# make square 'alive' if click is True
def cursor_on_square(grid_squares, cursor_loc, click, buttons_rect):
    for row in grid_squares:
        for square in row:
            if pygame.Rect.collidepoint(square.rect, cursor_loc) \
                    and not pygame.Rect.collidepoint(buttons_rect, cursor_loc):
                square.touch_cursor = True
                if click:
                    square.alive = not square.alive
            else:
                square.touch_cursor = False


# if pause/play button clicked, the game stops executing the die_alive_method.
def pause_button_click(button_rect, cursor_loc, click):
    if pygame.Rect.collidepoint(button_rect, cursor_loc) and click:
        global CONTINUE
        CONTINUE = not CONTINUE


# zoom in = 1
# zoom out = -1
# nothing, zoom = 0
# changes the size of squares for zoom effect
# center square is the focal point of zoom in/out
def zoom_pause_button_click(grid_squares, in_button_rect, out_button_rect, cursor_loc, click):
    if pygame.Rect.collidepoint(in_button_rect, cursor_loc) and click:
        zoom = 1
    elif pygame.Rect.collidepoint(out_button_rect, cursor_loc) and click:
        zoom = -1
    else:
        zoom = 0

    len_y = len(grid_squares)
    len_x = len(grid_squares[0])
    center = [int(len_y / 2), int(len_x / 2)]
    min_size = int(WINDOW_SIZE[0] / len_x)
    max_size = 100

    # when zooming out
    if zoom == 1 and max_size > grid_squares[0][0].rect.width:
        for y in range(len_y):
            for x in range(len_x):
                # squares that are further out from center square move more than squares closer to center
                grid_squares[y][x].rect.y += -(center[0] - y + 1) * zoom
                grid_squares[y][x].rect.x += -(center[1] - x + 1) * zoom
                grid_squares[y][x].rect.width += 1 * zoom
                grid_squares[y][x].rect.height += 1 * zoom

    in_screen = False
    bigger_rect = 24
    screen_rect = pygame.Rect(-bigger_rect, -bigger_rect, WINDOW_SIZE[0] + bigger_rect, WINDOW_SIZE[1] + bigger_rect)
    # uses big rectangle, size of the window, used too see if being zoomed out of screen

    if grid_squares[0][len_x - 1].rect.right > screen_rect.right and grid_squares[0][0].rect.left < screen_rect.left \
            and grid_squares[len_y - 1][0].rect.bottom > screen_rect.bottom and grid_squares[0][
            0].rect.top < screen_rect.top:
        in_screen = True
    # when zooming out
    if zoom == -1 and grid_squares[0][0].rect.width > min_size and in_screen:
        for y in range(len_y):
            for x in range(len_x):
                # squares that are further out from center square move more than squares closer to center
                grid_squares[y][x].rect.y += -(center[0] - y + 1) * zoom
                grid_squares[y][x].rect.x += -(center[1] - x + 1) * zoom
                grid_squares[y][x].rect.width += 1 * zoom
                grid_squares[y][x].rect.height += 1 * zoom

    return grid_squares


def move(grid_squares, right_button_rect, left_button_rect, up_button_rect, down_button_rect, cursor_loc, click):
    screen_rect = pygame.Rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])
    speed = 4

    if click:
        if pygame.Rect.collidepoint(right_button_rect, cursor_loc):
            direction = [-speed, 0]
        elif pygame.Rect.collidepoint(left_button_rect, cursor_loc):
            direction = [speed, 0]
        elif pygame.Rect.collidepoint(up_button_rect, cursor_loc):
            direction = [0, speed]
        elif pygame.Rect.collidepoint(down_button_rect, cursor_loc):
            direction = [0, -speed]
        else:
            direction = [0, 0]

        len_x = len(grid_squares[0])
        len_y = len(grid_squares)

        if direction[0] != 0:
            if direction[0] < 0:
                if grid_squares[0][len_x - 1].rect.right > screen_rect.right:
                    for row in grid_squares:
                        for square in row:
                            square.rect.x += direction[0]
            else:
                if grid_squares[0][0].rect.left < screen_rect.left:
                    for row in grid_squares:
                        for square in row:
                            square.rect.x += direction[0]
        else:
            if direction[1] < 0:
                if grid_squares[len_y - 1][0].rect.bottom > screen_rect.bottom:
                    for row in grid_squares:
                        for square in row:
                            square.rect.y += direction[1]
            else:
                if grid_squares[0][0].rect.top < screen_rect.top:
                    for row in grid_squares:
                        for square in row:
                            square.rect.y += direction[1]

    return grid_squares


# clears all squares
def clear(grid_squares, button_rect, cursor_loc, click):
    if pygame.Rect.collidepoint(button_rect, cursor_loc) and click:
        for row in grid_squares:
            for square in row:
                square.alive = False
    return grid_squares


# makes all squares either alive of dead, using the random module
def shuffle(grid_squares, button_rect, cursor_loc, click):
    len_y = len(grid_squares)
    len_x = len(grid_squares[0])

    if pygame.Rect.collidepoint(button_rect, cursor_loc) and click:
        for y in range(len_y):
            for x in range(len_x):
                edge = False
                if y < CONST_EDGE_IGNORE or y > len_y - CONST_EDGE_IGNORE - 1:
                    edge = True
                if x < CONST_EDGE_IGNORE or x > len_x - CONST_EDGE_IGNORE - 1:
                    edge = True
                if not edge:
                    if random.randint(0, 9) < 5:
                        grid_squares[y][x].alive = True
                    else:
                        grid_squares[y][x].alive = False
    return grid_squares


# x,y are the pixel cords on the window
# loc is the cord on the grid
# neighbors is the number of 'alive' squares around the self square
# grid_edge indicates whether the square is on the edge of grid
class Square:
    def __init__(self, x, y, edge_square, alive):
        self.x = x
        self.y = y
        self.loc = [int((x - CONST_GRID_OFFSET[0]) / CONST_SIZE), int((y - CONST_GRID_OFFSET[1]) / CONST_SIZE)]
        self.alive = alive
        self.rect = pygame.Rect(x, y, CONST_SIZE, CONST_SIZE)
        self.touch_cursor = False
        self.neighbors = 0
        self.grid_edge = edge_square
        self.color = []

    # counts the number of 'alive' squares around self square
    def tot_neighbors(self, grid_squares):
        tot = 0
        for y, x in ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)):
            if not grid_squares[self.loc[1]][self.loc[0]].grid_edge:
                if grid_squares[self.loc[1] + y][self.loc[0] + x].alive:
                    tot += 1
        self.neighbors = tot

    # implements the rules of the game. Can be changed by changing THRESHOLDS
    def die_alive_method(self):
        if not self.grid_edge:
            if self.neighbors == REPR_THRESH:
                self.alive = True
            if self.neighbors < UNDER_THRESH:
                self.alive = False
            elif self.neighbors > OVER_THRESH:
                self.alive = False


text_output = load_text_file("GameMap")
# off_set_grid(text_output)
# grid = make_grid(text_output)
grid = make_custom_grid(75, 75)

click_state = False

test = pygame.time.Clock()

while True:  # Main game loop

    test.tick()
    print(test)

    display.fill(BLACK)  # makes screen black

    mx, my = pygame.mouse.get_pos()  # gets cursor co-ords
    loc = [mx, my]
    single_click = False

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # checks if window is closed
            pygame.quit()  # stops pygame
            sys.exit()  # stops script
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                click_state = True
                single_click = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:  # left click
                click_state = False

    # updates the # of neighbors around square
    for row_of_squares in grid:
        for single_square in row_of_squares:
            single_square.tot_neighbors(grid)

    # 'kills' or 'spawn' squares depending of the number of neighbors
    if CONTINUE:
        for row_of_squares in grid:
            for single_square in row_of_squares:
                single_square.die_alive_method()

    pause_button_click(play_pause_rect, loc, single_click)
    grid = zoom_pause_button_click(grid, zoom_in_rect, zoom_out_rect, loc, click_state)
    grid = move(grid, right_rect, left_rect, up_rect, down_rect, loc, click_state)
    grid = clear(grid, clear_rect, loc, single_click)
    grid = shuffle(grid, shuffle_rect, loc, single_click)

    cursor_on_square(grid, loc, single_click, buttons_area_rect)
    draw_grid(grid)

    pygame.draw.rect(display, BLACK, buttons_area_rect)

    display.blit(plus_button, [zoom_in_rect.x, zoom_in_rect.y])
    display.blit(minus_button, [zoom_out_rect.x, zoom_out_rect.y])

    display.blit(right_button, [right_rect.x, right_rect.y])
    display.blit(left_button, [left_rect.x, left_rect.y])
    display.blit(up_button, [up_rect.x, up_rect.y])
    display.blit(down_button, [down_rect.x, down_rect.y])

    display.blit(clear_button, [clear_rect.x, clear_rect.y])
    display.blit(shuffle_button, [shuffle_rect.x, shuffle_rect.y])

    if CONTINUE:
        display.blit(pause_button, [int(WINDOW_SIZE[0] / 2 - 35 / 2), 550])
    else:
        display.blit(play_button, [int(WINDOW_SIZE[0] / 2 - 35 / 2), 550])
    # end here

    pygame.display.update()  # update display
    mainDisplay = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(mainDisplay, (0, 0))

    clock.tick(60)  # set frame rate

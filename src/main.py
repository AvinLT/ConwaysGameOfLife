import sys
from draw import *
import random
import json

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
CONTINUE = False  # False means that game is paused
PRESET_DROPDOWN = False
SETTING_DROPDOWN = False
SCROLL = 0

# RGB color codes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (30, 30, 40)
LIGHT_GREY = (206, 206, 206)
BLUE = (160, 240, 255)
GREEN = (127, 255, 212)

clock = pygame.time.Clock()  # initialize clock
pygame.init()  # initialize pygame

font_style = pygame.font.SysFont('cambria', 15)
font_style_med = pygame.font.SysFont('cambria', 18)
font_style_big = pygame.font.SysFont('cambria', 25)


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
# makes a grid of Squares. If 1 occurs, make the Square alive, else it is not alive
# marks outer Squares, so that a Square won't 'scan' neighbors outside of grid
def make_custom_grid(len_x, len_y):
    edge = False
    map = []

    global CONST_SIZE
    CONST_SIZE = int(WINDOW_SIZE[0] / (len_x / 1.3))

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
                # makes the square that has been alive for longer, more blue. the max square.time is 200
                # so darkest color a square can be is (55, 55, 255)
                pygame.draw.rect(display, (255 - square.time, 255 - square.time, 255), square.rect)
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
def zoom_button_click(grid_squares, in_button_rect, out_button_rect, cursor_loc, click):
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
            and grid_squares[len_y - 1][0].rect.bottom > screen_rect.bottom and grid_squares[0][0].rect.top < \
            screen_rect.top:
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


def move_button_click(grid_squares, right_button_rect, left_button_rect, up_button_rect, down_button_rect, cursor_loc,
                      click):
    screen_rect = pygame.Rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])
    speed = 3

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


def import_pattern(json_path):
    with open(json_path, 'r') as fh:
        s = fh.read()
        json_patterns = json.loads(s)
    return json_patterns


# clears all squares
# makes all squares either alive of dead, using the random module
def other_buttons(grid_squares, cursor_loc, click, rect_shuffle, rect_clear, rect_preset, rect_settings):
    len_y = len(grid_squares)
    len_x = len(grid_squares[0])

    if pygame.Rect.collidepoint(rect_shuffle, cursor_loc) and click:
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

    if pygame.Rect.collidepoint(rect_clear, cursor_loc) and click:
        for row in grid_squares:
            for square in row:
                square.alive = False

    global PRESET_DROPDOWN
    global SETTING_DROPDOWN

    if pygame.Rect.collidepoint(rect_preset, cursor_loc) and click:
        PRESET_DROPDOWN = not PRESET_DROPDOWN
        SETTING_DROPDOWN = False

    if pygame.Rect.collidepoint(rect_settings, cursor_loc) and click:
        SETTING_DROPDOWN = not SETTING_DROPDOWN
        PRESET_DROPDOWN = False

    return grid_squares


def draw_dropdown(preset_dropdown, setting_dropdown, cursor_loc, click, preset, grid_squares):
    preset_loc = [570, 50]
    setting_loc = [570, 410]

    global UNDER_THRESH
    global OVER_THRESH
    global REPR_THRESH

    if preset_dropdown:
        pygame.draw.rect(display, BLACK, (preset_loc[0], preset_loc[1], 155, 540))
        for i in range(0, 18):
            pygame.draw.rect(display, WHITE, (preset_loc[0], preset_loc[1] + 30 * i, 155, 30), 2)
            text = preset[i + SCROLL]["title"]
            label = font_style.render(text, True, WHITE)
            display.blit(label, (preset_loc[0] + 5, preset_loc[1] + 5 + 30 * i))

            if pygame.Rect.collidepoint(pygame.Rect(preset_loc[0], preset_loc[1] + 30 * i, 155, 30), cursor_loc) \
                    and click:
                pattern = preset[i + SCROLL]["life"]
                len_x = len(grid_squares[0])
                len_y = len(grid_squares)
                if len(pattern) > len_y or len(pattern[0]) > len_x:
                    print("preset pattern is too big")
                else:
                    for row in grid_squares:
                        for square in row:
                            square.alive = False
                    pattern_loc = [int((len_x - len(pattern[0])) / 2), int((len_y - len(pattern)) / 2)]

                    for y in range(len(pattern)):
                        for x in range(len(pattern[0])):
                            if pattern[y][x] == 1:
                                grid_squares[pattern_loc[1] + y][pattern_loc[0] + x].alive = True
    elif setting_dropdown:
        pygame.draw.rect(display, BLACK, (setting_loc[0], setting_loc[1], 155, 150))
        for i in range(3):
            pygame.draw.rect(display, WHITE, (setting_loc[0], setting_loc[1] + 60 * i, 155, 60), 2)

            pygame.draw.rect(display, WHITE, (setting_loc[0] + 110, setting_loc[1] + 60 * i, 45, 60), 2)

            pygame.draw.rect(display, WHITE, (setting_loc[0] + 110, setting_loc[1] + 60 * i, 45, 15), 2)
            pygame.draw.rect(display, WHITE, (setting_loc[0] + 110, setting_loc[1] + 45 + 60 * i, 45, 15), 2)

            pygame.draw.polygon(screen, WHITE, [[703, 416 + 60 * i], [701, 419 + 60 * i], [705, 419 + 60 * i]])
            pygame.draw.polygon(screen, WHITE, [[703, 464 + 60 * i], [701, 461 + 60 * i], [705, 461 + 60 * i]])

            under_num = font_style_big.render(str(UNDER_THRESH), True, WHITE)
            under_text1 = font_style_med.render("Under", True, WHITE)
            under_text2 = font_style_med.render("Limit", True, WHITE)
            over_num = font_style_big.render(str(OVER_THRESH), True, WHITE)
            over_text1 = font_style_med.render("Over", True, WHITE)
            over_text2 = font_style_med.render("Limit", True, WHITE)
            repr_num = font_style_big.render(str(REPR_THRESH), True, WHITE)
            repr_text1 = font_style_med.render("Spawn", True, WHITE)
            repr_text2 = font_style_med.render("Rate", True, WHITE)

            display.blit(under_num, (697, 425))
            display.blit(over_num, (697, 485))
            display.blit(repr_num, (697, 545))

            display.blit(under_text1, (setting_loc[0] + 30, 418))
            display.blit(under_text2, (setting_loc[0] + 33, 440))

            display.blit(over_text1, (setting_loc[0] + 33, 478))
            display.blit(over_text2, (setting_loc[0] + 33, 500))

            display.blit(repr_text1, (setting_loc[0] + 27, 538))
            display.blit(repr_text2, (setting_loc[0] + 36, 560))

            if pygame.Rect.collidepoint(pygame.Rect((setting_loc[0] + 110, setting_loc[1] + 60 * i, 45, 15)),
                                        cursor_loc) and click:
                if i == 0:
                    UNDER_THRESH += 1
                    if UNDER_THRESH > 8:
                        UNDER_THRESH = 8
                    if UNDER_THRESH > OVER_THRESH:
                        UNDER_THRESH -= 1
                elif i == 1:
                    OVER_THRESH += 1
                    if OVER_THRESH > 8:
                        OVER_THRESH = 8
                elif i == 2:
                    REPR_THRESH += 1
                    if REPR_THRESH > OVER_THRESH:
                        REPR_THRESH -= 1
            elif pygame.Rect.collidepoint(pygame.Rect((setting_loc[0] + 110, setting_loc[1] + 45 + 60 * i, 45, 15)),
                                          cursor_loc) and click:
                if i == 0:
                    UNDER_THRESH -= 1
                    if UNDER_THRESH < 1:
                        UNDER_THRESH = 1
                elif i == 1:
                    OVER_THRESH -= 1
                    if OVER_THRESH < 1:
                        OVER_THRESH = 1
                    if OVER_THRESH < UNDER_THRESH:
                        OVER_THRESH += 1
                elif i == 2:
                    REPR_THRESH -= 1
                    if REPR_THRESH < UNDER_THRESH:
                        REPR_THRESH += 1

            if REPR_THRESH > OVER_THRESH:
                REPR_THRESH = OVER_THRESH
            if REPR_THRESH < UNDER_THRESH:
                REPR_THRESH = UNDER_THRESH

    return grid


# each square on grid is made of Square class
class Square:
    def __init__(self, x, y, edge_square, alive):
        self.x = x  # x the pixel cords on the window
        self.y = y  # y the pixel cords on the window
        self.loc = [int((x - CONST_GRID_OFFSET[0]) / CONST_SIZE), int((y - CONST_GRID_OFFSET[1]) / CONST_SIZE)]
        self.alive = alive  # is the number of 'alive' squares around the self square
        self.rect = pygame.Rect(x, y, CONST_SIZE, CONST_SIZE)
        self.touch_cursor = False
        self.neighbors = 0
        self.grid_edge = edge_square  # indicates whether the square is on the edge of grid
        self.time = 0  # is the number of frames the square has been alive without dying. Used for color and max is 200
        self.prev_alive = False  # tells you if square was alive previous frame

    # counts the number of 'alive' squares around self square
    def tot_neighbors(self, grid_squares):
        tot = 0
        for y, x in ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)):
            if not grid_squares[self.loc[1]][self.loc[0]].grid_edge:
                if grid_squares[self.loc[1] + y][self.loc[0] + x].alive:
                    tot += 1
        self.neighbors = tot

    # checks if square is on the edge of grid, applies rules of game, increments self.time up to a maximum
    def die_alive_method(self):
        if not self.grid_edge:
            if self.alive:
                self.prev_alive = True
            else:
                self.prev_alive = False

            # implements the rules of the game. Can be changed by changing THRESHOLDS
            if self.neighbors == REPR_THRESH:
                self.alive = True
            if self.neighbors < UNDER_THRESH:
                self.alive = False
            elif self.neighbors > OVER_THRESH:
                self.alive = False

            # self.time used for color of square, so limit is 200 to not make square too dark blue
            if self.prev_alive and self.alive:
                if self.time < 200:
                    self.time += 2
            else:
                self.time = 0


patterns = import_pattern("../json/all_patterns.json")
text_output = load_text_file("../res/GameMap")
# grid = make_grid(text_output)
grid = make_custom_grid(100, 100)

click_state = False

while True:  # Main game loop

    display.fill(BLACK)  # makes screen black

    mx, my = pygame.mouse.get_pos()  # gets cursor co-ords
    loc = [mx, my]
    single_click = False

    for event in pygame.event.get():  # event loop
        if event.type == pygame.QUIT:  # checks if window is closed
            pygame.quit()  # stops pygame
            sys.exit()  # stops script
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                click_state = True
                single_click = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # left click
                click_state = False
        if event.type == pygame.MOUSEWHEEL:
            SCROLL += - event.y
            if SCROLL < 0:
                SCROLL = 0
            elif SCROLL > len(patterns) - 18:
                SCROLL = len(patterns) - 18

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
    zoom_button_click(grid, zoom_in_rect, zoom_out_rect, loc, click_state)
    move_button_click(grid, right_rect, left_rect, up_rect, down_rect, loc, click_state)
    other_buttons(grid, loc, single_click, shuffle_rect, clear_rect, preset_rect, settings_rect)

    cursor_on_square(grid, loc, single_click, buttons_area_rect)
    draw_grid(grid)
    draw_tools(CONTINUE, font_style)
    draw_dropdown(PRESET_DROPDOWN, SETTING_DROPDOWN, loc, single_click, patterns, grid)

    # end here

    pygame.display.update()  # update display
    mainDisplay = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(mainDisplay, (0, 0))

    clock.tick(30)  # set frame rate
from ImportImages import *

WINDOW_SIZE = (770, 600)  # window size
display = pygame.Surface((770, 600))  # what we display images on
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize window

# black bar at bottom, used for button organising buttons
buttons_area_rect = pygame.Rect(0, WINDOW_SIZE[1] - 50, WINDOW_SIZE[0] - 2, 51)

# rectangles for all the buttons
play_pause_rect = pygame.Rect(367, 559, 32, 32)
zoom_in_rect = pygame.Rect(367 + 40, 559, 32, 32)
zoom_out_rect = pygame.Rect(367 + 80, 559, 32, 32)
right_rect = pygame.Rect(367 - 40, 559, 32, 32)
left_rect = pygame.Rect(367 - 80, 559, 32, 32)
up_rect = pygame.Rect(367 - 120, 559, 32, 32)
down_rect = pygame.Rect(367 - 160, 559, 32, 32)

clear_rect = pygame.Rect(367 - 200, 559, 32, 32)
shuffle_rect = pygame.Rect(367 - 240, 559, 32, 32)

preset_rect = pygame.Rect(367 + 165, 559, 32, 32)
settings_rect = pygame.Rect(730, 559, 32, 32)


def draw_tools(paused, font_style):
    pygame.draw.rect(display, (0, 0, 0), buttons_area_rect)
    # pygame.draw.rect(display, (255, 255, 255), buttons_area_rect, 1)

    display.blit(plus_button, [zoom_in_rect.x, zoom_in_rect.y])
    display.blit(minus_button, [zoom_out_rect.x, zoom_out_rect.y])
    display.blit(settings_button, [settings_rect.x, settings_rect.y])
    display.blit(right_button, [right_rect.x, right_rect.y])
    display.blit(left_button, [left_rect.x, left_rect.y])
    display.blit(up_button, [up_rect.x, up_rect.y])
    display.blit(down_button, [down_rect.x, down_rect.y])
    display.blit(clear_button, [clear_rect.x, clear_rect.y])
    display.blit(shuffle_button, [shuffle_rect.x, shuffle_rect.y])
    display.blit(preset_button, [preset_rect.x, preset_rect.y])

    if paused:
        display.blit(pause_button, [int(WINDOW_SIZE[0] / 2 - 35 / 2), 559])
    else:
        display.blit(play_button, [int(WINDOW_SIZE[0] / 2 - 35 / 2), 559])

    game_name1 = font_style.render("Game", True, (255, 255, 255))
    game_name2 = font_style.render("of Life", True, (255, 255, 255))
    display.blit(game_name1, (27, WINDOW_SIZE[1] - 45))
    display.blit(game_name2, (25, WINDOW_SIZE[1] - 30))
    pygame.draw.rect(display, (160, 240, 255), (22, WINDOW_SIZE[1] - 45, 50, 38), 2, 3)

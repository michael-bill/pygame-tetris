import pygame
from time import time
from field import Field
from config import screen_size, block_size_in_pixels, border_color, \
    brick_falling_speed, field_size_x, field_size_y, \
    background_color, block_border_color
import pygame as pg

pg.init()

screen = pg.display.set_mode(screen_size)
clock = pygame.time.Clock()
field = Field(field_size_x, field_size_y, background_color)
frame_time = time()

def draw_block(x, y, color):
    """Draws a block on the screen

    Args:
        x (int): Game coordinate x
        y (int): Game coordinate y
        color (pg.Color): The color of the block
    """    
    display_x = x * block_size_in_pixels
    display_y = y * block_size_in_pixels
    pg.draw.rect(screen, color, pg.Rect(
        display_x, display_y, block_size_in_pixels, block_size_in_pixels))
    pg.draw.rect(screen, block_border_color, pg.Rect(
        display_x, display_y, block_size_in_pixels, block_size_in_pixels), 1)


def draw_field():
    """Draws the playing field"""    
    for i in range(max(field.size_x + 1, field.size_y + 1)):
        if i <= field.size_x + 1:
            draw_block(i, 0, border_color)
            draw_block(i, field.size_y + 1, border_color)
        if 1 <= i <= field.size_y:
            draw_block(0, i, border_color)
            draw_block(field.size_x + 1, i, border_color)
    for i in range(field.size_x):
        for j in range(field.size_y):
            draw_block(i + 1, j + 1, field.matrix[j][i][1])


def move():
    """Moves the falling block (fall)"""   
    global field
    global frame_time
    field.move()
    if field.detect_game_over():
        field = Field(field_size_x, field_size_y, background_color)
    frame_time = time()


def key_down_listener(key):
    """The method that listens to keyboard strokes
    Key a - move a brick to the left
    Key d - move a brick to the right
    Key s - move a brick downward
    Key e - rotate the brick 90 degrees clockwise
    Key q - rotate the brick 90 degrees counterclockwise
    Key space - flip the brick downward

    Args:
        key (event.key): Key pressed
    """    
    global frame_time
    global field
    if key == pg.K_a:
        field.move_falling_brick(-1)
    elif key == pg.K_d:
        field.move_falling_brick(1)
    elif key == pg.K_s:
        move()
    elif key == pg.K_q:
        field.rotate_falling_brick(-1)
    elif key == pg.K_e:
        field.rotate_falling_brick(1)
    elif key == pg.K_SPACE:
        field.fall_the_brick()
        if field.detect_game_over():
            field = Field(field_size_x, field_size_y, background_color)
        frame_time = time()


def event_listener():
    """Application event listener method"""    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            key_down_listener(event.key)


while True:
    """Main game cycle"""
    event_listener()
    draw_field()
    if time() - frame_time >= brick_falling_speed:
        move()
    pg.display.flip()
    clock.tick(100)

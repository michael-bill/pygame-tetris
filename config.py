# The speed of the falling brick in seconds
brick_falling_speed = 0.5
# Field width in blocks
field_size_x = 10
# Field height in blocks
field_size_y = 20
# Border size
border_size = 1
# Block size in pixels
block_size_in_pixels = 40
# Field background color
background_color = (255, 255, 255)
# Color of border blocks
border_color = (155, 155, 155)
# Color of block borders
block_border_color = (0, 0, 0)
# [Screen Width, Screen Height]
screen_size = [
    (field_size_x + border_size * 2) * block_size_in_pixels,
    (field_size_y + border_size * 2) * block_size_in_pixels
]
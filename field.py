from random import randint
from brick import bricks


def rotate_90_matrix(matrix, direction):
    """Rotates the matrix by 90 degrees
    If direction == 1 then clockwise
    If direction == 0, then counterclockwise

    Args:
        matrix (list): Matrix
        direction (int): Direction

    Returns:
        list: New matrix
    """    
    if direction == 1:
        return [list(reversed(col)) for col in zip(*matrix)]
    elif direction == -1:
        return [list(row) for row in list(zip(*matrix))[::-1]]


class Field:
    """The playing field.
    The class is mostly a matrix, where each
    i, j element is a list: [1 (there is a block) or 0 (no block, empty), pg.Color (block color)].
    """    
    def __init__(self, size_x, size_y, color):
        """Playing Field

        Args:
            size_x (int): Width of the playing field
            size_y (int): Length of the playing field
            color (pg.Color): Color of the playing field
        """        
        self.size_x = size_x
        self.size_y = size_y
        self.matrix = [[[0, color] for _ in range(size_x)] for _ in range(size_y)]
        self.color = color
        self.falling_brick = None
        self.generate_new_falling_brick()

    def generate_new_falling_brick(self):
        """Generates a new random falling brick"""        
        brick = bricks[randint(0, len(bricks) - 1)].copy()
        self.set_falling_brick(brick, randint(0, self.size_x - brick.size_x), -brick.size_y)

    def set_falling_brick(self, brick, x, y):
        """Sets up a falling brick

        Args:
            brick (Brick): Brick
            x (int): x position
            y (int): Y position
        """        
        for i in range(y, y + brick.size_y):
            for j in range(x, x + brick.size_x):
                if 0 <= i < self.size_y and 0 <= j < self.size_x and brick.matrix[i - y][j - x] == 1:
                    self.matrix[i][j][0] = brick.matrix[i - y][j - x]
                    self.matrix[i][j][1] = brick.color
        brick.x = x
        brick.y = y
        self.falling_brick = brick

    def detect_illegal_move(self, direction):
        """Determines whether a move is possible or not
        Direction options:
        1 - right
        -1 - left
        0 - down
        Args:
            direction (int): Direction of motion

        Returns:
            bool: Possible move or not
        """
        brick = self.falling_brick
        if brick.x == 0 and direction == -1: return True
        if brick.x + brick.size_x == self.size_x and direction == 1: return True
        if brick.y + brick.size_y == self.size_y and direction == 0: return True
        for i in range(brick.y, brick.y + brick.size_y):
            for j in range(brick.x, brick.x + brick.size_x):
                brick_i = i - brick.y
                brick_j = j - brick.x
                block_not_empty = (brick.matrix[brick_i][brick_j] == 1)
                block_at_the_brick_left = \
                    (brick_j == 0 or brick.matrix[brick_i][brick_j - 1] == 0)
                block_at_the_brick_right = \
                    (brick.size_x == brick_j + 1 or brick.matrix[brick_i][brick_j + 1] == 0)
                block_move_left_to_another_block = (self.matrix[i][j - 1][0] == 1)
                block_move_right_to_another_block = (j + 1 < self.size_x and self.matrix[i][j + 1][0] == 1)
                if block_not_empty and \
                        ((direction == -1 and block_at_the_brick_left and block_move_left_to_another_block) or
                         (direction == 1 and block_at_the_brick_right and block_move_right_to_another_block)):
                    return True
        return False

    def move_falling_brick(self, direction):
        """Move brick
        If direction == 1 - to the right
        If direction == -1 - to the left
        If direction ==0 - down

        Args:
            direction (int): Direction of movement
        """        
        brick = self.falling_brick
        if self.detect_illegal_move(direction): return
        self.remove_brick_from_field()
        if direction != 0:
            brick.x += direction
        else:
            brick.y += 1
        self.set_falling_brick(brick, brick.x, brick.y)

    def fall_the_brick(self):
        """Fail a falling brick down"""        
        while not self.detect_fall():
            self.move_falling_brick(0)
        res, row_index = self.detect_filled_row()
        if res:
            self.remove_row(row_index)
        self.generate_new_falling_brick()
        self.detect_filled_row()

    def remove_brick_from_field(self):
        """Remove a falling brick from the field"""
        brick = self.falling_brick
        for i in range(brick.y, brick.y + brick.size_y):
            for j in range(brick.x, brick.x + brick.size_x):
                brick_i = i - brick.y
                brick_j = j - brick.x
                if 0 <= i < self.size_y and 0 <= j < self.size_x and brick.matrix[brick_i][brick_j] == 1:
                    self.matrix[i][j][0] = 0
                    self.matrix[i][j][1] = self.color

    def detect_fall(self):
        """Determine if there is a drop

        Returns:
            bool: Whether there is a drop or not
        """
        brick = self.falling_brick
        for i in range(brick.y, brick.y + brick.size_y):
            for j in range(brick.x, brick.x + brick.size_x):
                brick_i = i - brick.y
                brick_j = j - brick.x
                block_not_empty = (brick.matrix[brick_i][brick_j] == 1)
                block_at_the_brick_bottom = \
                    (brick.size_y == brick_i + 1 or brick.matrix[brick_i + 1][brick_j] == 0)
                block_on_floor = (i + 1 == self.size_y)
                block_on_another_block = (i + 1 < self.size_y and self.matrix[i + 1][j][0] == 1)
                if block_not_empty and block_at_the_brick_bottom and (block_on_floor or block_on_another_block):
                    return True
        return False

    def detect_filled_row(self):
        """Detect if there is a filled row to delete it

        Returns:
            bool: Whether there is a row or not
        """
        for i in range(self.size_y):
            remove = True
            for j in range(self.size_x):
                if self.matrix[i][j][0] != 1:
                    remove = False
            if remove:
                return True, i
        return False, -1

    def remove_row(self, row_index):
        """Delete a row by its index

        Args:
            row_index (int): Row index
        """
        new_row = [[0, self.color] for _ in range(self.size_x)]
        del self.matrix[row_index]
        self.matrix.insert(0, new_row)

    def rotate_falling_brick(self, direction):
        """Turn the falling brick 90 degrees clockwise or counterclockwise
        If direction == 1, clockwise.
        If direction == 0, counterclockwise.
        
        Args:
            direction (int): Direction
        """
        brick = self.falling_brick.copy()
        self.remove_brick_from_field()
        new_matrix = rotate_90_matrix(brick.matrix, direction)
        brick.matrix = new_matrix
        brick.size_x = len(new_matrix[0])
        brick.size_y = len(new_matrix)
        for i in range(brick.y, brick.y + brick.size_y):
            for j in range(brick.x, brick.x + brick.size_x):
                brick_i = i - brick.y
                brick_j = j - brick.x
                if (brick.matrix[brick_i][brick_j] == 1 and
                        (i >= self.size_y or j >= self.size_x or
                         (self.matrix[i][j][0] == 1))):
                    self.set_falling_brick(self.falling_brick, brick.x, brick.y)
                    return
        self.set_falling_brick(brick, brick.x, brick.y)

    def detect_game_over(self):
        """Determines if the game is over or not

        Returns:
            bool: Whether the game is over or not
        """
        brick = self.falling_brick
        self.remove_brick_from_field()
        for i in self.matrix[0]:
            if i[0] == 1 :
                return True
        self.set_falling_brick(self.falling_brick, brick.x, brick.y)
        return False

    def move(self):
        """Moves the falling block (fall)"""
        if self.detect_fall():
            self.generate_new_falling_brick()
            while True:
                res, row_index = self.detect_filled_row()
                if res: self.remove_row(row_index)
                else: break
        self.move_falling_brick(0)
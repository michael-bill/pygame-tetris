class Brick:
    """A class that defines a brick"""

    def __init__(self, matrix, color):
        """A class that defines a brick

        Args:
            matrix (list): A matrix of 0 and 1, where 0 is empty, 1 is the presence of a block
            color (pg.Color): The color of the brick
        """        
        self.matrix = matrix
        self.color = color
        self.x = 0
        self.y = 0
        self.size_x = len(matrix[0])
        self.size_y = len(matrix)

    def copy(self):
        """Copies a brick

        Returns:
            Brick: new instance of the Brick class
        """        
        brick = Brick(self.matrix, self.color)
        brick.x = self.x
        brick.y = self.y
        return brick


# All default kinds of bricks in tetris
brick1 = Brick([
    [1],
    [1],
    [1],
    [1]
], (0, 255, 255))

brick2 = Brick([
    [0, 1],
    [0, 1],
    [1, 1]
], (0, 0, 255))

brick3 = Brick([
    [1, 0],
    [1, 0],
    [1, 1]
], (255, 125, 0))

brick4 = Brick([
    [1, 1],
    [1, 1]
], (255, 255, 0))

brick5 = Brick([
    [0, 1, 1],
    [1, 1, 0]
], (0, 255, 0))

brick6 = Brick([
    [1, 1, 1],
    [0, 1, 0]
], (255, 0, 255))

brick7 = Brick([
    [1, 1, 0],
    [0, 1, 1]
], (255, 0, 0))

bricks = [brick1, brick2, brick3, brick4, brick5, brick6, brick7]
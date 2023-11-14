# Pygame Tetris

Simple pygame tetris just for fun

### demo.gif:
![demo.gif](https://github.com/michael-bill/pygame-tetris/blob/main/demo.gif)

### Game Controls:

    Key a - move the pick to the left
    Key d - move the pick to the right
    Key s - move the pick down
    Key e - rotate the brick 90 degrees clockwise
    Key q - rotate the brick 90 degrees counterclockwise
    Key space - move the brick down

### Install requirements:
```
pip install -r requirements.txt
```

### Run:
```
python3 main.py
```

### Project structure:
``main.py`` - The main file in which the game is launched, the game board is drawn and the game is controlled.<br/>
``brick.py`` - Brick class and created instances of all standard bricks in Tetris.<br/>
``config.py`` - Some configuration data of the game.<br/>
``field.py`` - Class of the playing field (matrix) and functions with implementation of all logic to control it.<br/>
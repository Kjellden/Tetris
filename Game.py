import arcade 
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_SPACE_WIDTH = 300
PLAY_SPACE_HEIGHT = 600
BLOCK_SIZE = 30
SCREEN_TITLE = "Tetris"

TOP_LEFT_X = (SCREEN_WIDTH - PLAY_SPACE_WIDTH) // 2
TOP_LEFT_Y = (SCREEN_HEIGHT // 2) + (PLAY_SPACE_HEIGHT // 2)
START_CENTER_X = (SCREEN_WIDTH - PLAY_SPACE_WIDTH) // 2 + 15
START_CENTER_Y = (SCREEN_HEIGHT // 2) + (PLAY_SPACE_HEIGHT // 2) - 15

# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '0000.',
      '.....',
      '.....',
      '.....'],
     ['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
color = [arcade.color.BLUE, arcade.color.RED, arcade.color.GREEN, arcade.color.PURPLE, arcade.color.ORANGE, arcade.color.YELLOW, arcade.color.PINK]

# class
class Tetris(arcade.Window):
    """
    Main class for the Tetris game.
    """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.grid= self.create_grid()
        self.locked_pos = {}
        self.game_over = False
        self.current_piece = self.get_shape()
        self.next_piece = self.get_shape()
        self.change_piece = False
        self.fall_speed = 5
        self.score = 0
        self.time = 0


    class Piece():
        """
        Class that gives the information on the piece that is being used or that is next in line to use.
        """
        def __init__(self, x, y, shape):
            self.x = x
            self.y = y
            self.shape = shape
            self.color = color[shapes.index(shape)] 
            self.rotation = 0
            self.shape_pos = []

    def on_update(self, delta_time: float = 1/ 60):
        """
        updates the game every time this is called.
        """
        self.time += delta_time
        seconds = int(self.time) % 60
        if seconds == 1:
            self.time = 0
            self.current_piece.y += 1
            if not(self.valid_space(self.current_piece, self.grid)) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                self.change_piece = True
        
            self.current_piece.shape_pos = self.convert_shape_format(self.current_piece)
            for i in range(len(self.current_piece.shape_pos)):
                            x, y = self.current_piece.shape_pos[i]
                            if y > -1:
                                self.grid[y][x] = self.current_piece.color

            if self.change_piece == True:
                for pos in self.current_piece.shape_pos:
                    p = (pos[0], pos[1])
                    self.locked_pos[p] = self.current_piece.color
                self.current_piece = self.next_piece
                self.next_piece = self.get_shape()
                self.change_piece = False
        else:
            self.current_piece.shape_pos = self.convert_shape_format(self.current_piece)
            for i in range(len(self.current_piece.shape_pos)):
                x, y = self.current_piece.shape_pos[i]
                if y > -1:
                    self.grid[y][x] = self.current_piece.color

    def setup(self):
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.draw_next_shape(self.next_piece)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                arcade.draw_rectangle_filled(center_x = START_CENTER_X + j*BLOCK_SIZE, center_y = START_CENTER_Y - i*BLOCK_SIZE, width = BLOCK_SIZE, height =BLOCK_SIZE, color = self.grid[i][j])
                
        self.draw_grid(self.grid)
        self.grid = self.create_grid(self.locked_pos)
        
    def on_key_press(self, symbol, modifiers):
        """
        On a key event the game will move the current peace. The set movements for this game are
        Left arrow: Moves the current peace to the left one tile.
        Right arrow: Moves the current peace to the right one tile.
        Down arrow: Moves the current peace down one tile and resets the move timer.
        Up arrow: Rotates the current peace.
        """
        if symbol == arcade.key.RIGHT: # Moves the peace to the right one tile
            print("this is a key test RIGHT")
            self.current_piece.x += 1
            if not(self.valid_space(self.current_piece, self.grid)):
                self.current_piece.x -= 1  

        if symbol == arcade.key.LEFT: # Moves the peace to the left one tile
            print("this is a key test LEFT")
            self.current_piece.x -= 1
            if not(self.valid_space(self.current_piece, self.grid)):
                self.current_piece.x += 1

        if symbol == arcade.key.DOWN: # Moves the peace down by one tile
            print("this is a key test DOWN")
            self.current_piece.y += 1
            self.time = 0
            if not(self.valid_space(self.current_piece, self.grid)):
                self.current_piece.y -= 1
                self.time = 1
                
        if symbol == arcade.key.UP: # Rotates the peace
            print("this is a key test UP")
            self.current_piece.rotation += 1
            if not(self.valid_space(self.current_piece, self.grid)):
                self.current_piece.rotation -= 1

    def create_grid(self, locked_pos={}):
        """
        Creates a clean grid that only shows the locked in peaces of the game
        clearing this allows up to move the current peace without it hitting itself
        """
        grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in locked_pos:
                    c = locked_pos[(j,i)]
                    grid[i][j] = c
        return grid

    def convert_shape_format(self, shape):
        """
        Convert the shape format of the object into x and y locations for the gird.
        """
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
        return positions

    def valid_space(self, shape, grid):
        """
        Checks to see if the place the peace is about to move to is a valid space or not.
        """
        accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        formatted = self.convert_shape_format(shape)

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def check_lost(self, positions):
        """
        Check to see if the game is over. The game is over when a peace hits the top of set game area.
        """
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

    def get_shape(self):
        """
        Get a new random shape.
        """
        return Tetris.Piece(5, 0, random.choice(shapes))

    def draw_text_middle(self, text, size, color, surface):  
        pass
    
    def draw_grid(self, grid):
        """
        Draw a grid with lines so the player can see the size of the tiles and see what row they are on.
        """
        arcade.draw_rectangle_outline(center_x= TOP_LEFT_X + PLAY_SPACE_WIDTH/2  , center_y= TOP_LEFT_Y - PLAY_SPACE_HEIGHT/2, height = PLAY_SPACE_HEIGHT + 6, width = PLAY_SPACE_WIDTH + 6, border_width= 6, color = arcade.color.RED)

        for i in range(0, len(grid)):
            if i >= 1:
                arcade.draw_line(start_x= TOP_LEFT_X, end_x= TOP_LEFT_X + PLAY_SPACE_WIDTH, start_y= TOP_LEFT_Y - (i * BLOCK_SIZE), end_y= TOP_LEFT_Y - (i * BLOCK_SIZE), color= arcade.color.WHITE)
            for j in range(0, len(grid[i])):
                if j >= 1:
                    arcade.draw_line(start_x= TOP_LEFT_X + (j * BLOCK_SIZE), end_x= TOP_LEFT_X + (j* 30), start_y= TOP_LEFT_Y, end_y= TOP_LEFT_Y - PLAY_SPACE_HEIGHT, color= arcade.color.WHITE)

    def draw_next_shape(self, shape):
        """
        Draws the next shape that will be used in the game
        """
        arcade.draw_text(start_x= SCREEN_WIDTH * 3/4, start_y= SCREEN_HEIGHT * 3 / 4, text= "Next Shape", font_size = 20, align="center",width= 100, color = arcade.color.BLACK)
        format = shape.shape[shape.rotation]
        x_placement = START_CENTER_X + PLAY_SPACE_WIDTH + 30
        y_placement = START_CENTER_Y - PLAY_SPACE_HEIGHT/2 + 50

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0" :
                    arcade.draw_rectangle_filled(center_x= x_placement + (j*BLOCK_SIZE), center_y= y_placement + (i*BLOCK_SIZE), width= BLOCK_SIZE, height= BLOCK_SIZE, color = shape.color)


def main():
    """ Main function """
    game = Tetris(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
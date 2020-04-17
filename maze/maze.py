# Simple Maze Game Using The Recursive Back-Tracker Algorithm
from enum import Enum
import random
import pygame as pg


# Global Settings
SHOW_DRAW = False  # Show the maze being created
SHOW_FPS = False  # Show frames per second in caption
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Maze Size: 36 X 30 is max size for screen of 1200 X 1024
MAZE_WIDTH = 10  # in cells
MAZE_HEIGHT = 10  # in cells
CELL_COUNT = MAZE_WIDTH * MAZE_HEIGHT
BLOCK_SIZE = 8  # Pixel size/Wall thickness
PATH_WIDTH = 3  # Width of pathway in blocks
CELL_SIZE = BLOCK_SIZE * PATH_WIDTH + BLOCK_SIZE  # extra BLOCK_SIZE to include wall to east and south of cell
MAZE_WIDTH_PX = CELL_SIZE * MAZE_WIDTH + BLOCK_SIZE  # extra BLOCK_SIZE to include left edge wall
MAZE_HEIGHT_PX = CELL_SIZE * MAZE_HEIGHT + BLOCK_SIZE  # extra BLOCK_SIZE to include top edge wall
MAZE_TOP_LEFT_CORNER = (SCREEN_WIDTH // 2 - MAZE_WIDTH_PX // 2, SCREEN_HEIGHT // 2 - MAZE_HEIGHT_PX // 2)

# Define the colors we'll need
BACK_COLOR = (100, 100, 100)
WALL_COLOR = (18, 94, 32)
MAZE_COLOR = (255, 255, 255)
UNVISITED_COLOR = (0, 0, 0)
PLAYER1_COLOR = (255, 0, 0)
PLAYER2_COLOR = (0, 0, 255)
MESSAGE_COLOR = (0, 255, 0)


class CellProp(Enum):
    Path_N = 1
    Path_E = 2
    Path_S = 4
    Path_W = 8
    Visited = 16


class Direction(Enum):
    North = (0, -1)
    East = (1, 0)
    South = (0, 1)
    West = (-1, 0)


class Player(pg.sprite.Sprite):
    def __init__(self, color, x, y, radius):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Save the start position
        self.start_x = x
        self.start_y = y

        # Create the rectangular image, fill and set background to transparent
        self.image = pg.Surface([radius * 2, radius * 2])
        self.image.fill(MAZE_COLOR)
        self.image.set_colorkey(MAZE_COLOR)

        # Draw our player onto the transparent rectangle
        pg.draw.circle(self.image, color, (radius, radius), radius)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y


class MazeGenerator:
    direction_to_flag = {
        Direction.North: CellProp.Path_N,
        Direction.East: CellProp.Path_E,
        Direction.South: CellProp.Path_S,
        Direction.West: CellProp.Path_W
    }

    opposite_direction = {
        Direction.North: Direction.South,
        Direction.East: Direction.West,
        Direction.South: Direction.North,
        Direction.West: Direction.East
    }

    def __init__(self):
        # Need to initialize pygame before using it
        pg.init()

        # Create a display surface to draw our game on
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set the title on the window
        pg.display.set_caption('PyMaze')

        # Use a single list to store 2D array
        self.maze = []

        random.seed()

        # Store maze as image after we create it so that we just have to redraw the image on update
        self.maze_image = None

        # Create players
        self.player1 = Player(PLAYER1_COLOR, MAZE_TOP_LEFT_CORNER[0] + BLOCK_SIZE,
                              MAZE_TOP_LEFT_CORNER[1] + BLOCK_SIZE, (BLOCK_SIZE * 3) // 2)
        self.player1_sprite = None

        self.player2 = Player(PLAYER2_COLOR,
                              MAZE_TOP_LEFT_CORNER[0] + MAZE_WIDTH_PX - CELL_SIZE,
                              MAZE_TOP_LEFT_CORNER[1] + MAZE_HEIGHT_PX - CELL_SIZE,
                              (BLOCK_SIZE * 3) // 2)
        self.player2_sprite = None

        self.player1_score = 0
        self.player2_score = 0

        self.round = 1

        self.win1_flag = False
        self.win2_flag = False

    def get_cell_index(self, position):
        x, y = position
        return y * MAZE_WIDTH + x

    def generate_maze(self):
        # Initialize maze with zero values
        self.maze = [0] * CELL_COUNT
        visited_count = 0

        # Start at alternating corners to be more fair
        process_stack = [(0, 0)]
        if self.round % 2 == 0:
            process_stack = [(MAZE_WIDTH - 1, MAZE_HEIGHT - 1)]
            self.maze[CELL_COUNT - 1] |= CellProp.Visited.value
        else:
            process_stack = [(0, 0)]
            self.maze[0] |= CellProp.Visited.value

        visited_count += 1
        while visited_count < CELL_COUNT:
            # Step 1 - Create a list of the unvisited neighbors
            x, y = process_stack[-1]  # get position of top item on stack
            current_cell_index = self.get_cell_index((x, y))

            # Find all unvisited neighbors
            neighbors = []
            for direction in Direction:
                dir = direction.value
                new_x, new_y = (x + dir[0], y + dir[1])
                if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
                    index = self.get_cell_index((new_x, new_y))
                    if not self.maze[index] & CellProp.Visited.value:
                        # Cell was not already visited so add to neighbors list with the direction
                        neighbors.append((new_x, new_y, direction))

            if len(neighbors) > 0:
                # Choose a random neighboring cell
                cell = neighbors[random.randrange(len(neighbors))]
                cell_x, cell_y, cell_direction = cell
                cell_position = (cell_x, cell_y)
                cell_index = self.get_cell_index(cell_position)

                # Create a path between the neighbor and the current cell by setting the direction property flag
                flag_to = MazeGenerator.direction_to_flag[cell_direction]
                flag_from = MazeGenerator.direction_to_flag[MazeGenerator.opposite_direction[cell_direction]]

                self.maze[current_cell_index] |= flag_to.value
                self.maze[cell_index] |= flag_from.value | CellProp.Visited.value

                process_stack.append(cell_position)
                visited_count += 1
            else:
                # Backtrack since there were no unvisited neighbors
                process_stack.pop()

            if SHOW_DRAW:
                self.draw_maze()
                pg.display.update()
                #pg.time.wait(500)
                pg.event.pump()

        # save image of completed maze
        self.draw_maze()
        pg.display.update()
        self.maze_image = self.screen.copy()

    def draw_maze(self):
        self.screen.fill(BACK_COLOR)
        pg.draw.rect(self.screen, WALL_COLOR, (MAZE_TOP_LEFT_CORNER[0], MAZE_TOP_LEFT_CORNER[1],
                                               MAZE_WIDTH_PX, MAZE_HEIGHT_PX))

        for x in range(MAZE_WIDTH):
            for y in range(MAZE_HEIGHT):
                for py in range(PATH_WIDTH):
                    for px in range(PATH_WIDTH):
                        cell_index = self.get_cell_index((x, y))
                        if self.maze[cell_index] & CellProp.Visited.value:
                            self.draw(MAZE_COLOR, x * (PATH_WIDTH + 1) + px, y * (PATH_WIDTH + 1) + py)
                        else:
                            self.draw(UNVISITED_COLOR, x * (PATH_WIDTH + 1) + px, y * (PATH_WIDTH + 1) + py)

                for p in range(PATH_WIDTH):
                    if self.maze[y * MAZE_WIDTH + x] & CellProp.Path_S.value:
                        self.draw(MAZE_COLOR, x * (PATH_WIDTH + 1) + p, y * (PATH_WIDTH + 1) + PATH_WIDTH)

                    if self.maze[y * MAZE_WIDTH + x] & CellProp.Path_E.value:
                        self.draw(MAZE_COLOR, x * (PATH_WIDTH + 1) + PATH_WIDTH, y * (PATH_WIDTH + 1) + p)

        # Color the player exits
        pg.draw.rect(self.screen, PLAYER2_COLOR, (MAZE_TOP_LEFT_CORNER[0],
                     MAZE_TOP_LEFT_CORNER[1] + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE * 3))

        pg.draw.rect(self.screen, PLAYER1_COLOR,
                     (MAZE_TOP_LEFT_CORNER[0] + MAZE_WIDTH_PX - BLOCK_SIZE,
                      MAZE_TOP_LEFT_CORNER[1] + MAZE_HEIGHT_PX - BLOCK_SIZE * 4,
                      BLOCK_SIZE, BLOCK_SIZE * 3))

    def draw(self, color, x, y):
        x_offset = MAZE_TOP_LEFT_CORNER[0] + BLOCK_SIZE
        y_offset = MAZE_TOP_LEFT_CORNER[1] + BLOCK_SIZE
        pg.draw.rect(self.screen, color, (x * BLOCK_SIZE + x_offset,
                                          y * BLOCK_SIZE + y_offset,
                                          BLOCK_SIZE, BLOCK_SIZE))

    def draw_screen(self):
        self.screen.blit(self.maze_image, (0, 0))
        self.player1_sprite.draw(self.screen)
        self.player2_sprite.draw(self.screen)

        font = pg.font.SysFont('Arial', 18, True)

        # Display Scores
        p1_msg = f'PLAYER 1: {self.player1_score}'
        p2_msg = f'PLAYER 2: {self.player2_score}'
        p1_size = font.size(p1_msg)
        p2_size = font.size(p2_msg)
        p1 = font.render(p1_msg, True, PLAYER1_COLOR)
        p2 = font.render(p2_msg, True, PLAYER2_COLOR)
        self.screen.blit(p1, (MAZE_TOP_LEFT_CORNER[0], MAZE_TOP_LEFT_CORNER[1] - p1_size[1]))
        self.screen.blit(p2, (MAZE_TOP_LEFT_CORNER[0] + MAZE_WIDTH_PX - p2_size[0],
                              MAZE_TOP_LEFT_CORNER[1] - p1_size[1]))

        # Display instructions
        p1_msg = 'a w s d to move'
        p2_msg = '← ↑ ↓ → to move'
        p2_size = font.size(p2_msg)
        p1 = font.render(p1_msg, True, PLAYER1_COLOR)
        p2 = font.render(p2_msg, True, PLAYER2_COLOR)
        self.screen.blit(p1, (MAZE_TOP_LEFT_CORNER[0], MAZE_TOP_LEFT_CORNER[1] + MAZE_HEIGHT_PX + 2))
        self.screen.blit(p2, (MAZE_TOP_LEFT_CORNER[0] + MAZE_WIDTH_PX - p2_size[0],
                              MAZE_TOP_LEFT_CORNER[1] + MAZE_HEIGHT_PX + 2))

        pg.display.update()

    def display_win(self):
        msg = 'Player 1 Wins!!!' if self.win1_flag else 'Player 2 Wins!!!'

        self.round += 1
        if self.win1_flag:
            self.player1_score += 1
        else:
            self.player2_score += 1

        font = pg.font.SysFont('Arial', 72, True)
        size = font.size(msg)
        s = font.render(msg, True, MESSAGE_COLOR, (0, 0, 0))
        self.screen.blit(s, (SCREEN_WIDTH // 2 - size[0] // 2, SCREEN_HEIGHT // 2 - size[1] // 2))
        pg.display.update()
        pg.time.wait(3000)

    def can_move(self, direction, player):
        # Top left corner of first cell
        corner_offset_x = MAZE_TOP_LEFT_CORNER[0] + BLOCK_SIZE
        corner_offset_y = MAZE_TOP_LEFT_CORNER[1] + BLOCK_SIZE

        # Calculate which cells the player occupies
        square = BLOCK_SIZE * 4
        p1 = (player.rect.x - corner_offset_x, player.rect.y - corner_offset_y)
        p2 = (p1[0] + square - 1, p1[1] + square - 1)
        player_pos1 = (p1[0] // square, p1[1] // square)
        player_pos2 = (p2[0] // square, p2[1] // square)
        cell_index1 = self.get_cell_index((player_pos1[0], player_pos1[1]))
        cell_index2 = self.get_cell_index((player_pos2[0], player_pos2[1]))

        functions = {
            Direction.North: self.can_move_up,
            Direction.East: self.can_move_right,
            Direction.South: self.can_move_down,
            Direction.West: self.can_move_left
        }

        # Check for maze exit/win
        # Check if player is at opposing player's start x,y
        if self.player1.rect.x == self.player2.start_x and self.player1.rect.y == self.player2.start_y:
            self.win1_flag = True
        elif self.player2.rect.x == self.player1.start_x and self.player2.rect.y == self.player1.start_y:
            self.win2_flag = True

        return functions[direction](cell_index1, cell_index2)

    def can_move_up(self, index1, index2):
        if index1 == index2:
            return self.maze[index1] & CellProp.Path_N.value
        else:
            return index2 == index1 + MAZE_WIDTH

    def can_move_right(self, index1, index2):
        if index1 == index2:
            return self.maze[index1] & CellProp.Path_E.value
        else:
            return index2 == index1 + 1

    def can_move_down(self, index1, index2):
        if index1 == index2:
            return self.maze[index1] & CellProp.Path_S.value
        else:
            return index2 == index1 + MAZE_WIDTH

    def can_move_left(self, index1, index2):
        if index1 == index2:
            return self.maze[index1] & CellProp.Path_W.value
        else:
            return index2 == index1 + 1

    def move_up(self, player):
        if self.can_move(Direction.North, player):
            player.rect.y -= 1

    def move_right(self, player):
        if self.can_move(Direction.East, player):
            player.rect.x += 1

    def move_down(self, player):
        if self.can_move(Direction.South, player):
            player.rect.y += 1

    def move_left(self, player):
        if self.can_move(Direction.West, player):
            player.rect.x -= 1

    def initialize(self):
        self.player1_sprite = None
        self.player1.reset()
        self.player2_sprite = None
        self.player2.reset()

        self.generate_maze()
        self.player1_sprite = pg.sprite.RenderPlain(self.player1)
        self.player2_sprite = pg.sprite.RenderPlain(self.player2)

    def run_game(self):
        clock = pg.time.Clock()
        self.initialize()

        # Main game loop
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False

            if not self.win1_flag and not self.win2_flag:
                keys = pg.key.get_pressed()
                if keys[pg.K_LEFT]:
                    self.move_left(self.player2)
                if keys[pg.K_RIGHT]:
                    self.move_right(self.player2)
                if keys[pg.K_UP]:
                    self.move_up(self.player2)
                if keys[pg.K_DOWN]:
                    self.move_down(self.player2)
                if keys[pg.K_a]:
                    self.move_left(self.player1)
                if keys[pg.K_d]:
                    self.move_right(self.player1)
                if keys[pg.K_w]:
                    self.move_up(self.player1)
                if keys[pg.K_s]:
                    self.move_down(self.player1)

                if self.win1_flag or self.win2_flag:
                    self.display_win()
                    self.initialize()
                    self.win1_flag = self.win2_flag = False

                self.draw_screen()

                if SHOW_FPS:
                    pg.display.set_caption(f'PyMaze ({str(int(clock.get_fps()))} FPS)')
                    clock.tick()

        pg.quit()


mg = MazeGenerator()
mg.run_game()
import pygame
import colors
from random import shuffle
from Tile import Tile

class Grid:
    def __init__(self, width: int, rows: int) -> None:
        self.rows: int = rows
        self.grid: list[Tile] = []
        self.width: int = width
        self.gap: int = self.width // self.rows
        self.gap_row: int = None
        self.gap_col: int = None
        self.solved: bool = False
        self.__make_grid()

    def __make_grid(self) -> None:
        self.grid: list[Tile] = []
        nums: list[int] = list(range(self.rows * self.rows))
        shuffle(nums)
        for i in range(self.rows):
            self.grid.append([])

            for j in range(self.rows):
                num: int = nums[self.rows*i + j]
                if (num == 0):
                    self.gap_row: int = i
                    self.gap_col: int = j
                tile: Tile = Tile(i, j, self.gap, num)
                self.grid[i].append(tile)

    def __draw_gridlines(self, win) -> None:

        for i in range(self.rows):
            pos: int = i * self.gap
            pygame.draw.line(win, colors.BLACK, (0, pos), (self.width, pos))
            pygame.draw.line(win, colors.BLACK, (pos, 0), (pos, self.width))

    def draw(self, win: pygame.display) -> None:
        # Fill the screen with white (clear the display essentially)
        win.fill(colors.WHITE)

        # Draw the tiles
        for row in self.grid:
            for tile in row:
                tile.draw(win)
        
        # Draw the grid lines
        self.__draw_gridlines(win)

        # Update the display
        pygame.display.update()

    def move_tile(self, row, col) -> bool:
        tile: Tile = self.grid[row][col]
        gap_tile: Tile = self.grid[self.gap_row][self.gap_col]

        if tile.move(gap_tile):
            self.gap_row: int = row
            self.gap_col: int = col
            return True

        else:
            return False
    
    def move_left(self):
        if self.gap_row == 0:
            return False

        else:
            self.grid[self.gap_row][self.gap_col].swap(self.grid[self.gap_row - 1][self.gap_col])
            self.gap_row: int = self.gap_row - 1
            return True

    def move_right(self):
        if self.gap_row == self.rows - 1:
            return False

        else:
            self.grid[self.gap_row][self.gap_col].swap(self.grid[self.gap_row + 1][self.gap_col])
            self.gap_row: int = self.gap_row + 1
            return True

    def move_up(self):
        if self.gap_col == 0:
            return False

        else:
            self.grid[self.gap_row][self.gap_col].swap(self.grid[self.gap_row][self.gap_col - 1])
            self.gap_col: int = self.gap_col - 1
            return True


    def move_down(self):
        if self.gap_col == self.rows - 1:
            return False

        else:
            self.grid[self.gap_row][self.gap_col].swap(self.grid[self.gap_row][self.gap_col + 1])
            self.gap_col: int = self.gap_col + 1
            return True
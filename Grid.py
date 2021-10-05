import pygame
import pygame.freetype
import colors
from random import shuffle
from Tile import Tile
from typing import List

class Grid:
    def __init__(self, width: int, rows: int) -> None:
        self.rows: int = rows
        self.grid: List[Tile] = []
        self.width: int = width
        self.gap: int = self.width // self.rows
        self.gap_pos: int = None
        self.solved: bool = False
        self.make_grid()



    def make_grid(self) -> None:
        self.grid: List[Tile] = []
        nums: List[int] = list(range(1, (self.rows * self.rows) + 1))
        shuffle(nums)

        while (not self.solvable(nums)):
            shuffle(nums)

        for i in range(len(nums)):
            num: int = nums[i]
            if (num == (self.rows*self.rows)):
                self.gap_pos: int = i
            tile: Tile = Tile(i // self.rows, i % self.rows, self.gap, num, self.rows)
            self.grid.append(tile)
        
        if self.is_solved():
            self.make_grid()



    def get_grid(self):
        return self.grid



    def get_gap(self) -> int:
        return self.gap_pos



    def fill_solution(self, move: int) -> None:
        # Move left
        if move == 0:
            self.grid[self.gap_pos - 1].set_color(colors.GREEN)

        # Move right
        elif move == 1:
            self.grid[self.gap_pos + 1].set_color(colors.GREEN)

        # Move up
        elif move == 2:
            self.grid[self.gap_pos - self.rows].set_color(colors.GREEN)

        # Move Down
        elif move == 3:
            self.grid[self.gap_pos + self.rows].set_color(colors.GREEN)



    def update_solver(self, expected_move: int, move: int, gap: int) -> bool:
        if expected_move == move:
            self.grid[gap].set_color(colors.WHITE)
            return True

        return False


    def draw_gridlines(self, win) -> None:

        for i in range(self.rows):
            pos: int = i * self.gap
            pygame.draw.line(win, colors.BLACK, (0, pos), (self.width, pos))
            pygame.draw.line(win, colors.BLACK, (pos, 0), (pos, self.width))



    def draw(self, win, grid_width, extra_width, time, mins) -> None:

        # Fill the screen with white (clear the display essentially)
        win.fill(colors.WHITE, (0, 0, grid_width, grid_width))
        win.fill(colors.GRAY, (grid_width, 0, extra_width, grid_width))

        # Draw the tiles
        for tile in self.grid:
            tile.draw(win)
        
        # Draw the grid lines
        self.draw_gridlines(win)



    def move_tile(self, row, col) -> bool:
        if row >= self.rows:
            return False
        if row < 0:
            return False
        if col >= self.rows:
            return False
        if col < 0:
            return False
        pos = self.rows * row + col

        if self.grid[pos].move(self.grid[self.gap_pos]):
            self.gap_pos = pos
            return True

        else:
            return False
    


    def move_left(self) -> bool:
        if (self.gap_pos % self.rows) == 0:
            return False

        else:
            self.grid[self.gap_pos].swap(self.grid[self.gap_pos - 1])
            self.gap_pos: int = self.gap_pos - 1
            return True




    def move_right(self) -> bool:
        if (self.gap_pos % self.rows) == (self.rows - 1):
            return False

        else:
            self.grid[self.gap_pos].swap(self.grid[self.gap_pos + 1])
            self.gap_pos: int = self.gap_pos + 1
            return True



    def move_up(self) -> bool:
        if (self.gap_pos // self.rows) == 0:
            return False

        else:
            self.grid[self.gap_pos].swap(self.grid[self.gap_pos - self.rows])
            self.gap_pos: int = self.gap_pos - self.rows
            return True



    def move_down(self) -> bool:
        if (self.gap_pos // self.rows) == (self.rows - 1):
            return False

        else:
            self.grid[self.gap_pos].swap(self.grid[self.gap_pos + self.rows])
            self.gap_pos: int = self.gap_pos + self.rows
            return True



    def is_solved(self) -> bool:
        for i in range(len(self.grid)):
            if self.grid[i].get_num() != (i + 1):
                return False
        
        return True

    
    def solvable(self, nums: List[int]) -> bool:
        inversions: int = 0
        for i in range(len(nums)):
            if nums[i] == 1:
                continue

            if nums[i] == (self.rows * self.rows):
                gap_row = i // self.rows
                continue

            for j in range(i + 1, len(nums)):
                if nums[i] > nums[j]:
                    inversions: int = inversions + 1

        if (self.rows % 2) == 0:
            if ((inversions % 2) != (gap_row % 2)):
                return True
            else:
                return False

        else:
            if (inversions % 2) == 0:
                return True
            else:
                return False
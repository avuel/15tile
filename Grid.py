import pygame
import pygame.freetype
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
        self.make_grid()



    def make_grid(self) -> None:
        self.grid: list[Tile] = []
        nums: list[int] = list(range(1, (self.rows * self.rows) + 1))
        shuffle(nums)
        for i in range(self.rows):
            self.grid.append([])

            for j in range(self.rows):
                num: int = nums[self.rows*j + i]
                if (num == (self.rows*self.rows)):
                    self.gap_row: int = i
                    self.gap_col: int = j
                tile: Tile = Tile(i, j, self.gap, num, self.rows)
                self.grid[i].append(tile)
                
        if self.is_solved():
            self.make_grid()



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
        for row in self.grid:
            for tile in row:
                tile.draw(win)
        
        # Draw the grid lines
        self.draw_gridlines(win)

        # Draw the restart button
        restart_x: int = grid_width + extra_width // 6
        restart_y: int = 3 * grid_width // 5
        restart_width: int = 2 * extra_width // 3
        restart_height: int = grid_width / 12
        pygame.draw.rect(win, colors.WHITE, (restart_x, restart_y, restart_width, restart_height))
        text: pygame.freetype.Font = pygame.freetype.Font('cour.ttf', 36)
        text.render_to(win, (restart_x + restart_width / 6, restart_y + 7 * restart_height / 20), "restart", colors.BLACK)
        
        # Draw border of restart button
        pygame.draw.line(win, colors.BLACK, (restart_x, restart_y), (restart_x + restart_width, restart_y))
        pygame.draw.line(win, colors.BLACK, (restart_x, restart_y), (restart_x, restart_y + restart_height))
        pygame.draw.line(win, colors.BLACK, (restart_x + restart_width, restart_y), (restart_x + restart_width, restart_y + restart_height))
        pygame.draw.line(win, colors.BLACK, (restart_x, restart_y + restart_height), (restart_x + restart_width, restart_y + restart_height))

        # Draw the timer window
        timer_x: int = grid_width + extra_width // 6
        timer_y: int = grid_width // 5
        timer_width: int = 2 * extra_width // 3
        timer_height: int = grid_width / 12
        pygame.draw.rect(win, colors.WHITE, (timer_x, timer_y, timer_width, timer_height))
        #if time < 60000:
        #    text.render_to(win, (timer_x + timer_width / 4, timer_y + timer_height / 3), "{:.2f}".format(time / 1000) + "s", colors.BLACK)
        #else:
        if mins < 10:
            text.render_to(win, (timer_x + (32 * timer_width / 100), timer_y + (7 * timer_height / 20)), f"{mins:01d}" + ":" + f"{(time - time % 100) // 1000:02d}", colors.BLACK)
        else:
            text.render_to(win, (timer_x + (32 * timer_width / 100) - 22, timer_y + (7 * timer_height / 20)), f"{mins:02d}" + ":" + f"{(time - time % 100) // 1000:02d}", colors.BLACK)
            
        # Draw border of timer button
        pygame.draw.line(win, colors.BLACK, (timer_x, timer_y), (timer_x + timer_width, timer_y))
        pygame.draw.line(win, colors.BLACK, (timer_x, timer_y), (timer_x, timer_y + restart_height))
        pygame.draw.line(win, colors.BLACK, (timer_x + timer_width, timer_y), (timer_x + timer_width, timer_y + timer_height))
        pygame.draw.line(win, colors.BLACK, (timer_x, timer_y + timer_height), (timer_x + timer_width, timer_y + timer_height))

        # Update the display
        pygame.display.update()



    def move_tile(self, row, col) -> bool:
        if row >= self.rows:
            return False
        if row < 0:
            return False
        if col >= self.rows:
            return False
        if col < 0:
            return False
        tile: Tile = self.grid[row][col]
        gap_tile: Tile = self.grid[self.gap_row][self.gap_col]

        if tile.move(gap_tile):
            self.gap_row: int = row
            self.gap_col: int = col
            return True

        else:
            return False
    


    def move_left(self) -> bool:
        if self.gap_row == 0:
            return False

        else:
            self.grid[self.gap_row][self.gap_col].swap(self.grid[self.gap_row - 1][self.gap_col])
            self.gap_row: int = self.gap_row - 1
            return True



    def move_right(self) -> bool:
        if self.gap_row == self.rows - 1:
            return False

        else:
            self.grid[self.gap_row][self.gap_col].swap(self.grid[self.gap_row + 1][self.gap_col])
            self.gap_row: int = self.gap_row + 1
            return True



    def move_up(self) -> bool:
        if self.gap_col == 0:
            return False

        else:
            self.grid[self.gap_row][self.gap_col].swap(self.grid[self.gap_row][self.gap_col - 1])
            self.gap_col: int = self.gap_col - 1
            return True



    def move_down(self) -> bool:
        if self.gap_col == self.rows - 1:
            return False

        else:
            self.grid[self.gap_row][self.gap_col].swap(self.grid[self.gap_row][self.gap_col + 1])
            self.gap_col: int = self.gap_col + 1
            return True



    def is_solved(self) -> bool:
        for i in range(self.rows):
            for j in range(self.rows):
                if self.grid[j][i].get_num() != (self.rows*i + j + 1):
                    return False
        
        return True
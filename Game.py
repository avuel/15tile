import pygame
import pygame.freetype
import numpy as np
from collections import deque
from Grid import Grid
from Button import Button
from Tile import Tile
from typing import Deque, List
#sys.setrecursionlimit(4000)
#print(sys.getrecursionlimit())

class Game:
    def __init__(self, grid_width: int, extra_width: int, clock, fps: int, rows: int) -> None:
        self.grid: Grid = Grid(grid_width, rows)
        self.grid_width: int = grid_width
        self.extra_width: int = extra_width
        self.clock = clock
        self.fps: int = fps
        self.rows: int = rows
        self.buttons: list(Button) = []

        self.running: bool = True
        self.solved: bool = False
        self.time: int = 0
        self.mins: int = 0
        self.clicks: int = 0
        print(self.solve_grid())



    def is_running(self) -> bool:
        return self.running



    def get_clicked_pos(self, x: int, y: int, rows: int, width: int) -> int:
        gap: int = width // rows

        # Find the row, column that the mouse click occured in
        row: int = y // gap
        col: int = x // gap

        return row, col



    def add_button(self, name: str, x: int, y: int, width: int, height: int, button_color, text: str, text_x: int, text_y: int, text_color, border_color) -> None:
        self.buttons.append(Button(name, x, y, width, height, button_color, text, text_x, text_y, text_color, border_color))



    def draw(self, win) -> None:
        # Draw the grid (updated tiles)
        self.grid.draw(win, self.grid_width, self.extra_width, self.time, self.mins)

        # Draw the buttons
        for button in self.buttons:

            # Update the text of the timer based on the amount of minutes (hopefully we don't solve it slower than 99 minutes)
            if (button.get_name() == "Timer"):
    
                if (self.mins < 10):
                    time: str = f"{self.mins:01d}" + ":" + f"{(self.time - self.time % 100) // 1000:02d}"
                    button.set_text_x(button.get_x() + (32 * button.get_width() / 100))

                else:
                    time: str = f"{self.mins}" + ":" + f"{(self.time - self.time % 100) // 1000:02d}"
                    button.set_text_x(button.get_x() + (32 * button.get_width() / 100) - 22)

                button.set_text(time)

            elif (button.get_name() == "Fps Counter"):
                button.set_text(str(int(round(self.clock.get_fps()))))
                button.draw_text(win)
                continue

            elif (button.get_name() == "Clicks Counter"):
                button.set_text(str(self.clicks))
                clicks: int = self.clicks
                shifts_left: int = 0

                while (clicks > 9):
                    shifts_left: int = shifts_left + 22
                    clicks: int = clicks // 100

                button.set_text_x(button.get_x() + (button.get_width() / 2) - shifts_left)

            # Draw the button
            button.draw(win)
            
        # Finally update the display
        pygame.display.update()



    def update(self, win) -> None:
        # Exit if we are not running
        if not (self.running):
            return None

        # Control the framerate
        self.clock.tick(self.fps)

        if not self.solved:
            self.time: int = self.time + self.clock.get_time()
            if (self.time // 60000) > 0:
                self.mins: int = self.mins + 1
                self.time: int = self.time - 60000
                
        # Draw the game
        self.draw(win)

        for event in pygame.event.get():
            
            # See if we want to quit
            if event.type == pygame.QUIT:
                self.running: bool = False
                return None
            
            # Check if left mouse was pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    y,x = pos

                    # If we are in the grid and we have not solved the puzzle, try to move
                    if (y <= self.grid_width) and (not self.solved):
                        row, col = self.get_clicked_pos(x, y, self.rows, self.grid_width)
                        if self.grid.move_tile(row, col):
                            self.solved: bool = self.grid.is_solved()
                            self.clicks: int = self.clicks + 1

                    # Otherwise, if we are out of the grid and we click on restart, restart (even if solved)
                    else:
                        restart_x: int = self.grid_width + self.extra_width // 6
                        restart_y: int = 3 * self.grid_width // 5
                        restart_width: int = 2 * self.extra_width // 3
                        restart_height: int = self.grid_width / 12

                        if (y >= restart_x) and (y <= (restart_x + restart_width)):
                            if (x >= restart_y) and (x <= (restart_y + restart_height)):
                                self.grid.make_grid()
                                self.solved: bool = self.grid.is_solved()
                                print(self.solve_grid())
                                self.time: int = 0
                                self.mins: int = 0
                                self.clicks: int = 0

            elif self.solved:
                continue

            # Handle Keyboard presses, check if the board is solved after each press
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.grid.move_left():
                        self.solved: bool = self.grid.is_solved()
                        self.clicks: int = self.clicks + 1

                elif event.key == pygame.K_RIGHT:
                    if self.grid.move_right():
                        self.solved: bool = self.grid.is_solved()
                        self.clicks: int = self.clicks + 1

                elif event.key == pygame.K_DOWN:
                    if self.grid.move_down():
                        self.solved: bool = self.grid.is_solved()
                        self.clicks: int = self.clicks + 1

                elif event.key == pygame.K_UP:
                    if self.grid.move_up():
                        self.solved: bool = self.grid.is_solved()
                        self.clicks: int = self.clicks + 1

            #print(self.convert_grid())



    def convert_grid(self) -> List[int]:
        grid: List[int] = list(range(0, (self.rows * self.rows)))
        tiles: List[Tile] = self.grid.get_grid()
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                #num = grid[j][i].get_num()
                #print(num)
                grid[self.rows*i + j] = tiles[j][i].get_num()

        return grid


    
    def solve_grid(self) -> bool:
        start_grid: List[int] = self.convert_grid()
        f_bound: int = 50
        F_BOUND: int = 55

        while (f_bound < F_BOUND):
            path: Deque[List[int]] = []
            path.append(start_grid)
            explored: List[List[int]] = []
            if self.explore(path, explored, f_bound):
                if len(path) > 0:
                    if self.h(path[-1]) == 0:
                        break
            f_bound: int = f_bound + 5
        
        if f_bound >= F_BOUND:
            print("didnt find")
        
        else:
            print("found in " + str(len(path)) + " steps")
            print("visited a total of " + str(len(explored)) + " nodes")


    def h(self, grid: List[int]) -> int:
        sum: int = 0
        for i in range(len(grid)):
            row: int = i // self.rows
            col: int = i % self.rows
            end_row: int = (grid[i] - 1) // self.rows
            end_col: int = (grid[i] - 1) % self.rows
            sum: int = sum + abs(row - end_row) + abs(col - end_col)

        return sum


    def explore(self, path: Deque[List[int]], explored: List[List[int]], f_bound: int):
        # If our path is empty we have no states left to search, so return
        if len(path) == 0:
            return False

        current = path[-1]
        print(current)
        # If we are looking at a state outside of our bounds, we do not want to continue so return
        if (self.h(current) + len(path)) > f_bound:
            return False

        # If our heuristic is 0, we have found a solution path (so stop searching)
        if (self.h(current) == 0):
            return False

        # Find the current position of the gap so we can check available moves
        gap_pos = current.index(self.rows * self.rows)
        visited: bool = False

        # Left (column > 0)
        if (gap_pos % self.rows) > 0:
            print("left")
            current[gap_pos], current[gap_pos - 1] = current[gap_pos - 1], current[gap_pos]
            a = np.array(current)

            # Check if we visited this before on our current path
            for state in path:
                b = np.array(state)
                if (a == b).all():
                    visited: bool = True
                    break
            
            # Or if we have explored this state in a different path
            for state in explored:
                if visited:
                    break
                b = np.array(state)
                if (a == b).all():
                    visited: bool = True

            # If we have not visited it before, add it to the current path and then explore that path
            if not visited:
                path.append(current)
                self.explore(path, explored, f_bound)
                    

        # Right (column < self.rows (max columns))
        if (gap_pos % self.rows) < (self.rows - 1):
            print("right")
            current[gap_pos], current[gap_pos + 1] = current[gap_pos + 1], current[gap_pos]
            a = np.array(current)

            # Check if we visited this before on our current path
            for state in path:
                b = np.array(state)
                if (a == b).all():
                    visited: bool = True
                    break
            
            # Or if we have explored this state in a different path
            for state in explored:
                if visited:
                    break
                b = np.array(state)
                if (a == b).all():
                    visited: bool = True

            # If we have not visited it before, add it to the current path and then explore that path
            if not visited:
                path.append(current)
                self.explore(path, explored, f_bound)

        # Up (row > 0)
        if (gap_pos // self.rows) > 0:
            print("up")
            current[gap_pos], current[gap_pos - self.rows] = current[gap_pos - self.rows], current[gap_pos]
            a = np.array(current)

            # Check if we visited this before on our current path
            for state in path:
                b = np.array(state)
                if (a == b).all():
                    visited: bool = True
                    break
            
            # Or if we have explored this state in a different path
            for state in explored:
                if visited:
                    break
                b = np.array(state)
                if (a == b).all():
                    visited: bool = True

            # If we have not visited it before, add it to the current path and then explore that path
            if not visited:
                path.append(current)
                self.explore(path, explored, f_bound)

        # Down (row < self.rows):
        if (gap_pos // self.rows) < (self.rows - 1):
            print("down")
            current[gap_pos], current[gap_pos + self.rows] = current[gap_pos + self.rows], current[gap_pos]
            a = np.array(current)

            # Check if we visited this before on our current path
            for state in path:
                b = np.array(state)
                if (a == b).all():
                    visited: bool = True
                    break
            
            # Or if we have explored this state in a different path
            for state in explored:
                if visited:
                    break
                b = np.array(state)
                if (a == b).all():
                    visited: bool = True

            # If we have not visited it before, add it to the current path and then explore that path
            if not visited:
                path.append(current)
                self.explore(path, explored, f_bound)

        # This means we have explored all the posibilites of a node and cannot move (at least to a new state)
        explored.append(path.pop())
        return True
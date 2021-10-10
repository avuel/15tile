import pygame
import pygame.freetype
import buttons as b
import numpy as np
from collections import deque
from Grid import Grid
from Button import Button
from Tile import Tile
from typing import Deque, List
import cProfile
import pstats

class Game:
    def __init__(self, grid_width: int, extra_width: int, clock, fps: int, rows: int) -> None:
        self.grid: Grid = Grid(grid_width, rows)
        self.grid_width: int = grid_width
        self.extra_width: int = extra_width
        self.clock = clock
        self.fps: int = fps
        self.rows: int = rows
        self.buttons: List[Button] = []

        self.running: bool = True
        self.playing: bool = False
        self.solved: bool = False
        self.time: int = 0
        self.mins: int = 0
        self.clicks: int = 0

        self.moves: Deque[int] = deque([])

        with cProfile.Profile() as pr:
            self.solve_grid()

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        #stats.print_stats()
        stats.dump_stats(filename='timing_statistics.prof')



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
        if len(self.moves) > 0:
            self.grid.fill_solution(self.moves[0])

        # If we have no solution moves, make every tile white
        else:
            grid = self.grid.get_grid()

            for tile in grid:
                if tile.get_color() == b.sol_on_clr:
                    tile.set_color(b.sol_off_clr)
                    break

        self.grid.draw(win, self.grid_width, self.extra_width, self.time, self.mins)

        # Draw the buttons
        for button in self.buttons:

            # Update the text of the timer based on the amount of minutes (hopefully we don't solve it slower than 99 minutes)
            if (button.get_name() == b.timer_name):
    
                if (self.mins < 10):
                    time: str = f"{self.mins:01d}" + ":" + f"{(self.time - self.time % 100) // 1000:02d}"
                    button.set_text_x(button.get_x() + (32 * button.get_width() / 100))

                else:
                    time: str = f"{self.mins}" + ":" + f"{(self.time - self.time % 100) // 1000:02d}"
                    button.set_text_x(button.get_x() + (32 * button.get_width() / 100) - 22)

                button.set_text(time)

            elif (button.get_name() == b.fps_name):
                button.set_text(str(int(round(self.clock.get_fps()))))
                button.draw_text(win)
                continue

            elif (button.get_name() == b.clks_name):
                button.set_text(str(self.clicks))
                clicks: int = self.clicks
                shifts_left: int = 0

                while (clicks > 9):
                    shifts_left: int = shifts_left + 22
                    clicks: int = clicks // 100

                button.set_text_x(button.get_x() + (button.get_width() / 2) - shifts_left)
            
            elif (button.get_name() == b.sol_name):
                if len(self.moves) == 0:
                    button.set_color(b.sol_off_clr)

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

        if (not self.solved) and self.playing:
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
                        self.playing: bool = True
                        row, col = self.get_clicked_pos(x, y, self.rows, self.grid_width)
                        gap1: int = self.grid.get_gap()
                        if self.grid.move_tile(col, row):
                            self.solved: bool = self.grid.is_solved()
                            self.clicks: int = self.clicks + 1

                            if len(self.moves) > 0:
                                gap2: int = self.grid.get_gap()
                                move: int = -1
                                if (gap2 - gap1) == -1:
                                    move = 0
                                elif (gap2 - gap1) == 1:
                                    move = 1
                                elif (gap2 - gap1) == -self.rows:
                                    move = 2
                                elif (gap2 - gap1) == self.rows:
                                    move = 3
                                if self.grid.update_solver(self.moves[0], move, gap1):
                                    self.moves.popleft()
                                else:
                                    self.moves = []
                                        

                    # Otherwise, if we are out of the grid and we click on a button (restart or solve)
                    else:
                        # Clicked on a button
                        if (y >= b.rest_x) and (y <= (b.rest_x + b.rest_wdth)):

                            # Clicked on restart
                            if (x >= b.rest_y) and (x <= (b.rest_y + b.rest_hght)):
                                self.grid.make_grid()
                                self.solved: bool = self.grid.is_solved()
                                self.time: int = 0
                                self.mins: int = 0
                                self.clicks: int = 0
                                self.playing: bool = False

                                for button in self.buttons:
                                    if button.get_name() == b.sol_name:
                                        button.set_color(b.sol_off_clr)
                                        break
                                
                                self.moves = []

                            # If we did not click on restart just continue
                            elif self.solved:
                                continue
                            
                            # If the puzzle is not solved, check if we clicked on solve
                            elif (x >= b.sol_y) and (x <= (b.sol_y + b.sol_hght)):
                                
                                self.moves: Deque[int] = self.solve_grid()
                                if len(self.moves) > 0:
                                    self.moves.popleft()
                                    #print("moves: " + str(len(self.moves)))
                                    for button in self.buttons:
                                        if button.get_name() == b.sol_name:
                                            button.set_color(b.sol_on_clr)
                                            break

            elif self.solved:
                continue

            # Handle Keyboard presses, check if the board is solved after each press
            elif event.type == pygame.KEYDOWN:
                self.playing: bool = True
                gap: int = self.grid.get_gap()
                if event.key == pygame.K_LEFT:
                    if self.grid.move_left():
                        self.solved: bool = self.grid.is_solved()
                        self.clicks: int = self.clicks + 1
                        if len(self.moves) > 0:
                            if self.moves[0] == 0:
                                self.grid.update_solver(0, 0, gap)
                                self.moves.popleft()
                            else:
                                self.moves = []

                elif event.key == pygame.K_RIGHT:
                    if self.grid.move_right():
                        self.solved: bool = self.grid.is_solved()
                        self.clicks: int = self.clicks + 1
                        if len(self.moves) > 0:
                            if self.moves[0] == 1:
                                self.grid.update_solver(1, 1, gap)
                                self.moves.popleft()
                            else:
                                self.moves = []

                elif event.key == pygame.K_UP:
                    if self.grid.move_up():
                        self.solved: bool = self.grid.is_solved()
                        self.clicks: int = self.clicks + 1
                        if len(self.moves) > 0:
                            if self.moves[0] == 2:
                                self.grid.update_solver(2, 2, gap)
                                self.moves.popleft()
                            else:
                                self.moves = []

                elif event.key == pygame.K_DOWN:
                    if self.grid.move_down():
                        self.solved: bool = self.grid.is_solved()
                        self.clicks: int = self.clicks + 1
                        if len(self.moves) > 0:
                            if self.moves[0] == 3:
                                self.grid.update_solver(3, 3, gap)
                                self.moves.popleft()
                            else:
                                self.moves = []
                


    def convert_grid(self) -> np.ndarray:
        temp_grid: List[int] = []
        tiles: List[Tile] = self.grid.get_grid()
        for i in range(len(tiles)):
            temp_grid.append(tiles[i].get_num())

        grid: np.ndarray = np.array(temp_grid)

        return grid


    
    def solve_grid(self) -> Deque[int]:
        start_grid: np.ndarray = self.convert_grid()
        f_bound: int = 5
        MAX_BOUND: int = 50
        
        while(f_bound <= MAX_BOUND):
            path: Deque[np.ndarray] = deque([])
            moves: Deque[int] = deque([])
            path.append(start_grid)
            moves.append(-1)
            gap: int = self.grid.get_gap()
            if self.explore(path, moves, gap, f_bound):
                if self.h(path[-1]) == 0:
                    break
            print(f_bound)
            f_bound: int = f_bound + 1

        if f_bound > MAX_BOUND:
            return []
        
        elif self.h(path[-1]) == 0:
            return moves
        
        else:
            return []



    def h(self, grid: np.ndarray) -> int:
        sum: int = 0
        for i in range(self.rows * self.rows):
            sum: int = sum + abs((i // self.rows) - ((grid[i] - 1) // self.rows)) + abs((i % self.rows) - ((grid[i] - 1) % self.rows))
        return sum


    def explore(self, path: Deque[np.ndarray], moves: Deque[int], gap: int, f_bound: int) -> bool:
        if self.h(path[-1]) == 0:
            return True
        
        # If we moved right last (1), dont try to move left
        if moves[-1] !=  1:
            if self.move_left(path, moves, gap, f_bound):
                self.explore(path, moves, gap - 1, f_bound)

        # If we moved down last (3), dont try to move up
        if (moves[-1] != 3):
            if self.move_up(path, moves, gap, f_bound):
                self.explore(path, moves, gap - self.rows, f_bound)

        # If we moved left last (0)
        if moves[-1] != 0:
            if self.move_right(path, moves, gap, f_bound):
                self.explore(path, moves, gap + 1, f_bound)

        # If we moved up last (2), dont try to move down
        if moves[-1] != 2:
            if self.move_down(path, moves, gap, f_bound):
                self.explore(path, moves, gap + self.rows, f_bound)

        if self.h(path[-1]) == 0:
            return True

        path.pop()
        moves.pop()
        
        if (len(path)) == 0:
            return False

        if (len(moves)) == 0:
            return False



    # Move code 0
    def move_left(self, path: Deque[np.ndarray], moves: Deque[int], gap: int, f_bound: int) -> bool:
        if (gap % self.rows) > 0:
            grid: np.ndarray = np.copy(path[-1])
            grid[[gap - 1, gap]] = grid[[gap, gap - 1]]
            f = self.h(grid) + (len(path) - 1)
            
            if f > f_bound:
                return False

            for state in path:
                if (state == grid).all():
                    return False

            path.append(grid)
            moves.append(0)
            return True

        return False



    # Move code 1
    def move_right(self, path: Deque[np.ndarray], moves: Deque[int], gap: int, f_bound: int) -> bool:
        if (gap % self.rows) < (self.rows - 1):
            grid: np.ndarray = np.copy(path[-1])
            grid[[gap + 1, gap]] = grid[[gap, gap + 1]]
            f = self.h(grid) + (len(path) - 1)

            if f > f_bound:
                return False

            for state in path:
                if (state == grid).all():
                    return False
            
            path.append(grid)
            moves.append(1)
            return True
            
        return False



    # Move code 2
    def move_up(self, path: Deque[np.ndarray], moves: Deque[int], gap: int, f_bound: int) -> bool:
        if (gap // self.rows) > 0:
            grid: np.ndarray = np.copy(path[-1])
            grid[[gap - self.rows, gap]] = grid[[gap, gap - self.rows]]

            f = self.h(grid) + (len(path) - 1)
            if f > f_bound:
                return False

            for state in path:
                if (state == grid).all():
                    return False
            
            path.append(grid)
            moves.append(2)
            return True
            
        return False



    # Move code 3
    def move_down(self, path: Deque[np.ndarray], moves: Deque[int], gap: int, f_bound: int) -> bool:
        if (gap // self.rows) < (self.rows - 1):
            grid: np.ndarray = np.copy(path[-1])
            #grid = deepcopy(path[-1])
            grid[[gap + self.rows, gap]] = grid[[gap, gap + self.rows]]

            f = self.h(grid) + (len(path) - 1)
            if f > f_bound:
                return False

            for state in path:
                if (state == grid).all():
                    return False

            path.append(grid)
            moves.append(3)
            return True
            
        return False
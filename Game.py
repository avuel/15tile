import pygame
import pygame.freetype
import buttons as b
from collections import deque
from Grid import Grid
from Button import Button
from Tile import Tile
from typing import Deque, List
from copy import deepcopy

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
        self.solved: bool = False
        self.time: int = 0
        self.mins: int = 0
        self.clicks: int = 0

        self.moves: Deque[int] = deque([])



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
        
        if len(self.moves) > 0:
            self.grid.fill_solution(self.moves[0])

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

                            for button in self.buttons:
                                if button.get_name() == b.sol_name:
                                    button.set_color(b.sol_off_clr)
                                    break
                                
                            self.moves = []

                    # Otherwise, if we are out of the grid and we click on restart, restart (even if solved)
                    else:
                        if (y >= b.rest_x) and (y <= (b.rest_x + b.rest_wdth)):
                            if (x >= b.rest_y) and (x <= (b.rest_y + b.rest_hght)):
                                self.grid.make_grid()
                                self.solved: bool = self.grid.is_solved()
                                self.time: int = 0
                                self.mins: int = 0
                                self.clicks: int = 0

                            elif self.solved:
                                continue

                            elif (x >= b.sol_y) and (x <= (b.sol_y + b.sol_hght)):
                                
                                self.moves: Deque[int] = self.solve_grid()
                                if len(self.moves) > 0:
                                    self.moves.popleft()
                                    for button in self.buttons:
                                        if button.get_name() == b.sol_name:
                                            button.set_color(b.sol_on_clr)
                                            break
                                
                                print(self.moves)
                    

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

            



    def convert_grid(self) -> List[int]:
        grid: List[int] = list(range(0, (self.rows * self.rows)))
        tiles: List[Tile] = self.grid.get_grid()
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                #num = grid[j][i].get_num()
                #print(num)
                grid[self.rows*i + j] = tiles[j][i].get_num()

        return grid


    
    def solve_grid(self) -> Deque[int]:
        start_grid: List[int] = self.convert_grid()
        f_bound: int = 15
        MAX_BOUND: int = 100
        
        while(f_bound <= MAX_BOUND):
            path: Deque[List[int]] = deque([])
            moves: Deque[int] = deque([])
            path.append(start_grid)
            moves.append(-1)
            explored: List[List[int]] = []
            gap: int = self.grid.get_gap()
            if self.explore(path, explored, moves, gap, f_bound):
                if self.h(path[-1]) == 0:
                    break

            f_bound: int = f_bound + 1

        if f_bound > MAX_BOUND:
            return []
            #print("didnt find")
        
        elif self.h(path[-1]) == 0:
            return moves
            '''
            print("total of " + str(len(path) - 1) + " moves")
            print("visited a total of " + str(len(explored)) + " nodes")
            count: int = 0
            for move in moves:
                if move == -1:
                    print("start:")
                else:
                    print(str(count) + ":", end =' ')
                    if move == 0:
                        print("left")
                    elif move == 1:
                        print("right")
                    elif move == 2:
                        print("up")
                    elif move == 3:
                        print("down")
                count: int = count + 1

            print()
            '''
        
        else:
            return []
            #print("didnt find")


    def h(self, grid: List[int]) -> int:
        sum: int = 0
        for i in range(len(grid)):
            row: int = i // self.rows
            col: int = i % self.rows
            end_row: int = (grid[i] - 1) // self.rows
            end_col: int = (grid[i] - 1) % self.rows
            sum: int = sum + abs(row - end_row) + abs(col - end_col)

        return sum


    def explore(self, path: Deque[List[int]], explored: List[List[int]], moves: Deque[int], gap: int, f_bound: int) -> bool:
        if (self.h(path[-1]) == 0):
            return True

        # If we moved right last (1), dont try to move left
        if moves[-1] !=  1:
            if self.move_left(path, explored, moves, gap, f_bound):
                self.explore(path, explored, moves, gap - 1, f_bound)

        # If we moved down last (3), dont try to move up
        if (moves[-1] != 3):
            if self.move_up(path, explored, moves, gap, f_bound):
                self.explore(path, explored, moves, gap - self.rows, f_bound)

        # If we moved left last (0)
        if moves[-1] != 0:
            if self.move_right(path, explored, moves, gap, f_bound):
                self.explore(path, explored, moves, gap + 1, f_bound)

        # If we moved up last (2), dont try to move down
        if moves[-1] != 2:
            if self.move_down(path, explored, moves, gap, f_bound):
                self.explore(path, explored, moves, gap + self.rows, f_bound)

        if (self.h(path[-1]) == 0):
            return True

        popped: List[int] = path.pop()
        moves.pop()
                
        explore: bool = True
        for state in explored:
            if state == popped:
                explore = False

        if explore:
            explored.append(popped)
        
        if (len(path)) == 0:
            return False

        if (len(moves)) == 0:
            return False


    # Move code 0
    def move_left(self, path: Deque[List[int]], explored: List[List[int]], moves: Deque[int], gap: int, f_bound: int) -> bool:
        if (gap % self.rows) > 0:
            grid = deepcopy(path[-1])
            grid[gap - 1], grid[gap] = grid[gap], grid[gap - 1]
            f = self.h(grid) + len(path)
            
            if f > f_bound:
                return False

            for state in path:
                if state == grid:
                    return False

            for state in explored:
                if state == grid:
                    return False

            path.append(grid)
            moves.append(0)
            return True

        return False


    # Move code 1
    def move_right(self, path: Deque[List[int]], explored: List[List[int]], moves: Deque[int], gap: int, f_bound: int) -> bool:
        if (gap % self.rows) < (self.rows - 1):
            grid = deepcopy(path[-1])
            grid[gap + 1], grid[gap] = grid[gap], grid[gap + 1]
            f = self.h(grid) + len(path)

            if f > f_bound:
                return False

            for state in path:
                if state == grid:
                    return False

            for state in explored:
                if state == grid:
                    return False
            
            path.append(grid)
            moves.append(1)
            return True
            
        return False


    # Move code 2
    def move_up(self, path: Deque[List[int]], explored: List[List[int]], moves: Deque[int], gap: int, f_bound: int) -> bool:
        if (gap // self.rows) > 0:
            grid = deepcopy(path[-1])
            grid[gap - self.rows], grid[gap] = grid[gap], grid[gap - self.rows]

            f = self.h(grid) + len(path)
            if f > f_bound:
                return False

            for state in path:
                if state == grid:
                    return False

            for state in explored:
                if state == grid:
                    return False
            
            path.append(grid)
            moves.append(2)
            return True
            
        return False


    # Move code 3
    def move_down(self, path: Deque[List[int]], explored: List[List[int]], moves: Deque[int], gap: int, f_bound: int) -> bool:
        if (gap // self.rows) < (self.rows - 1):
            grid = deepcopy(path[-1])
            grid[gap + self.rows], grid[gap] = grid[gap], grid[gap + self.rows]

            f = self.h(grid) + len(path)
            if f > f_bound:
                return False

            for state in path:
                if state == grid:
                    return False

            for state in explored:
                if state == grid:
                    return False
        
            path.append(grid)
            moves.append(3)
            return True
            
        return False
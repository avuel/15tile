import pygame
import pygame.freetype
import my_algorithm
from Grid import Grid

def get_clicked_pos(x: int, y: int, rows: int, width: int) -> int:
    gap: int = width // rows

    # Find the row, column that the mouse click occured in
    row: int = y // gap
    col: int = x // gap

    return row, col

def main(win, width: int, clock, fps: int, rows: int):
    extra_width: int = width % 960
    grid_width: int = width - extra_width
    grid: Grid = Grid(grid_width, rows)

    run: bool = True
    solved: bool = False
    time: int = 0
    mins: int = 0
    while run:
        # Control the framerate
        clock.tick(fps)

        if not solved:
            time += clock.get_time()
            if (time // 60000) > 0:
                mins += 1
                time = time - 60000

        # Draw the grid
        grid.draw(win, grid_width, extra_width, time, mins)

        for event in pygame.event.get():
            
            # See if we want to quit
            if event.type == pygame.QUIT:
                run = False
                break
            
            if solved:
                continue

            # Check if left mouse was pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    y,x = pos

                    if (y <= grid_width):
                        row, col = get_clicked_pos(x, y, rows, grid_width)
                        if grid.move_tile(row, col):
                            grid.draw(win, grid_width, extra_width, time, mins)
                            solved: bool = grid.is_solved()
                    else:
                        restart_x: int = grid_width + extra_width // 6
                        restart_y: int = 3 * grid_width // 5
                        restart_width: int = 2 * extra_width // 3
                        restart_height: int = grid_width / 12

                        if (y >= restart_x) and (y <= (restart_x + restart_width)):
                            if (x >= restart_y) and (x <= (restart_y + restart_height)):
                                grid.make_grid()


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if grid.move_left():
                        grid.draw(win, grid_width, extra_width, time, mins)
                        solved: bool = grid.is_solved()

                elif event.key == pygame.K_RIGHT:
                    if grid.move_right():
                        grid.draw(win, grid_width, extra_width, time, mins)
                        solved: bool = grid.is_solved()

                elif event.key == pygame.K_DOWN:
                    if grid.move_down():
                        grid.draw(win, grid_width, extra_width, time, mins)
                        solved: bool = grid.is_solved()

                elif event.key == pygame.K_UP:
                    if grid.move_up():
                        grid.draw(win, grid_width, extra_width, time, mins)
                        solved: bool = grid.is_solved()
    
    pygame.quit()

if __name__ == '__main__':
    ROWS: int = 0
    while (ROWS < 3) or (ROWS > 10):
        ROWS: int = int(input("How many rows (3-10): "))
        print()

    # Width (and height since we are going to be using a square) of the screen
    GRID_WIDTH: int = 960
    EXTRA_WIDTH: int = 320
    # Set the display for the window
    WIN = pygame.display.set_mode((GRID_WIDTH + EXTRA_WIDTH, GRID_WIDTH))

    # Set the name of the window
    pygame.display.set_caption("Fortnite 2")
    pygame.freetype.init()
    
    # Set framerate of the game
    FPS: int = 60
    CLOCK = pygame.time.Clock()
    main(WIN, GRID_WIDTH + EXTRA_WIDTH, CLOCK, FPS, ROWS)
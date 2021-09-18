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
    framerates: list[float] = []
    fps_avg: int = 0
    fps_counter: pygame.freetype.Font = pygame.freetype.Font('freesansbold.ttf', 16)
    run: bool = True
    solved: bool = False

    while run:
        # Control the framerate
        clock.tick(fps)

        '''
        framerates.append(clock.get_fps())
        if len(framerates) == 10:
            fps_avg: int = 0 

            for framerate in framerates:
                fps_avg: int = fps_avg + framerate

            framerates = []
            fps_avg: int = fps_avg // 10
            fps_counter.render_to(win, (width - 32, 16), str(fps_avg), GREY)
        '''

        # Draw the grid
        grid.draw(win, grid_width, extra_width)

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
                    x,y = pos

                    if (x < grid_width):
                        row, col = get_clicked_pos(x, y, rows, grid_width)
                        if grid.move_tile(row, col):
                            grid.draw(win, grid_width, extra_width)
                            solved: bool = grid.is_solved()
                    else:
                        restart_x: int = grid_width + extra_width // 6
                        restart_y: int = 3 * grid_width // 5
                        restart_width: int = 2 * extra_width // 3
                        restart_height: int = grid_width / 12
                        if (x >= restart_x) and (x <= (restart_x + restart_width)):
                            if (y >= restart_y) and (y <= (restart_y + restart_height)):
                                grid.make_grid()


            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if grid.move_left():
                        grid.draw(win, grid_width, extra_width)
                        solved: bool = grid.is_solved()

                elif event.key == pygame.K_RIGHT:
                    if grid.move_right():
                        grid.draw(win, grid_width, extra_width)
                        solved: bool = grid.is_solved()

                elif event.key == pygame.K_DOWN:
                    if grid.move_down():
                        grid.draw(win, grid_width, extra_width)
                        solved: bool = grid.is_solved()

                elif event.key == pygame.K_UP:
                    if grid.move_up():
                        grid.draw(win, grid_width, extra_width)
                        solved: bool = grid.is_solved()
    
    pygame.quit()

if __name__ == '__main__':
    ROWS: int = 0
    while (not (3 <= ROWS <= 10)):
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
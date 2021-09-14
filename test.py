import pygame
import pygame.freetype
import my_algorithm
from colors import GREY
from Grid import Grid

def get_clicked_pos(pos, rows: int, width: int) -> int:
    gap: int = width // rows

    # Get position of the mouse click
    y, x = pos

    # Find the row, column that the mouse click occured in
    row: int = y // gap
    col: int = x // gap

    return row, col

def main(win, width, clock, fps, rows):
    grid: Grid = Grid(width, rows)
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
        grid.draw(win)

        for event in pygame.event.get():
            
            # See if we want to quit
            if event.type == pygame.QUIT:
                run = False
                break
            
            # Check if left mouse was pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                if grid.move_tile(row, col):
                    grid.draw(win)

        
    pygame.quit()

if __name__ == '__main__':
    ROWS = 3
    # Width (and height since we are going to be using a square) of the screen
    WIDTH: int = 960

    # Set the display for the window
    WIN = pygame.display.set_mode((WIDTH, WIDTH))

    # Set the name of the window
    pygame.display.set_caption("Fortnite 2")
    pygame.freetype.init()
    # Set framerate of the game
    FPS: int = 60
    CLOCK = pygame.time.Clock()
    main(WIN, WIDTH, CLOCK, FPS, ROWS)
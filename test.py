import pygame
import pygame.freetype
import colors
from Game import Game
from typing import Tuple


def main() -> None:
    # Rows of the game
    rows: int = 0

    # Get the rows from the user
    while (rows < 3) or (rows > 10):
        rows: int = int(input("How many rows (3-10): "))

    # 1280x960 window, use (0,0) to (960,960) for grid, (960,0) to (1280,960) as the side bar for restart button/timer/click counter/fps counter
    grid_width: int = 960
    extra_width: int = 320

    # Set the display for the window
    win = pygame.display.set_mode((grid_width + extra_width, grid_width))

    # Set the name of the window
    pygame.display.set_caption("Fortnite 2")
    pygame.freetype.init()

    # Set framerate of the game
    fps: int = 60
    clock = pygame.time.Clock()

    # Constants we are going to use for the restart button
    restart_name: str = "Restart Button"
    restart_x: int = grid_width + extra_width // 6
    restart_y: int = 3 * grid_width // 5
    restart_width: int = 2 * extra_width // 3
    restart_height: int = grid_width / 12
    restart_button_color: Tuple(int, int, int) = colors.WHITE
    restart_text: str = "restart"
    restart_text_x: int = restart_x + restart_width / 6
    restart_text_y: int = restart_y + (7 * restart_height / 20)
    restart_text_color: Tuple(int, int, int) = colors.BLACK
    restart_border_color: Tuple(int, int, int) = colors.BLACK

    # Constants we are going to use for the timer
    timer_name: str = "Timer"
    timer_x: int = restart_x
    timer_y: int = grid_width // 5
    timer_width: int = restart_width
    timer_height: int = restart_height
    timer_button_color: Tuple(int, int, int) = colors.WHITE
    timer_text: str = None
    timer_text_x: int = timer_x + (32 * timer_width / 100)
    timer_text_y: int = timer_y + (7 * timer_height / 20)
    timer_text_color: Tuple(int, int, int) = colors.BLACK
    timer_border_color: Tuple(int, int, int) = colors.BLACK

    # Constants we are going to use for the click counter
    clicks_name: str = "Clicks Counter"
    clicks_x: int = restart_x
    clicks_y: int = (timer_y + restart_y) // 2
    clicks_width: int = restart_width
    clicks_height: int = restart_height
    clicks_button_color: Tuple(int, int, int) = colors.WHITE
    clicks_text: str = None
    clicks_text_x: int = clicks_x + (64 * clicks_width / 100)
    clicks_text_y: int = clicks_y + (7 * clicks_height / 20)
    clicks_text_color: Tuple(int, int, int) = colors.BLACK
    clicks_border_color: Tuple(int, int, int) = colors.BLACK
    

    # Constants we are going to use for the fps counter
    fps_name: str = "Fps Counter"
    fps_x: int = None
    fps_y: int = None
    fps_width: int = None
    fps_height: int = None
    fps_button_color: Tuple(int, int, int) = None
    fps_text: str = None
    fps_text_x: int = grid_width + extra_width - 39
    fps_text_y: int = 4
    fps_text_color: Tuple(int, int, int) = colors.BLACK
    fps_border_color: Tuple(int, int, int) = None

    game: Game = Game(grid_width, extra_width, clock, fps, rows)
    game.add_button(restart_name, restart_x, restart_y, restart_width, restart_height, restart_button_color, restart_text, restart_text_x, restart_text_y, restart_text_color, restart_border_color)
    game.add_button(timer_name, timer_x, timer_y, timer_width, timer_height, timer_button_color, timer_text, timer_text_x, timer_text_y, timer_text_color, timer_border_color)
    game.add_button(fps_name, fps_x, fps_y, fps_width, fps_height, fps_button_color, fps_text, fps_text_x, fps_text_y, fps_text_color, fps_border_color)
    game.add_button(clicks_name, clicks_x, clicks_y, clicks_width, clicks_height, clicks_button_color, clicks_text, clicks_text_x, clicks_text_y, clicks_text_color, clicks_border_color)

    # Update the game while the game is running
    while (game.is_running()):
        game.update(win)

    # Quit once the game is no longer running
    pygame.quit()
    

if __name__ == '__main__':
    main()
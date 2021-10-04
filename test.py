import pygame
import pygame.freetype
import buttons as b
from Game import Game


def main() -> None:
    # Rows of the game
    rows: int = 0

    # Get the rows from the user
    while (rows < 2) or (rows > 10):
        rows: int = int(input("How many rows (2-10): "))

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

    game: Game = Game(grid_width, extra_width, clock, fps, rows)
    game.add_button(b.rest_name, b.rest_x, b.rest_y, b.rest_wdth, b.rest_hght, b.rest_btn_clr, b.rest_txt, b.rest_txt_x, b.rest_txt_y, b.rest_txt_clr, b.rest_border_clr)
    game.add_button(b.timer_name, b.timer_x, b.timer_y, b.timer_wdth, b.timer_hght, b.timer_btn_clr, b.timer_txt, b.timer_txt_x, b.timer_txt_y, b.timer_txt_clr, b.timer_border_clr)
    game.add_button(b.fps_name, b.fps_x, b.fps_y, b.fps_wdth, b.fps_hght, b.fps_btn_clr, b.fps_txt, b.fps_txt_x, b.fps_txt_y, b.fps_txt_clr, b.fps_border_clr)
    game.add_button(b.clks_name, b.clks_x, b.clks_y, b.clks_wdth, b.clks_hght, b.clks_btn_clr, b.clks_txt, b.clks_txt_x, b.clks_txt_y, b.clks_txt_clr, b.clks_border_clr)
    game.add_button(b.sol_name, b.sol_x, b.sol_y, b.sol_wdth, b.sol_hght, b.sol_btn_clr, b.sol_txt, b.sol_txt_x, b.sol_txt_y, b.sol_txt_clr, b.sol_border_clr)
    
    # Update the game while the game is running
    while (game.is_running()):
        game.update(win)

    # Quit once the game is no longer running
    pygame.quit()
    

if __name__ == '__main__':
    main()
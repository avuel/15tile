import colors

# Constants we are going to use for the restart button
grid_width: int = 960
extra_width: int = 320

rest_name: str = "Restart"
rest_x: int = grid_width + extra_width // 6
rest_y: int = 3 * grid_width // 5
rest_wdth: int = 2 * extra_width // 3
rest_hght: int = grid_width / 12
rest_btn_clr: colors.Color = colors.WHITE
rest_txt: str = "restart"
rest_txt_x: int = rest_x + rest_wdth / 6
rest_txt_y: int = rest_y + (7 * rest_hght / 20)
rest_txt_clr: colors.Color = colors.BLACK
rest_border_clr: colors.Color = colors.BLACK

# Constants we are going to use for the timer
timer_name: str = "Timer"
timer_x: int = rest_x
timer_y: int = grid_width // 5
timer_wdth: int = rest_wdth
timer_hght: int = rest_hght
timer_btn_clr: colors.Color = colors.WHITE
timer_txt: str = None
timer_txt_x: int = timer_x + (32 * timer_wdth / 100)
timer_txt_y: int = timer_y + (7 * timer_hght / 20)
timer_txt_clr: colors.Color = colors.BLACK
timer_border_clr: colors.Color = colors.BLACK

# Constants we are going to use for the click counter
clks_name: str = "Clicks Counter"
clks_x: int = rest_x
clks_y: int = (timer_y + rest_y) // 2
clks_wdth: int = rest_wdth
clks_hght: int = rest_hght
clks_btn_clr: colors.Color = colors.WHITE
clks_txt: str = None
clks_txt_x: int = clks_x + (64 * clks_wdth / 100)
clks_txt_y: int = clks_y + (7 * clks_hght / 20)
clks_txt_clr: colors.Color = colors.BLACK
clks_border_clr: colors.Color = colors.BLACK

# Constants we are going to use for the fps counter
fps_name: str = "Fps Counter"
fps_x: int = None
fps_y: int = None
fps_wdth: int = None
fps_hght: int = None
fps_btn_clr: colors.Color = None
fps_txt: str = None
fps_txt_x: int = grid_width + extra_width - 40
fps_txt_y: int = 4
fps_txt_clr: colors.Color = colors.BLACK
fps_border_clr: colors.Color = None

# Constants we are going to use for the fps counter
sol_name: str = "Solver"
sol_x: int = grid_width + extra_width // 6
sol_y: int = 7 * grid_width // 8
sol_wdth: int = 2 * extra_width // 3
sol_hght: int = grid_width / 12
sol_btn_clr: colors.Color = colors.WHITE
sol_txt: str = "solve"
sol_txt_x: int = sol_x + sol_wdth / 4
sol_txt_y: int = sol_y + (7 * sol_hght / 20)
sol_txt_clr: colors.Color = colors.BLACK
sol_border_clr: colors.Color = colors.BLACK
from typing import NewType

Color = NewType('Color', (int, int, int))
# Colors
WHITE: Color = (255, 255, 255)
BLACK: Color = (0, 0, 0)
RED: Color = (255, 0, 0)
GREEN: Color = (0, 255, 0)
BLUE: Color = (0, 0, 255)
PURPLE: Color = (255, 0, 255)
YELLOW: Color = (255, 255, 0)
ORANGE: Color = (255, 255//2, 0)
CYAN: Color = (0, 255, 255)
GRAY: Color = (255 // 2, 255 // 2, 255 // 2)
DARKGRAY: Color = (50, 50, 50)
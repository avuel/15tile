import pygame
import pygame.freetype
import colors


class Tile:
    def __init__(self, row: int, col: int, width: int, num: int, rows: int) -> None:
        self.row: int = row
        self.col: int  = col
        self.width: int = width
        self.x: int = self.row * self.width
        self.y: int = self.col * self.width
        self.rows: int = rows
        self.color: colors.Color = colors.WHITE
        self.num: int = num
        self.gap_color: colors.Color = colors.DARKGRAY
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.width)
        self.img: pygame.freetype.Font = pygame.freetype.Font('cour.ttf', 48)
        if (self.num == (self.rows*self.rows)):
            self.color: colors.Color = self.gap_color

    def set_pos(self, row, col) -> None:
        self.row: int = row
        self.col: int  = col
        self.x: int = row * self.width
        self.y: int = col * self.width

    def get_pos(self) -> int: 
        return self.row, self.col

    def get_color(self) -> colors.Color:
        return self.color

    def get_num(self) -> int:
        return self.num

    def pos_diff(self, rows) -> int:
        true_row: int = (self.num // rows)
        true_col: int = (self.num - 1) % rows
        return (true_row - self.row) + (true_col - self.col)
    
    def draw(self, win) -> None:
        if (self.num == (self.rows * self.rows)):
            pygame.draw.rect(win, self.color, self.rect)

        else:
            x: int = self.x + (self.width / 2)
            y: int = self.y + (self.width / 2)
            if (self.num > 9):
                x: int = x - 12
            self.img.render_to(win, (x-8, y-16), str(self.num), colors.BLACK)

    def set_tile(self, color, num) -> None:
        self.color: colors.Color = color
        self.num: int = num
        if (self.num == (self.rows*self.rows)):
            self.color: colors.Color = self.gap_color

    def swap(self, tile) -> None:
        new_color: colors.Color = tile.get_color()
        new_num: int = tile.get_num()
        tile.set_tile(self.color, self.num)
        self.set_tile(new_color, new_num)


    def move(self, gap_tile) -> bool:
        gap_row: int = gap_tile.get_pos()[0]
        gap_col: int = gap_tile.get_pos()[1]
        if (self.color == self.gap_color):
            return False

        elif (self.row == gap_row):
            if abs(gap_col - self.col) == 1:
                self.swap(gap_tile)
                return True
            
            else:
                return False

        elif (self.col == gap_col):
            if (abs(gap_row - self.row)) == 1:
                self.swap(gap_tile)
                return True
            
            else:
                return False
        
        else:
            return False


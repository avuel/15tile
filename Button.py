import pygame
import pygame.freetype
from typing import Tuple

class Button:
    def __init__(self, name: str, x: int, y: int, width: int, height: int, button_color, text: str, text_x: int, text_y: int, text_color, border_color) -> None:
        self.name = name
        self.x: int = x
        self.y: int = y
        self.button_color: Tuple(int, int, int) = button_color
        self.text: str = text
        self.text_x: int = text_x
        self.text_y: int = text_y
        self.text_color: Tuple(int, int, int) = text_color
        self.width: int = width
        self.height: int = height
        self.border_color: Tuple(int, int, int) = border_color
        self.img: pygame.freetype.Font = pygame.freetype.Font('cour.ttf', 36)



    def get_x(self) -> int:
        return self.x



    def get_width(self) -> int:
        return self.width



    def get_name(self) -> str:
        return self.name
        


    def set_text_x(self, text_x: int) -> None:
        self.text_x: int = text_x



    def set_text(self, text: str) -> None:
        self.text: str = text



    def draw_button(self, win) -> None:
        pygame.draw.rect(win, self.button_color, (self.x, self.y, self.width, self.height))



    def draw_text(self, win)-> None:
        self.img.render_to(win, (self.text_x, self.text_y), self.text, self.text_color)



    def draw_border(self, win) -> None:
        pygame.draw.line(win, self.border_color, (self.x, self.y), (self.x + self.width, self.y))
        pygame.draw.line(win, self.border_color, (self.x, self.y), (self.x, self.y + self.height))
        pygame.draw.line(win, self.border_color, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height))
        pygame.draw.line(win, self.border_color, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height))



    def draw(self, win):
        self.draw_button(win)
        self.draw_text(win)
        self.draw_border(win)
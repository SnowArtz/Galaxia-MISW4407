import pygame

class CText:
    def __init__(self, font:pygame.font, text:str, color:pygame.Color, position:pygame.Vector2) -> None:
        self.font = font
        self.text = text
        self.color = color
        self.position = position
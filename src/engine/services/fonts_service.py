import pygame

class FontsService:
    def __init__(self) -> None:
        self._fonts = {}

    def get(self, path:str, font_size:int) -> pygame.font.Font:
        if path+str(font_size) not in self._fonts:
            self._fonts[path+str(font_size)] = pygame.font.Font(path, font_size)
        return self._fonts[path+str(font_size)]
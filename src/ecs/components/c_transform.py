import pygame

class CTransform:
    def __init__(self, position:pygame.Vector2) -> None:
        self.initial_position = position.copy()
        self.position = position
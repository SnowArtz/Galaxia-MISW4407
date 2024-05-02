import pygame

class CSurface:
    def __init__(self, size:pygame.Vector2, color:pygame.Color) -> None:
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.area = self.surface.get_rect()
        pass
    
    @classmethod
    def from_surface(cls, surface:pygame.Surface) -> None:
        c_surface = cls(pygame.Vector2(0,0), pygame.Color(0,0,0))
        c_surface.surface = surface
        c_surface.area = surface.get_rect()
        return c_surface
    
    def get_relative_area(area:pygame.Rect, pos_topleft:pygame.Vector2) -> pygame.Rect:
        new_rectangle = area.copy()
        new_rectangle.topleft = pos_topleft.copy()
        return new_rectangle
import pygame

from src.engine.service_locator import ServiceLocator
class CStaticImage:
    def __init__(self, type:str, start_position:pygame.Vector2) -> None:
        self.image = None
        if type == "life":
            self.image = ServiceLocator.images_service.get("assets/img/invaders_life.png")
        elif type == "level_flag":
            self.image = ServiceLocator.images_service.get("assets/img/invaders_level_flag.png")
        self.start_position = start_position
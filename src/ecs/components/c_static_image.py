import pygame

from src.engine.service_locator import ServiceLocator
class CStaticImage:
    def __init__(self, type:str, start_position:pygame.Vector2) -> None:
        self.image = None
        if type == "life":
            self.image = ServiceLocator.images_service.get("assets/img/invaders_life.png")
        elif type == "level_flag":
            self.image = ServiceLocator.images_service.get("assets/img/invaders_level_flag.png")
        elif type == "logo_title":
            self.image = ServiceLocator.images_service.get("assets/img/invaders_logo_title.png")
        elif type == "selector":
            self.image = ServiceLocator.images_service.get("assets/img/invaders_selector.png")
        self.start_position = start_position
        self.already_in_final_position = False
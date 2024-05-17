import esper
import pygame

from src.create.prefab_creator import create_text
from src.ecs.components.c_static_image import CStaticImage
from src.ecs.components.c_text import CText
from src.ecs.components.tags.c_tag_flag import CTagFlag


def system_render_flags(world: esper.World, screen: pygame.Surface, level_flags: int, config_interface: dict):
    for ent, (image, flag) in world.get_components(CStaticImage, CTagFlag):
        if level_flags < 6:
            for i in range(level_flags):
                position_x = image.start_position[0] + i * (image.image.get_width() - 3)
                position_y = image.start_position[1]
                screen.blit(image.image, (position_x, position_y))
        else:
            position_x = image.start_position[0]
            position_y = image.start_position[1]
            screen.blit(image.image, (position_x, position_y))
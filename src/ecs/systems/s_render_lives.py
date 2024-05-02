import esper
import pygame

from src.ecs.components.c_static_image import CStaticImage
from src.ecs.components.tags.c_tag_life import CTagLife

def system_render_lives(world:esper.World, screen: pygame.Surface, player_lives:int):
    for ent, (image, life) in world.get_components(CStaticImage, CTagLife):
        for i in range(player_lives):
            position_x = image.start_position[0] + i * (image.image.get_width())
            position_y = image.start_position[1]
            screen.blit(image.image, (position_x, position_y))

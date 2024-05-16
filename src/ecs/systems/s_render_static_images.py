import esper
import pygame

from src.ecs.components.c_static_image import CStaticImage
from src.ecs.components.c_transform import CTransform


def system_render_static_images(world:esper.World, screen: pygame.Surface):
    for ent, (image, transform) in world.get_components(CStaticImage, CTransform):
        screen.blit(image.image,  pygame.Vector2(transform.position))

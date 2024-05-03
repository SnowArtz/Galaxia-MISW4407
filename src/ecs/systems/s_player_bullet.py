
import math
import esper
import pygame

from src.create.prefab_creator import create_bullet
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_player_bullet(world:esper.World, position: pygame.Vector2, bullet_information:dict):
    components = world.get_components(CTransform, CTagBullet)
    for bullet_entity, (bullet_position, bullet_tag) in components:
        if bullet_tag.active == False:
            bullet_position.position = pygame.Vector2(position.x-bullet_information["width"]/2, position.y-bullet_information["height"]/2-1)
    if len(world.get_components(CTagBullet)) == 0:
        bullet_entity = create_bullet(world, position, bullet_information)
    return bullet_entity
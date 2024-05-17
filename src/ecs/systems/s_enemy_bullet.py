import math
import random
import esper
import pygame

from src.create.prefab_creator import create_bullet, create_enemy_bullet
from src.ecs.components.c_cooldown import CCooldown
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemy_bullet(world:esper.World, bullet_information:dict, entity):
    global_cooldown = world.component_for_entity(entity, CCooldown)
    if global_cooldown.current_time  > 0.1 :
        return
    components = world.get_components(CTransform, CSurface, CTagEnemy)
    for enemy_entity, (enemy_transform, enemy_surface, enemy) in components:
        if random.random() < 0.0008:
            enemy_rect = enemy_surface.surface.get_rect(topleft = enemy_transform.position)
            bullet_size_x = bullet_information["width"]
            bullet_size_y = bullet_information["height"]
            bullet_position = pygame.Vector2(enemy_rect.x + enemy_surface.area.size[0]/2-(bullet_size_x/2),
                                               enemy_rect.y + enemy_surface.area.size[1]/2-(bullet_size_y/2))
            create_enemy_bullet(world, bullet_position, bullet_information)
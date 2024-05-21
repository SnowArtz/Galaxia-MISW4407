import math
import random
import esper
import pygame

from src.create.prefab_creator import create_bullet, create_enemy_bullet
from src.ecs.components.c_cooldown import CCooldown
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemy_bullet(world:esper.World, bullet_information:dict, bullet_cooldown_entity):
    global_cooldown = world.component_for_entity(bullet_cooldown_entity, CCooldown)
    if global_cooldown.current_time  > 0.1:
        return
    components = world.get_components(CTransform, CSurface, CTagEnemy, CEnemyState)
    for enemy_entity, (enemy_transform, enemy_surface, enemy_tag, enemy_state) in components:
        if random.random() < 0.0008:
            enemy_rect = enemy_surface.surface.get_rect(topleft = enemy_transform.position)
            bullet_size_x = bullet_information["width"]
            bullet_size_y = bullet_information["height"]
            bullet_position = pygame.Vector2(enemy_rect.x + enemy_surface.area.size[0]/2-(bullet_size_x/2),
                                               enemy_rect.y + enemy_surface.area.size[1]/2-(bullet_size_y/2))
            create_enemy_bullet(world, bullet_position, bullet_information)
        if enemy_state.state == EnemyState.EMERGING:
            world.add_component(enemy_entity, CCooldown(0.4))
        if enemy_state.state == EnemyState.ATTACKING:
            if enemy_state.shoots == 0:
                attack_cooldown = world.component_for_entity(enemy_entity, CCooldown)
                attack_position = world.component_for_entity(enemy_entity, CTransform)
                attack_surface = world.component_for_entity(enemy_entity, CSurface)
                attack_enemy_rect = enemy_surface.surface.get_rect(topleft = attack_position.position)
                bullet_size_x = bullet_information["width"]
                bullet_size_y = bullet_information["height"]
                bullet_position = pygame.Vector2(attack_enemy_rect.x + attack_surface.area.size[0]/2-(bullet_size_x/2),
                                                attack_enemy_rect.y + attack_surface.area.size[1]/2-(bullet_size_y/2))
                if attack_cooldown.current_time > 0.1 :
                    return
                create_enemy_bullet(world, bullet_position, bullet_information)
                enemy_state.shoots = 1
                world.add_component(enemy_entity, CCooldown(0.7))
            if enemy_state.shoots == 1:
                attack_cooldown = world.component_for_entity(enemy_entity, CCooldown)
                attack_position = world.component_for_entity(enemy_entity, CTransform)
                attack_surface = world.component_for_entity(enemy_entity, CSurface)
                attack_enemy_rect = enemy_surface.surface.get_rect(topleft = attack_position.position)
                bullet_size_x = bullet_information["width"]
                bullet_size_y = bullet_information["height"]
                bullet_position = pygame.Vector2(attack_enemy_rect.x + attack_surface.area.size[0]/2-(bullet_size_x/2),
                                                attack_enemy_rect.y + attack_surface.area.size[1]/2-(bullet_size_y/2))
                if attack_cooldown.current_time > 0.1 :
                    return
                create_enemy_bullet(world, bullet_position, bullet_information)
                enemy_state.shoots = 2
            
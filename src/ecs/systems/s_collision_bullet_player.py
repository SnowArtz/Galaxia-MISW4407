import pygame
import esper
from src.create.prefab_creator import create_player, create_player_explosion_sprite
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_player_dead import system_player_dead


def system_collision_bullet_player(world:esper.World, player_explosion_file: dict, config_level:dict):
    componentsP = world.get_components(CSurface, CTransform, CTagPlayer)
    componentsB = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    for enemy_bullet_entity, (enemy_bullet_s, enemy_bullet_t, _) in componentsB:
        bullet_rect = enemy_bullet_s.area.copy()
        bullet_rect.topleft = enemy_bullet_t.position
        for player_entity, (player_s, player_t, _) in componentsP:
            player_rect = CSurface.get_relative_area(player_s.area, player_t.position)
            player_rect.topleft = player_t.position
            if player_rect.colliderect(bullet_rect):
                world.delete_entity(enemy_bullet_entity)
                system_player_dead(world, player_explosion_file, config_level, player_entity)
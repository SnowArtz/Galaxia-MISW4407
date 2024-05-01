import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator import create_player_explosion_sprite

def system_collision_player_enemy(world:esper.World, player_entity:int, config_level:dict, player_explosion_file:dict):
    componentsE = world.get_components(CSurface, CTransform, CTagEnemy)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    size = pl_s.surface.get_size()
    pos = pygame.Vector2(config_level["player_spawn"]["position"]["x"]  - (size[0] / 2),
                         config_level["player_spawn"]["position"]["y"]  - (size[1] / 2))
    pl_rect = CSurface.get_relative_area(pl_s.area, pl_t.position)
    pl_rect.topleft = pl_t.position
    for enemy_entity, (c_s, c_t, _) in componentsE:
        ene_rect = CSurface.get_relative_area(c_s.area, c_t.position)
        if ene_rect.colliderect(pl_rect):
            world.delete_entity(enemy_entity)
            pl_t.position.x = pos.x
            pl_t.position.y = pos.y
            create_player_explosion_sprite(world, player_entity, player_explosion_file)


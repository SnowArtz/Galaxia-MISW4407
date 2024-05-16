
import time
import pygame
import esper
from src.create.prefab_creator import create_player_explosion_sprite
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator

def system_player_dead(world:esper.World, player_explosion_file: dict, config_level: dict, player_entity: int):
    create_player_explosion_sprite(world, player_entity, player_explosion_file)
    cont = 0
    for i in range(1000):
        cont+=1
    components = world.get_components(CSurface, CTransform, CVelocity, CTagPlayer)
    for player_entity, (player_s, player_t, player_v, player_tag) in components:
        player_t.position = pygame.Vector2(config_level['player_spawn']["position"]["x"]-player_s.surface.get_width()/2, config_level['player_spawn']["position"]["y"]-player_s.surface.get_height()/2)    



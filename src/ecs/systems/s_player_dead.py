import time
import pygame
import esper
from src.create.prefab_creator import create_player_explosion_sprite
from src.ecs.components.c_cooldown import CCooldown
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator

def system_player_dead(world:esper.World, player_explosion_file: dict, config_level: dict, player_entity: int):
    create_player_explosion_sprite(world, player_entity, player_explosion_file)
    components = world.get_components(CSurface, CTransform, CTagPlayer, CCooldown)
    componentsB = world.get_components(CTransform, CTagBullet, CCooldown)

    for player_entity, (player_s, player_t, player_tag, player_cooldown) in components:
        if player_cooldown.current_time > 0.1 :
            return
        player_tag.visible = True
        player_t.position = pygame.Vector2(config_level['player_spawn']["position"]["x"]-player_s.surface.get_width()/2, config_level['player_spawn']["position"]["y"]-player_s.surface.get_height()/2)  
    for bullet_entity, (bullet_t, bullet_tag, bullet_cooldown) in componentsB:
        if player_cooldown.current_time > 0.1 :
            return
        bullet_tag.visible = True
        bullet_t.position = pygame.Vector2(player_t.position.x + player_s.area.width/2, player_t.position.y)

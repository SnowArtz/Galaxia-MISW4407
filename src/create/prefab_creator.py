import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator

def create_sprite(world: esper.World, position: pygame.Vector2, velocity: pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    world.add_component(sprite_entity, CTransform(position=position))
    world.add_component(sprite_entity, CVelocity(velocity=velocity))
    return sprite_entity

def create_player(world: esper.World, position: pygame.Vector2, player_information:dict) -> int:
    player_surface = ServiceLocator.images_service.get(player_information["image"])
    velocity = pygame.Vector2(0, 0)
    position = pygame.Vector2(position.x-player_surface.get_width()/2, position.y-player_surface.get_height()/2)    
    player_entity = create_sprite(world, position, velocity, player_surface)
    world.add_component(player_entity, CTagPlayer())
    return player_entity

def create_bullet(world:esper.World, player_entity:int, bullet_info:dict) -> int:
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_rect = pl_s.surface.get_rect(topleft = pl_t.position)
    size = pygame.Vector2(bullet_info["width"], bullet_info["height"])
    bullet_surface = pygame.Surface(size)
    color = pygame.Color(bullet_info["color"]["r"],bullet_info["color"]["g"],bullet_info["color"]["b"])
    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(pl_rect.x + pl_s.area.size[0] /2 - (bullet_size[0] / 2)-1,
                         pl_rect.y - (bullet_size[1] / 2)-1)
    vel = pygame.Vector2(0, 0)
    bullet_entity = world.create_entity()
    world.add_component(bullet_entity, CSurface(size,color))
    world.add_component(bullet_entity, CTransform(pos))
    world.add_component(bullet_entity, CVelocity(vel))
    world.add_component(bullet_entity, CTagBullet(False))
    return bullet_entity


def create_enemy_explosion_sprite(world:esper.World, enemy_entity:int, enemy_explosion_file:dict):
    explosion_sprite = ServiceLocator.images_service.get(enemy_explosion_file["image"])
    pos = world.component_for_entity(enemy_entity, CTransform)
    vel = pygame.Vector2(0,0)
    explosion_entity = create_sprite(world, pos.position, vel, explosion_sprite)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity, CAnimation(enemy_explosion_file["animations"]))
    ServiceLocator.sounds_service.play(enemy_explosion_file["sound"])
    return explosion_entity

def create_player_explosion_sprite(world:esper.World, enemy_entity:int, player_explosion_file:dict):
    explosion_sprite = ServiceLocator.images_service.get(player_explosion_file["image"])
    pos = world.component_for_entity(enemy_entity, CTransform)
    vel = pygame.Vector2(0,0)
    explosion_entity = create_sprite(world, pos.position, vel, explosion_sprite)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity, CAnimation(player_explosion_file["animations"]))
    ServiceLocator.sounds_service.play(player_explosion_file["sound"])
    return explosion_entity


def create_input_player(world: esper.World) -> None:
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_fire = world.create_entity()

    world.add_component(input_left, CInputCommand(name="PLAYER_LEFT", key=pygame.K_LEFT))
    world.add_component(input_right, CInputCommand(name="PLAYER_RIGHT", key=pygame.K_RIGHT))
    world.add_component(input_fire, CInputCommand(name="PLAYER_FIRE", key=pygame.K_z))
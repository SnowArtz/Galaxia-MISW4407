import esper
import pygame
import random

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_star import CStar
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
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

def create_input_player(world: esper.World) -> None:
    input_left = world.create_entity()
    input_right = world.create_entity()

    world.add_component(input_left, CInputCommand(name="PLAYER_LEFT", key=pygame.K_LEFT))
    world.add_component(input_right, CInputCommand(name="PLAYER_RIGHT", key=pygame.K_RIGHT))

def create_stars(world:esper.World, config_starfield:dict, config_window:dict):
    for _ in range(config_starfield["number_of_stars"]):
        x = random.randint(0, config_window["size"]["w"])
        y = random.randint(0, config_window["size"]["h"])
        color = random.choice(config_starfield["star_colors"])
        vertical_speed = random.randint(config_starfield["vertical_speed"]["min"], config_starfield["vertical_speed"]["max"])
        blink_rate = random.uniform(config_starfield["blink_rate"]["min"], config_starfield["blink_rate"]["max"])

        star_color = (color["r"], color["g"], color["b"])
        star_entity = world.create_entity()
        world.add_component(star_entity, CStar((x, y), star_color, vertical_speed))
        world.add_component(star_entity, CBlink(blink_rate, pygame.time.get_ticks() + int(blink_rate * 1000)))
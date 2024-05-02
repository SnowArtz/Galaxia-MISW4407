import esper
import pygame
import random

<<<<<<< HEAD
from src.ecs.components.c_animation import CAnimation
=======
from src.ecs.components.c_blink import CBlink
>>>>>>> main
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_static_image import CStaticImage
from src.ecs.components.c_star import CStar
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_text import CText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
<<<<<<< HEAD
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
=======
from src.ecs.components.tags.c_tag_flag import CTagFlag
from src.ecs.components.tags.c_tag_life import CTagLife

>>>>>>> main
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

def create_bullet(world:esper.World, position: pygame.Vector2, bullet_information:dict) -> int:
    bullet_entity = world.create_entity()
    color = bullet_information['color']
    world.add_component(bullet_entity, CTagBullet(active=False))
    world.add_component(bullet_entity, CTransform(position=position))
    world.add_component(bullet_entity, CVelocity(velocity=pygame.Vector2(0, 0)))
    world.add_component(bullet_entity, CSurface(color=pygame.Color(color['r'], color['g'], color['b']), size=pygame.Vector2(bullet_information["width"],bullet_information["height"])))
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
<<<<<<< HEAD
    world.add_component(input_fire, CInputCommand(name="PLAYER_FIRE", key=pygame.K_z))
=======

def create_text(world:esper.World, config_text:dict, config_interface:dict) -> int:
    text_font = ServiceLocator.fonts_service.get(config_text["font"], config_text["size"])
    font_entity = world.create_entity()
    world.add_component(font_entity, CText(font=text_font, text=config_text["content"], color=pygame.Color(tuple(config_interface[config_text["color"]].values()))))
    world.add_component(font_entity, CTransform(position=pygame.Vector2(tuple(config_text["position"].values()))))
    return font_entity

def create_lives_display(world: esper.World)-> int:
    entity = world.create_entity()
    world.add_component(entity, CStaticImage("life", pygame.Vector2(168, 25)))
    world.add_component(entity, CTagLife())
    return entity

def create_level_flags(world: esper.World) -> int:
    entity = world.create_entity()
    world.add_component(entity, CStaticImage("level_flag", pygame.Vector2(200, 21)))
    world.add_component(entity, CTagFlag())
    return entity
  
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
>>>>>>> main

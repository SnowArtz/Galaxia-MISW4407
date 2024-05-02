import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_static_image import CStaticImage
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_text import CText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_flag import CTagFlag
from src.ecs.components.tags.c_tag_life import CTagLife

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

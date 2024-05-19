import esper
import pygame
from src.create.prefab_creator import create_player, create_text
from src.ecs.components.c_cooldown import CCooldown
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_timer import CTimer
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_player_xd(ecs_world:esper.World, game_engine, config_level, config_player, config_texts, config_interface):
    game_engine.active_keys.clear()
    game_engine.ready_text_entity = create_text(ecs_world, config_texts["READY"], config_interface)
    game_engine.ecs_world.add_component(game_engine.ready_text_entity, CTimer(pygame.time.get_ticks()+1000, 1500))
    game_engine._player_entity = create_player(ecs_world, pygame.Vector2(config_level['player_spawn']["position"]["x"], config_level['player_spawn']["position"]["y"]), config_player, 3)
    game_engine._player_c_velocity = ecs_world.component_for_entity(game_engine._player_entity, CVelocity)
    game_engine._player_c_transform = ecs_world.component_for_entity(game_engine._player_entity, CTransform)
    game_engine._player_c_surface = ecs_world.component_for_entity(game_engine._player_entity, CSurface)
    game_engine._player_c_cooldown = ecs_world.component_for_entity(game_engine._player_entity, CCooldown)
import math
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_cooldown import CCooldown
from src.ecs.components.c_grid_position import CGridPosition
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_state(world: esper.World, config_level: dict) -> None:
    for player_entity, (player_state, player_transform, player_surface, _) in world.get_components(CPlayerState, CTransform, CSurface, CTagPlayer):
        dead_cooldown = world.component_for_entity(player_entity, CCooldown)
        if player_state.state == PlayerState.REVIVIR:
            _do_revivir_state(player_transform, dead_cooldown, player_state, config_level, player_surface)
        elif player_state.state == PlayerState.ALIVE:
            _do_alive_state(player_transform, dead_cooldown, player_state, config_level, player_surface)
        elif player_state.state == PlayerState.DEAD:
            _do_dead_state(player_transform, dead_cooldown, player_state)



def _do_revivir_state(player_transform: CTransform, player_state: CPlayerState, config_level: dict, player_surface: CSurface):
    player_transform.position = pygame.Vector2(config_level['player_spawn']["position"]["x"]-player_surface.surface.get_width()/2, config_level['player_spawn']["position"]["y"]-player_surface.surface.get_height()/2)  
    player_state.change_state(PlayerState.ALIVE)


def _do_alive_state(player_transform, dead_cooldown: CCooldown, player_state: CPlayerState, config_level: dict, player_surface: CSurface):
    pass


def _do_dead_state(dead_cooldown: CCooldown, player_state: CPlayerState):
    if dead_cooldown.current_time > 0.1 :
        return
    pass
    player_state.change_state(PlayerState.ALIVE)


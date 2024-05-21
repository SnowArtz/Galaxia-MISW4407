import pygame
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_limit_player(world: esper.World, screen: pygame.Surface) -> None:
    screen_rect = screen.get_rect()
    player_components = world.get_components(CTransform, CSurface, CTagPlayer)

    for ent, (transform, surface, tag) in player_components:
        player_rect = pygame.Rect(transform.position.x, transform.position.y, surface.area.width, surface.area.height)

        min_x = screen_rect.left + surface.surface.get_width()/2
        max_x = screen_rect.right - surface.surface.get_width()/2

        if player_rect.left < min_x:
            transform.position.x = min_x
        elif player_rect.right > max_x:
            transform.position.x = max_x - surface.area.width

        if player_rect.top < screen_rect.top:
            transform.position.y = screen_rect.top
        elif player_rect.bottom > screen_rect.bottom:
            transform.position.y = screen_rect.bottom - surface.area.height


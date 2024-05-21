import pygame
import esper

from src.ecs.components.c_cooldown import CCooldown
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_blink import CBlink  
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_rendering(world: esper.World, screen: pygame.Surface) -> None:
    components = world.get_components(CTransform, CSurface)
    for ent, (transform, surface) in components:
        subsurface = surface.surface.subsurface(surface.area)
        if world.has_component(ent, CEnemyState):
            enemy_state = world.component_for_entity(ent, CEnemyState)
            if enemy_state.state != EnemyState.IDLE:
                rotated_image = pygame.transform.rotate(subsurface, enemy_state.sprite_angle)
                new_rect = rotated_image.get_rect(topleft=transform.position)
                screen.blit(rotated_image, new_rect)
            else:
                screen.blit(subsurface, transform.position)
        elif world.has_component(ent, CTagPlayer) or world.has_component(ent, CTagBullet):
            if world.has_component(ent, CCooldown):
                if world.component_for_entity(ent, CCooldown).current_time > 0.1:
                    continue
                screen.blit(subsurface, transform.position)
        else:
            screen.blit(subsurface, transform.position)
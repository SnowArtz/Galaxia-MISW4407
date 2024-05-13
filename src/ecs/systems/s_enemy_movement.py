import pygame
import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_grid_position import CGridPosition
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemy_movement(world: esper.World, screen: pygame.Surface, delta_time: float) -> None:
    screen_rect = screen.get_rect()
    change_direction = 0
    max_right = float('-inf')  
    min_left = float('inf')  

    for ent, (transform, velocity, surface, _, state) in world.get_components(CTransform, CVelocity, CSurface, CTagEnemy, CEnemyState):
        if state.state == EnemyState.ATTACKING:
            continue
        sprite_width = surface.area.width
        top_left = transform.position.x
        bottom_right = top_left + sprite_width

        max_right = max(max_right, bottom_right)
        min_left = min(min_left, top_left)
        if bottom_right >= screen_rect.width - 20:
            change_direction = -1
        elif top_left <= 20:
            change_direction = 1

    for ent, (transform, velocity, surface, grid, _) in world.get_components(CTransform, CVelocity, CSurface, CGridPosition, CTagEnemy):
            if change_direction != 0:
                velocity.velocity.x = abs(velocity.velocity.x) * change_direction
            if not world.component_for_entity(ent, CEnemyState).state == EnemyState.RETURNING:
                transform.position.x += velocity.velocity.x * delta_time
            grid.x += velocity.velocity.x * delta_time
            if world.component_for_entity(ent, CEnemyState).state == EnemyState.IDLE:
                try:
                    animation = world.component_for_entity(ent, CAnimation)
                    if animation.curr_frame in {0, 1, 3}:
                        transform.position.y = transform.initial_position.y
                    elif animation.curr_frame == 2:
                        transform.position.y = transform.initial_position.y - 1
                    elif animation.curr_frame == 4:
                        transform.position.y = transform.initial_position.y - 2
                except KeyError:
                    pass


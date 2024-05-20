import math
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_grid_position import CGridPosition
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState

def system_enemy_state(world: esper.World, delta_time: float, screen_height: int, screen_width: int) -> None:
    player_entities = world.get_component(CTagPlayer)
    if player_entities:
        player_entity = player_entities[0][0]
        player_transform = world.component_for_entity(player_entity, CTransform)
    else:
        player_entity = None
        player_transform = None

    for ent, (enemy_animation, enemy_state, transform, grid_position) in world.get_components(CAnimation, CEnemyState, CTransform, CGridPosition):
        if enemy_state.state == EnemyState.IDLE:
            _do_idle_state(enemy_animation, enemy_state)
        elif enemy_state.state == EnemyState.EMERGING:
            _do_emerging_state(enemy_animation, transform, enemy_state, delta_time)
        elif enemy_state.state == EnemyState.ATTACKING:
            _do_attacking_state(enemy_animation, transform, enemy_state, grid_position, player_transform, delta_time, screen_height, screen_width)
        elif enemy_state.state == EnemyState.RETURNING:
            _do_returning_state(enemy_animation, transform, enemy_state, grid_position, delta_time)


def _do_idle_state(enemy_animation, enemy_state):
    _set_animation(enemy_animation, 0)
    enemy_state.emerge_angle = 0
    enemy_state.sprite_angle = 0
    enemy_state.shoots = 0


def _do_emerging_state(enemy_animation, transform, enemy_state, delta_time):
    _set_animation(enemy_animation, 0)
    radius = 1
    angle_speed = math.pi * 2
    enemy_state.emerge_angle += angle_speed * delta_time
    enemy_state.sprite_angle += 45 * delta_time
    transform.position += pygame.math.Vector2(enemy_state.emerge_direction*math.sin(enemy_state.emerge_angle) * radius, -math.cos(enemy_state.emerge_angle) * radius)

    if enemy_state.emerge_angle >= 0.8 * 3/2 * math.pi:
        enemy_state.sprite_angle = enemy_state.emerge_direction*90
        enemy_state.change_state(EnemyState.ATTACKING)

def _do_attacking_state(enemy_animation, transform, enemy_state, grid_position, player_transform, delta_time, screen_height, screen_width):
    _set_animation(enemy_animation, 0)
    y_threshold = 180
    if player_transform:
        target_pos = player_transform.position
    else:
        # Define una posición fija cuando el jugador no está presente
        target_pos = pygame.math.Vector2(128, 224)

    direction = target_pos - transform.position
    distance = direction.length()

    if transform.position.y > screen_height*1.2 or transform.position.x < 0 or transform.position.x > screen_width:
        transform.position.y = 0
        transform.position.x = grid_position.x
        enemy_state.sprite_angle = 180
        enemy_state.change_state(EnemyState.RETURNING)
    elif transform.position.y > y_threshold:
        if hasattr(enemy_state, 'last_curve_direction'):
            transform.position += enemy_state.last_curve_direction * delta_time

        if player_transform and player_transform.position.x > transform.position.x and enemy_state.emerge_direction == 1:
            enemy_state.sprite_angle += 180 * delta_time
        elif player_transform and player_transform.position.x < transform.position.x and enemy_state.emerge_direction == -1:
            enemy_state.sprite_angle -= 180 * delta_time
        
    else:
        if distance > 1:
            direction = direction.normalize()
            curve_factor = pygame.math.Vector2(-direction.y, direction.x)
            if pygame.time.get_ticks() // 1000 % 2 == 0:
                curve_direction = curve_factor * 20
            else:
                curve_direction = -curve_factor * 20
            enemy_state.last_curve_direction = direction * enemy_state.speed + curve_direction
            transform.position += enemy_state.last_curve_direction * delta_time


def _do_returning_state(enemy_animation, transform, enemy_state, grid_position, delta_time):
    _set_animation(enemy_animation, 0)
    target_position = pygame.Vector2(grid_position.x, grid_position.y)
    if abs(transform.position.x - grid_position.x) < 3 and abs(transform.position.y - grid_position.y) < 3:
            transform.position.x = grid_position.x
            transform.position.y = grid_position.y
            enemy_state.change_state(EnemyState.IDLE)
    else:
        direction = (target_position - transform.position).normalize()
        transform.position.x =  grid_position.x * 0.5 + transform.position.x * 0.5
        transform.position.y += direction.y * 35 * delta_time
        if abs(transform.position.x - grid_position.x) < 35 and abs(transform.position.y - grid_position.y) < 35:
            enemy_state.sprite_angle += 180 * delta_time
        

def _set_animation(animation:CAnimation, index:int) -> None:
    if animation.curr_anim ==  index:
        return
    animation.curr_anim = index
    animation.curr_anim_time = 0
    animation.curr_frame = animation.animations_list[index].start

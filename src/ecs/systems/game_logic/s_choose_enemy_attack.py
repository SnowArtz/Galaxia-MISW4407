import esper
from src.ecs.components.c_cooldown import CCooldown
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_grid_position import CGridPosition
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
import random

from src.engine.service_locator import ServiceLocator

def system_choose_enemy_attack(world:esper.World, entity, enemy_config:dict):
    global_cooldown = world.component_for_entity(entity, CCooldown)

    if global_cooldown.current_time  > 0.1 :
        return

    components = world.get_components(CTagEnemy, CGridPosition, CEnemyState)
    most_left = None
    most_right = None
    for ent, (_, grid_pos, enemy_state) in components:
        if enemy_state.state != EnemyState.IDLE:
            continue
        if most_left is None:
            most_left = [(ent, grid_pos)]
        elif grid_pos.column < most_left[0][1].column:
            most_left = [(ent, grid_pos)]
        elif grid_pos.column == most_left[0][1].column and most_left[0][1].row > grid_pos.row and most_left[0][1].row > 1:
            most_left.append((ent, grid_pos))
        if most_right is None:
            most_right = [(ent, grid_pos)]
        elif grid_pos.column > most_right[0][1].column:
            most_right = [(ent, grid_pos)]
        elif grid_pos.column == most_right[0][1].column and most_right[0][1].row > grid_pos.row and most_right[0][1].row > 1:
            most_right.append((ent, grid_pos))
        emerge_direction = None
        if most_left is not None and most_right is not None:
            attackers = most_left + most_right
            random_attacker = random.choice(attackers)
            emerge_direction = -1 if random_attacker in most_left else 1
        elif most_left is not None:
            random_attacker = random.choice(most_left)
            emerge_direction = -1
        elif most_right is not None:
            random_attacker = random.choice(most_right)
            emerge_direction = 1
        else:
            return
    if (most_left is None and most_right is None) or not world.entity_exists(random_attacker[0]):
        return
    world.component_for_entity(random_attacker[0], CEnemyState).emerge_direction = emerge_direction
    world.component_for_entity(random_attacker[0], CEnemyState).state = EnemyState.EMERGING
    ServiceLocator.sounds_service.play(enemy_config["Enemy1"]["sound_chase"])
    global_cooldown.current_time = global_cooldown.cooldown_time

import pygame
import esper
from src.ecs.components.c_transform import CTransform


def system_game_over_animation(world:esper.World, delta_time, game_over_text_entity, config_window):
    position = world.component_for_entity(game_over_text_entity, CTransform).position
    target_x = config_window['size']['w'] / 2 - 35
    target_y = config_window['size']['h'] / 2 + 40

    # Si la posición x está a más de 5 unidades de distancia de la posición objetivo, continúa animando
    if abs(position.x - target_x) > 5:
        new_x = position.x + (target_x - position.x) * delta_time * 0.5
        world.component_for_entity(game_over_text_entity, CTransform).position = pygame.Vector2(new_x, target_y)
    else:
        # Una vez completada la animación, establece la posición final
        final_pos = pygame.Vector2(target_x, target_y)
        world.component_for_entity(game_over_text_entity, CTransform).position = final_pos
        return True  # Indica que la animación ha terminado
    return False  # Indica que la animación aún no ha terminado

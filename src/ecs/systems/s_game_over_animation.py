
import pygame
import esper
from src.ecs.components.c_text import CText
from src.ecs.components.c_transform import CTransform


def system_game_over_animation(world:esper.World, delta_time, game_over_text_entity, config_window):

    for ent, (text, transform) in world.get_components(CText, CTransform):
        if text.text == "GAME" or text.text == "OVER":
            position = transform.position
            if text.text == "GAME":
                new_x = position.x + 140 * delta_time * 0.5
                target_x = 95
            else:
                new_x = position.x - 140 * delta_time * 0.5
                target_x = 135


            if abs(position.x - target_x) > 5:
                if text.text == "GAME":
                    new_x = position.x + 140 * delta_time * 0.5
                else:
                    new_x = position.x - 140 * delta_time * 0.5
                transform.position.x = new_x
            else:
                transform.position.x = target_x

import esper
import pygame

from typing import Callable

from src.ecs.components.c_input_command import CInputCommand, CommandPhase

def system_input_player(world: esper.World, event: pygame.event.Event, action: Callable[[CInputCommand], None], is_paused:bool) -> None:
    for ent, input_command in world.get_component(CInputCommand):
        if event.type == pygame.KEYDOWN and event.key == input_command.key:
            if not is_paused:
                input_command.phase = CommandPhase.START
                action(input_command)
        elif event.type == pygame.KEYUP and event.key == input_command.key:
            if input_command.phase == CommandPhase.START:
                input_command.phase = CommandPhase.END
                action(input_command)
            input_command.phase = CommandPhase.END
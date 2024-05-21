import pygame
import esper
from src.ecs.components.c_timer import CTimer
from src.engine.service_locator import ServiceLocator

def system_check_timers_and_play_sound(world: esper.World, delta_time: float, entity):
    if world.entity_exists(entity) is False:
        return
    current_time = pygame.time.get_ticks()
    timer = world.component_for_entity(entity, CTimer)
    if current_time >= (timer.start_time + timer.duration + 1000) and not timer.finished:
        ServiceLocator.sounds_service.play("assets\snd\game_loop.ogg", loops=-1)
        timer.finished = True 

import esper
import pygame

from src.ecs.components.c_text import CText
from src.ecs.components.c_blink import CBlink  
from src.ecs.components.c_timer import CTimer
from src.ecs.components.c_transform import CTransform

def system_render_text(world: esper.World, screen: pygame.Surface):
    
    text_components = world.get_components(CTransform, CText)
    for ent, (transform, text) in text_components:
        timer = world.try_component(ent, CTimer)
        if timer and not (pygame.time.get_ticks() >= timer.start_time and pygame.time.get_ticks() < timer.start_time + timer.duration):
            continue
        blink = world.try_component(ent, CBlink)
        if blink and not blink.visible:
            continue
        text_render = text.font.render(text.text, True, text.color)
        text_rect = text_render.get_rect()
        text_rect.topleft = transform.position
        screen.blit(text_render, text_rect)
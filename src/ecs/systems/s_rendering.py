import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_text import CText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_blink import CBlink  

def system_rendering(world: esper.World, screen: pygame.Surface) -> None:
    components = world.get_components(CTransform, CSurface)
    for ent, (transform, surface) in components:
        screen.blit(surface.surface, transform.position, area=surface.area)

    text_components = world.get_components(CTransform, CText)
    for ent, (transform, text) in text_components:
        blink = world.try_component(ent, CBlink)
        if blink and not blink.visible:
            continue 
        text_render = text.font.render(text.text, True, text.color)
        text_rect = text_render.get_rect()
        text_rect.topleft = transform.position
        screen.blit(text_render, text_rect)

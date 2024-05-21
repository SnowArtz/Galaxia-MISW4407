import pygame

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_star import CStar

def system_render_stars(world, screen):
    for ent, (star, blink) in world.get_components(CStar, CBlink):
        if blink.visible:
            screen.fill(star.color, (star.position, (1, 1)))
import pygame

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_star import CStar

def system_update_stars(world, dt, screen_height):
    current_time = pygame.time.get_ticks()
    for ent, (star, blink) in world.get_components(CStar, CBlink):
        star.position = (star.position[0], (star.position[1] + star.vertical_speed * dt) % screen_height)
        if current_time > blink.next_blink_time:
            blink.visible = not blink.visible
            blink.next_blink_time = current_time + int(blink.blink_rate * 1000)
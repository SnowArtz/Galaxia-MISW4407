from src.ecs.components.c_cooldown import CCooldown


def system_cooldown(world, delta_time):
    for ent, (cooldown,) in world.get_components(CCooldown):
        if cooldown.current_time > 0:
            cooldown.current_time -= delta_time
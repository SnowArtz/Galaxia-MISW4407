import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_movement(world: esper.World, delta_time:float) -> None:
    components = world.get_components(CTransform, CVelocity)
    for ent, (transform, velocity) in components:
        transform.position.x += velocity.velocity.x * delta_time
        transform.position.y += velocity.velocity.y * delta_time
        pass
    pass
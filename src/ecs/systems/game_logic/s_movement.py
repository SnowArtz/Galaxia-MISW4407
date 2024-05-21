import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_movement(world: esper.World, delta_time:float) -> None:
    components = world.get_components(CTransform, CVelocity)
    for ent, (transform, velocity) in components:
        if not world.has_component(ent, CTagEnemy):
            transform.position.x += velocity.velocity.x * delta_time
            transform.position.y += velocity.velocity.y * delta_time
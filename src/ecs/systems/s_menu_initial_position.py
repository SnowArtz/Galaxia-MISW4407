import esper

from src.ecs.components.c_transform import CTransform

def system_menu_initial_position(world: esper.World) -> None:
    text_components = world.get_components(CTransform,)
    for ent, (transform, ) in text_components:
        transform.position.y += 236
    
 
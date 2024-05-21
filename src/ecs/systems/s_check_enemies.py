import esper
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_check_all_enemies_defeated(world: esper.World) -> bool:
    enemies = world.get_components(CTagEnemy)
    return not bool(enemies)

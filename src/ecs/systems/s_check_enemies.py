import esper
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_check_all_enemies_defeated(world: esper.World) -> bool:
    # Busca todas las entidades con el componente CTagEnemy
    enemies = world.get_components(CTagEnemy)
    # Si no hay entidades, todos los enemigos han sido derrotados
    return not bool(enemies)

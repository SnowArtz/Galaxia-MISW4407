from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_clear_player_and_bullets(world):
    for entity, _ in world.get_components(CTagPlayer):
        world.delete_entity(entity)
    for entity, _ in world.get_components(CTagBullet):
        world.delete_entity(entity)

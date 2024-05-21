import esper

from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.create.prefab_creator import create_player_explosion_sprite

def system_player_dead(world:esper.World, player_explosion_file: dict, config_level: dict, player_entity: int, bullet_entity: int, self):
    create_player_explosion_sprite(world, player_entity, player_explosion_file)
    self._game_engine.lives-=1
    world.delete_entity(player_entity)
    if world.entity_exists(bullet_entity) and not world.component_for_entity(bullet_entity, CTagBullet).active:
        world.delete_entity(bullet_entity)
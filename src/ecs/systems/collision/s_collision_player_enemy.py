import esper
from src.ecs.components.c_score import CScore
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.systems.player.s_player_dead import system_player_dead

def system_collision_player_enemy(world: esper.World, player_entity: int, config_level: dict, player_explosion_file: dict, update_global_score, bullet_entity, self):
    if world.entity_exists(player_entity) == False:
        return
    componentsE = world.get_components(CSurface, CTransform, CTagEnemy, CScore)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_rect = CSurface.get_relative_area(pl_s.area, pl_t.position)
    pl_rect.topleft = pl_t.position
    for enemy_entity, (c_s, c_t, _, c_score) in componentsE:
        ene_rect = CSurface.get_relative_area(c_s.area, c_t.position)
        if ene_rect.colliderect(pl_rect):
            if c_score:
                update_global_score(c_score.base_score + c_score.state_score)
            world.delete_entity(enemy_entity)
            system_player_dead(world, player_explosion_file, config_level, player_entity, bullet_entity, self)

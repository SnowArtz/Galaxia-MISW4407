import esper
from src.ecs.components.c_score import CScore
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

from src.create.prefab_creator import create_enemy_explosion_sprite
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState

def system_collision_bullet_enemy(world: esper.World, bullet_entity: int, enemy_explosion_file: dict, update_global_score):
    componentsE = world.get_components(CSurface, CTransform, CTagEnemy, CScore, CEnemyState)
    componentsB = world.get_components(CSurface, CTransform, CTagBullet)
    for bullet_entity, (bullet_s, bullet_t, bullet_tag) in componentsB:
        if bullet_tag.active:
            bullet_rect = bullet_s.area.copy()
            bullet_rect.topleft = bullet_t.position
            for enemy_entity, (c_s, c_t, _, c_score, c_state) in componentsE:
                ene_rect = CSurface.get_relative_area(c_s.area, c_t.position)
                ene_rect.topleft = c_t.position
                if ene_rect.colliderect(bullet_rect):
                    if c_state.state == EnemyState.IDLE:
                        update_global_score(c_score.state_scores['IDLE'])
                    else:
                        update_global_score(c_score.state_scores['default'])
                    create_enemy_explosion_sprite(world, enemy_entity, enemy_explosion_file)
                    world.delete_entity(enemy_entity)
                    world.delete_entity(bullet_entity)

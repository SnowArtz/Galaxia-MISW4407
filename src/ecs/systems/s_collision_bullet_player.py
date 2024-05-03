import esper
from src.create.prefab_creator import create_player_explosion_sprite
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_collision_bullet_player(world:esper.World, enemy_bullet_entity:int, player_explosion_file):
    componentsP = world.get_components(CSurface, CTransform, CTagPlayer)
    componentsB = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    for enemy_bullet_entity, (enemy_bullet_s, enemy_bullet_t, _) in componentsB:
        bullet_rect = enemy_bullet_s.area.copy()
        bullet_rect.topleft = enemy_bullet_t.position
        for player_entity, (c_s, c_t, _) in componentsP:
            ene_rect = CSurface.get_relative_area(c_s.area, c_t.position)
            ene_rect.topleft = c_t.position
            if ene_rect.colliderect(bullet_rect):
                world.delete_entity(player_entity)
                world.delete_entity(enemy_bullet_entity)
                create_player_explosion_sprite(world, player_entity, player_explosion_file)

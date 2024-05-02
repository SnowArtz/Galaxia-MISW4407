import esper
from src.create.prefab_creator import create_enemy_explosion_sprite
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_collision_bullet_enemy(world:esper.World, bullet_entity:int, enemy_explosion_file):
    componentsE = world.get_components(CSurface, CTransform, CTagEnemy)
    componentsB = world.get_components(CSurface, CTransform, CTagBullet)
    for bullet_entity, (bullet_s, bullet_t, bullet_tag) in componentsB:
        bullet_rect = bullet_s.area.copy()
        bullet_rect.topleft = bullet_t.position
        for enemy_entity, (c_s, c_t, _) in componentsE:
            ene_rect = CSurface.get_relative_area(c_s.area, c_t.position)
            ene_rect.topleft = c_t.position
            if ene_rect.colliderect(bullet_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                create_enemy_explosion_sprite(world, enemy_entity, enemy_explosion_file)

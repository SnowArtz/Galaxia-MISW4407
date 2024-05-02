

import esper
from src.create.prefab_creator import create_bullet
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_player_bullet(world:esper.World, player_entity:int, config_bullet:dict):
    components = world.get_components(CTransform, CSurface, CTagBullet)
    player_position = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)
    pl_rect = player_surface.surface.get_rect(topleft = player_position.position)
    for bullet_entity, (bullet_position, bullet_surface, bullet_tag) in components:
        if bullet_tag.active == False:
            bullet_size = bullet_surface.surface.get_rect().size
            bullet_position.position.x = pl_rect.x + player_surface.area.size[0] /2 - (bullet_size[0] / 2)-1
            bullet_position.position.y = pl_rect.y - (bullet_size[1] / 2)-1
    num_components = len(world.get_components(CTagBullet))
    if num_components == 0:
        bullet_entity = create_bullet(world, player_entity, config_bullet)
    return bullet_entity

        


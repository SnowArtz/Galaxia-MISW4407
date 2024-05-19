import pygame
import esper
from src.ecs.components.c_cooldown import CCooldown
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_score import CScore
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator import create_player_explosion_sprite
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_player_dead import system_player_dead

def system_collision_player_enemy(world: esper.World, player_entity: int, config_level: dict, player_explosion_file: dict, update_global_score, bullet_player_entity):
    componentsE = world.get_components(CSurface, CTransform, CTagEnemy, CScore)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_tag = world.component_for_entity(player_entity, CTagPlayer)
    pl_state = world.component_for_entity(player_entity, CPlayerState)
    
    #bullet_player_tag = world.component_for_entity(bullet_player_entity, CTagBullet)

    size = pl_s.surface.get_size()
    pos = pygame.Vector2(config_level["player_spawn"]["position"]["x"]  - (size[0] / 2),
                         config_level["player_spawn"]["position"]["y"]  - (size[1] / 2))
    pl_rect = CSurface.get_relative_area(pl_s.area, pl_t.position)
    pl_rect.topleft = pl_t.position
    for enemy_entity, (c_s, c_t, _, c_score) in componentsE:
        ene_rect = CSurface.get_relative_area(c_s.area, c_t.position)
        if ene_rect.colliderect(pl_rect):
            # Antes de eliminar, actualiza el puntaje
            if c_score:  # Asegúrate de que el enemigo tiene un componente CScore
                update_global_score(c_score.base_score + c_score.state_score)
            world.add_component(bullet_player_entity, CCooldown(3))
            world.add_component(player_entity, CCooldown(3))
            #bullet_player_tag.visible = False
            pl_tag.visible = False
            pl_state.change_state(PlayerState.DEAD)
            world.delete_entity(enemy_entity)

            system_player_dead(world, player_explosion_file, config_level, player_entity)

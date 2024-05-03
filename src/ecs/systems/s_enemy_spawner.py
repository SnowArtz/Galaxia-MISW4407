import pygame
import esper
from src.create.prefab_creator import create_enemy, create_sprite
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator


def system_enemy_spawner(world, config_enemy, config_enemies_list):
    for entity, (spawner,) in world.get_components(CEnemySpawner):
        for event in config_enemies_list['enemy_spawn_events']:
            if event not in spawner.spawned_events:
                enemy_details = config_enemy[event['enemy_type']]
                position = pygame.Vector2(event['position']['x'], event['position']['y'])
                enemy_entity = create_enemy(world, position, enemy_details)
                spawner.spawned_events.append(event)



import pygame
from src.create.prefab_creator import create_enemy
from src.ecs.components.c_cooldown import CCooldown
from src.ecs.components.c_enemy_spawner import CEnemySpawner

def system_enemy_spawner(world, config_enemy, config_enemies_list,self):
    rows = config_enemies_list['rows']
    columns = config_enemies_list['columns']
    for _, (spawner, cooldown) in world.get_components(CEnemySpawner, CCooldown):
        if cooldown.current_time > 0.1:
            continue
        for event in spawner.spawn_events:
            if event not in spawner.spawned_events:
                self.enemies_initialized=True
                enemy_details = config_enemy[event['enemy_type']]
                y_position = rows[str(event['row'])]
                x_position = columns[str(event['column'])]
                position = pygame.Vector2(x_position, y_position)
                row = event['row']
                column = event['column']
                create_enemy(world, position, enemy_details, row, column)
                spawner.spawned_events.append(event)

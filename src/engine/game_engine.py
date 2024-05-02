import os
import json
import esper
import pygame

from pathlib import Path

from src.create.prefab_creator import create_bullet, create_input_player, create_player
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_bullet_player import system_collision_bullet_player
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_explosion import system_explosion
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_limit_player import system_limit_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_bullet import system_player_bullet
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_delete_bullet import system_screen_delete_bullet
from src.engine.service_locator import ServiceLocator

class GameEngine:
    def __init__(self) -> None:
        self.config_folder = 'cfg'
        self._load_configurations()

        pygame.init()
        self.screen = pygame.display.set_mode((self.config_window["size"]["w"], self.config_window["size"]["h"]), pygame.SCALED)
        pygame.display.set_caption(self.config_window["title"])


        self.delta_time = 0
        self.is_paused = False
        self.is_running = False
        self.ecs_world = esper.World()
        self.clock = pygame.time.Clock()
        self.frame_rate = self.config_window["framerate"]
        self.max_bullets = 1
        self._bullet_entity = None


    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self._player_entity = create_player(self.ecs_world, pygame.Vector2(self.config_level['player_spawn']["position"]["x"], self.config_level['player_spawn']["position"]["y"]), self.config_player)
        self._player_c_velocity = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_transform = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_surface = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        create_input_player(self.ecs_world)
        self._bullet_entity = create_bullet(self.ecs_world, self._player_entity, self.config_bullet)
        self._bullet_entity_tag = self.ecs_world.component_for_entity(self._bullet_entity, CTagBullet)
        self._bullet_entity_tag.active = False

    def _calculate_time(self):
        self.clock.tick(self.frame_rate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action, self.is_paused)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_limit_player(self.ecs_world, self.screen)
        system_screen_delete_bullet(self.ecs_world, self.screen)
        system_collision_bullet_enemy(self.ecs_world, self._bullet_entity, self.config_enemy_explosion)
        system_collision_bullet_player(self.ecs_world, self._bullet_entity, self.config_player_explosion)
        system_collision_player_enemy(self.ecs_world, self._player_entity, self.config_level, self.config_player_explosion)
        system_explosion(self.ecs_world)
        system_animation(self.ecs_world, self.delta_time)
        self._bullet_entity = system_player_bullet(self.ecs_world, self._player_entity, self.config_bullet)
        self.ecs_world._clear_dead_entities()


    def _draw(self):
        self.screen.fill((self.config_window['bg_color']['r'], self.config_window['bg_color']['g'], self.config_window['bg_color']['b']))
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()


    def _do_action(self, c_input: CInputCommand, mouse_x:int = 0, mouse_y:int = 0):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_velocity.velocity.x -= self.config_player["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_velocity.velocity.x += self.config_player["input_velocity"]
        elif c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_velocity.velocity.x += self.config_player["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_velocity.velocity.x -= self.config_player["input_velocity"]
        elif c_input.name == "PLAYER_FIRE":
            num_components = len(self.ecs_world.get_components(CTagBullet))
            if num_components != 0:
                bullet_tag = self.ecs_world.component_for_entity(self._bullet_entity, CTagBullet)
                if num_components == self.max_bullets and bullet_tag.active == False:
                    if c_input.phase == CommandPhase.START:
                        bullet_tag.active = True
                        self._bullet_c_v = self.ecs_world.component_for_entity(self._bullet_entity, CVelocity)
                        direction = pygame.math.Vector2(0, -1)
                        direction = direction.normalize()
                        self._bullet_c_v.velocity = direction*self.config_bullet["velocity"]
                        ServiceLocator.sounds_service.play(self.config_bullet["sound"])


                    

    def _load_configurations(self):
        current_file_path = Path(__file__)
        base_path = current_file_path.parents[2]
        config_files = ['interface.json', 'starfield.json', 'window.json', 'level.json', 'player.json', 'enemy.json', 'bullet.json', 'enemy_explosion.json', 'player_explosion.json']
        config_attrs = ['config_interface', 'config_starfield', 'config_window', 'config_level', 'config_player', 'config_enemy', 'config_bullet', 'config_enemy_explosion', 'config_player_explosion']
        
        for file, attr in zip(config_files, config_attrs):
            try:
                with open(os.path.join(base_path, 'assets', self.config_folder, file)) as f:
                    setattr(self, attr, json.load(f))
            except FileNotFoundError:
                print(f"Configuration file {file} not found.")
            except json.JSONDecodeError:
                print(f"Error parsing the JSON file {file}.")

        self.config_interface
        self.config_starfield
        self.config_window
        self.config_level
        self.config_player
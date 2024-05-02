import os
import json
import esper
import pygame

from pathlib import Path

from src.create.prefab_creator import create_input_player, create_level_flags, create_lives_display, create_player, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_limit_player import system_limit_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_render_flags import system_render_flags
from src.ecs.systems.s_render_lives import system_render_lives
from src.ecs.systems.s_rendering import system_rendering

class GameEngine:
    def __init__(self) -> None:
        self.config_folder = 'cfg'
        self._load_configurations()

        pygame.init()
        self.screen = pygame.display.set_mode((self.config_window["size"]["w"], self.config_window["size"]["h"]), pygame.SCALED)
        pygame.display.set_caption(self.config_window["title"])

        self.lives = 3
        self.level = 3
        self.delta_time = 0
        self.is_paused = False
        self.is_running = False
        self.ecs_world = esper.World()
        self.clock = pygame.time.Clock()
        self.frame_rate = self.config_window["framerate"]

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

        create_text(self.ecs_world, self.config_texts["1UP"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["SCORE"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["HIGH_SCORE"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["HIGH_SCORE_VALUE"], self.config_interface)

        create_lives_display(self.ecs_world)
        create_level_flags(self.ecs_world)

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

    def _draw(self):
        self.screen.fill((self.config_window['bg_color']['r'], self.config_window['bg_color']['g'], self.config_window['bg_color']['b']))
        system_rendering(self.ecs_world, self.screen)
        system_render_lives(self.ecs_world, self.screen, self.lives)
        system_render_flags(self.ecs_world, self.screen, self.level)
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

    def _load_configurations(self):
        current_file_path = Path(__file__)
        base_path = current_file_path.parents[2]
        config_files = ['interface.json', 'starfield.json', 'window.json', 'level.json', 'player.json', 'texts.json']
        config_attrs = ['config_interface', 'config_starfield', 'config_window', 'config_level', 'config_player', 'config_texts']
        
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
        self.config_texts = self.config_texts["texts"]

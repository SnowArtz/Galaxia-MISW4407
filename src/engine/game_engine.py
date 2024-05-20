import os
import json
import esper
import pygame

from pathlib import Path
from src.game.game_over_scene import GameOverScene
from src.game.menu_scene import MenuScene
from src.game.play_scene import PlayScene
from src.ecs.components.c_input_command import CInputCommand

class GameEngine:
    def __init__(self) -> None:
        
        # Configuration variables
        self.config_folder = 'cfg'
        self.config_interface = None
        self.config_starfield = None
        self.config_window = None
        self.config_level = None
        self.config_player = None
        self.config_bullet = None
        self.config_enemy_explosion = None
        self.config_player_explosion = None
        self.config_texts = None
        self.config_enemies_list = None
        self.config_enemy = None
        self.config_enemy_bullet = None
        self.current_level = 1
        self.global_score = 0
        self.lives = 1
        self.level = 1
    

        self._load_configurations()

        self.ecs_world = esper.World()

        pygame.init()
        self.screen = pygame.display.set_mode((self.config_window["size"]["w"], self.config_window["size"]["h"]), pygame.SCALED)
        pygame.display.set_caption(self.config_window["title"])

        self.delta_time = 0
        self.is_running = False
        self.clock = pygame.time.Clock()
        self.frame_rate = self.config_window["framerate"]
       
        self._scenes = dict()
        self._scenes["MENU_SCENE"] = MenuScene(self, self.ecs_world, self.config_texts, self.config_interface)
        self._scenes["PLAY_SCENE"] = PlayScene(self, self.ecs_world, self.config_interface, self.config_starfield, self.config_window, self.config_level, self.config_player, self.config_bullet, self.config_enemy_explosion, self.config_player_explosion, self.config_texts, self.config_enemies_list, self.config_enemy, self.config_enemy_bullet)
        self._scenes["GAME_OVER_SCENE"] = GameOverScene(self, self.ecs_world, self.config_texts, self.config_interface)
        self._current_scene = None
        self._scene_name_to_switch = None
        
    def run(self, start_scene_name: str) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
        self._clean()

    def switch_scene(self, new_scene_name:str):
        self._scene_name_to_switch = new_scene_name

    def _create(self):
        self._current_scene.do_create()
        
    def _calculate_time(self):
        self.clock.tick(self.frame_rate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self.delta_time)
       
    def _draw(self):
        self.screen.fill((self.config_window['bg_color']['r'], self.config_window['bg_color']['g'], self.config_window['bg_color']['b']))
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.do_clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_action(self, c_input: CInputCommand, mouse_x:int = 0, mouse_y:int = 0):
        self._current_scene.do_action(c_input, mouse_x, mouse_y)

    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()

    def _load_configurations(self):
        current_file_path = Path(__file__)
        base_path = current_file_path.parents[2]
        config_files = ['interface.json', 'starfield.json', 'window.json', 'level.json', 'player.json', 'bullet.json', 'enemy_explosion.json', 'player_explosion.json','texts.json','enemies_list.json','enemy.json', 'enemy_bullet.json']
        config_attrs = ['config_interface', 'config_starfield', 'config_window', 'config_level', 'config_player', 'config_bullet', 'config_enemy_explosion', 'config_player_explosion', 'config_texts', 'config_enemies_list', 'config_enemy', 'config_enemy_bullet']
        for file, attr in zip(config_files, config_attrs):
            try:
                with open(os.path.join(base_path, 'assets', self.config_folder, file)) as f:
                    setattr(self, attr, json.load(f))
            except FileNotFoundError:
                print(f"Configuration file {file} not found.")
            except json.JSONDecodeError:
                print(f"Error parsing the JSON file {file}.")
        

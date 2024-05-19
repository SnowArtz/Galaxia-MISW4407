import pygame

from src.engine.scenes.scene import Scene
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_static_image import CStaticImage
from src.ecs.components.c_input_command import CInputCommand, CommandPhase

from src.ecs.systems.s_render_text import system_render_text
from src.ecs.systems.s_blink_text import system_blinking_text
from src.ecs.systems.s_update_stars import system_update_stars
from src.ecs.systems.s_render_stars import system_render_stars
from src.ecs.systems.s_menu_movement import system_menu_movement
from src.ecs.systems.s_render_static_images import system_render_static_images
from src.ecs.systems.s_menu_initial_position import system_menu_initial_position
from src.create.prefab_creator import create_stars, create_static_image, create_text

class MenuScene(Scene):

    def __init__(self, game_engine, ecs_world, config_texts:dict, config_interface:dict) -> None:
        super().__init__(game_engine, ecs_world)
        self.config_texts = config_texts
        self.config_interface = config_interface

    def do_create(self):
        create_stars(self.ecs_world, self._game_engine.config_starfield, self._game_engine.config_window)
        create_text(self.ecs_world, self.config_texts["HIGH_SCORE"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["1UP"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["SCORE_P1"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["2UP"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["SCORE_P2"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["HIGH_SCORE"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["HIGH_SCORE_VALUE"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["1_PLAYER"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["2_PLAYERS"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["PRESS_Z"], self.config_interface, blink=True, blink_rate=0.75)
        create_text(self.ecs_world, self.config_texts["INSTRUCTIONS_1"], self.config_interface)
        create_text(self.ecs_world, self.config_texts["INSTRUCTIONS_2"], self.config_interface)

        self.ecs_world.add_component(create_static_image(self.ecs_world, "logo_title", pygame.Vector2(60, 60)), CTransform(pygame.Vector2(60, 60)))
        self.selector_entity = create_static_image(self.ecs_world, "selector", pygame.Vector2(80, 123))
        self.ecs_world.add_component(self.selector_entity, CTransform(pygame.Vector2(80, 124)))

        start_game_action = self.ecs_world.create_entity()
        input_up = self.ecs_world.create_entity()
        input_down = self.ecs_world.create_entity()

        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
        self.ecs_world.add_component(input_up, CInputCommand("UP", pygame.K_UP))
        self.ecs_world.add_component(input_down, CInputCommand("DOWN", pygame.K_DOWN))
        system_menu_initial_position(self.ecs_world)
        
    def do_update(self, delta_time: float):
        self._game_engine.global_score=0
        self._game_engine.lives=3
        self._game_engine.current_level=1
        system_update_stars(self.ecs_world, delta_time, self._game_engine.config_window["size"]["h"])
        
    def do_draw(self, screen):
        system_render_stars(self.ecs_world, screen)
        system_blinking_text(self.ecs_world, self._game_engine.delta_time)
        system_menu_movement(self.ecs_world, self._game_engine.delta_time)
        system_render_static_images(self.ecs_world, screen)
        system_render_text(self.ecs_world, screen)
        super().do_draw(screen)
        
    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("PLAY_SCENE")
        if  self.ecs_world.component_for_entity(self.selector_entity, CStaticImage).already_in_final_position:
            if action.name == "UP" and action.phase == CommandPhase.START:
                if abs(self.ecs_world.component_for_entity(self.selector_entity, CTransform).position.y - 138) < 2:
                    self.ecs_world.component_for_entity(self.selector_entity, CTransform).position = pygame.Vector2(80, 123)
            elif action.name == "DOWN" and action.phase == CommandPhase.START:        
                if abs(self.ecs_world.component_for_entity(self.selector_entity, CTransform).position.y - 123) < 2:
                    self.ecs_world.component_for_entity(self.selector_entity, CTransform).position = pygame.Vector2(80, 138)

    def do_clean(self):
        return super().do_clean()
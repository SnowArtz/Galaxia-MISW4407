import pygame

from src.create.prefab_creator import create_text
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.systems.s_blink_text import system_blinking_text
from src.ecs.systems.s_render_text import system_render_text
from src.engine.scenes.scene import Scene
from src.ecs.components.c_input_command import CInputCommand
from src.engine.service_locator import ServiceLocator 

class MenuScene(Scene):

    def __init__(self, game_engine, config_texts:dict, config_interface:dict) -> None:
        super().__init__(game_engine)
        self.config_texts = config_texts
        self.config_interface = config_interface

    
    def do_create(self):
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


        image_entity = self.ecs_world.create_entity()
        image_surface = ServiceLocator.images_service.get("assets/img/invaders_logo_title.png")
        self.ecs_world.add_component(image_entity, CSurface.from_surface(image_surface))
        self.ecs_world.add_component(image_entity, CTransform(position=pygame.Vector2(60, 60)))
        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
        
    def do_draw(self, screen):
        super().do_draw(screen)
        system_render_text(self.ecs_world, screen)
        system_blinking_text(self.ecs_world, self._game_engine.delta_time)
        
    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")
        

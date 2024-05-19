import pygame
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.ecs.systems.s_game_over_animation import system_game_over_animation
from src.ecs.systems.s_render_flags import system_render_flags
from src.ecs.systems.s_render_lives import system_render_lives
from src.ecs.systems.s_render_stars import system_render_stars
from src.ecs.systems.s_render_text import system_render_text
from src.ecs.systems.s_update_stars import system_update_stars
from src.engine.scenes.scene import Scene
from src.ecs.components.c_transform import CTransform
from src.create.prefab_creator import create_stars, create_text
from src.engine.service_locator import ServiceLocator

class GameOverScene(Scene):
    def __init__(self, game_engine, ecs_world, config_texts:dict, config_interface:dict) -> None:
        super().__init__(game_engine, ecs_world)
        self.config_texts = config_texts
        self.config_interface = config_interface

        # Inicializa las variables de estado aquí para mantenerlas claras
        self.reset_state()

    def reset_state(self):
        # Función para resetear el estado cuando se entra a la escena
        self.animation_started = False
        self.animation_completed = False
        self.initial_wait_time = 2.0
        self.elapsed_time = 0
        self.sound_delay_time = 1
        self.sound_played = False
        self.scene_switch_timer_started = False
        self.scene_switch_delay = 5.0
        self.scene_switch_elapsed_time = 0

    def do_create(self):
        # Asegúrate de reiniciar el estado cada vez que se crea la escena
        self.reset_state()
        # Crea "Game Over" utilizando la configuración nueva
        self.game_over_text = create_text(self.ecs_world, self.config_texts["GAME_OVER"], self.config_interface)

    def do_update(self, delta_time: float):
        system_update_stars(self.ecs_world, delta_time, self._game_engine.config_window['size']['h'])
        system_animation(self.ecs_world, delta_time)
        system_enemy_movement(self.ecs_world, self.screen, delta_time)

        self.elapsed_time += delta_time

        if not self.animation_started and self.elapsed_time > self.initial_wait_time:
            self.animation_started = True

        if self.animation_started and not self.animation_completed:
            self.animation_completed = system_game_over_animation(
                self.ecs_world,
                delta_time,
                self.game_over_text,
                self._game_engine.config_window
            )

            if not self.sound_played and (self.elapsed_time > self.initial_wait_time + self.sound_delay_time):
                ServiceLocator.sounds_service.play(self.config_texts["GAME_OVER"]["sound"])
                self.sound_played = True
                self.scene_switch_timer_started = True

        if self.scene_switch_timer_started:
            self.scene_switch_elapsed_time += delta_time
            if self.scene_switch_elapsed_time >= self.scene_switch_delay:
                self._game_engine.switch_scene("MENU_SCENE")

    def do_draw(self, screen):
        system_render_lives(self.ecs_world, screen, 0)
        system_render_flags(self.ecs_world, screen, self._game_engine.current_level, self.config_interface)
        system_render_stars(self.ecs_world, screen)
        system_render_text(self.ecs_world, screen)
        if self.animation_completed:
            system_render_text(self.ecs_world, screen)
        super().do_draw(screen)

    def do_clean(self):
        # Aquí puedes limpiar cualquier estado necesario
        super().do_clean()


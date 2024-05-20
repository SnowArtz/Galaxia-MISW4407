import asyncio
import time
import pygame


from src.ecs.components.c_timer import CTimer
from src.ecs.components.tags.c_tag_flag import CTagFlag
from src.ecs.components.tags.c_tag_life import CTagLife
from src.ecs.systems.s_clear_bullet_player import system_clear_player_and_bullets
from src.ecs.systems.s_enemy_bullet import system_enemy_bullet
from src.ecs.systems.s_player_xd import system_player_xd
from src.engine.scenes.scene import Scene
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_cooldown import CCooldown
from src.engine.service_locator import ServiceLocator
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand, CommandPhase

from src.ecs.systems.s_cooldown import system_cooldown
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_explosion import system_explosion
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_render_text import system_render_text
from src.ecs.systems.s_enemy_state import system_enemy_state
from src.ecs.systems.s_blink_text import system_blinking_text
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_limit_player import system_limit_player
from src.ecs.systems.s_render_flags import system_render_flags
from src.ecs.systems.s_render_lives import system_render_lives
from src.ecs.systems.s_render_stars import system_render_stars
from src.ecs.systems.s_update_score import system_update_score
from src.ecs.systems.s_update_stars import system_update_stars
from src.ecs.systems.s_player_bullet import system_player_bullet
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.ecs.systems.s_update_high_score import system_update_high_score
from src.ecs.systems.s_choose_enemy_attack import system_choose_enemy_attack
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_screen_delete_bullet import system_screen_delete_bullet
from src.ecs.systems.s_collision_bullet_player import system_collision_bullet_player
from src.ecs.systems.s_check_enemies import system_check_all_enemies_defeated

from src.create.prefab_creator import create_bullet, create_input_player, create_level_flags, create_lives_display, create_player, create_stars, create_text


class PlayScene(Scene):
    def __init__(self, engine, ecs_world, config_interface, config_starfield, config_window, config_level, config_player, config_bullet, config_enemy_explosion, config_player_exlosion, config_texts, config_enemies_list, config_enemy, config_enemy_bullet) -> None:
        super().__init__(engine, ecs_world)

        # Configuration variables
        self.config_texts = config_texts
        self.config_enemy = config_enemy
        self.config_level = config_level
        self.config_window = config_window
        self.config_player = config_player
        self.config_bullet = config_bullet
        self.config_interface = config_interface
        self.config_starfield = config_starfield
        self.config_enemies_list = config_enemies_list
        self.config_enemy_explosion = config_enemy_explosion
        self.config_player_explosion = config_player_exlosion
        self.config_enemy_bullet = config_enemy_bullet

        # Game variables
        self.enemies_initialized = False
        self.level = 1
        self.global_score=0
        self.max_bullets = 1
        self.is_paused = False
        self.active_keys = set()
        self._player_entity = None
        self._bullet_entity = None
        self.paused_text_entity = None
        self.level_text_entity = None
        self.switch_game_over=False
        

    def do_create(self):
        if self.level > 5:
            self.config_texts["LEVEL"]["content"] = f"{self.level:02}"
            self.level_text_entity = create_text(self.ecs_world, self.config_texts["LEVEL"], self.config_interface)
        if self._player_entity not in self.ecs_world._entities:
            create_stars(self.ecs_world, self.config_starfield, self.config_window)
            self.ready_text_entity = create_text(self.ecs_world, self.config_texts["READY"], self.config_interface)
            self.ecs_world.add_component(self.ready_text_entity, CTimer(pygame.time.get_ticks(), 1500))
            self.spawner_entity = self.ecs_world.create_entity()
            self.ecs_world.add_component(self.spawner_entity, CEnemySpawner(self.config_enemies_list['enemy_spawn_events']))
            self.ecs_world.add_component(self.spawner_entity, CCooldown(0.5))
            self._player_entity = create_player(self.ecs_world, pygame.Vector2(self.config_level['player_spawn']["position"]["x"], self.config_level['player_spawn']["position"]["y"]), self.config_player)
            self._player_c_velocity = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
            self._player_c_transform = self.ecs_world.component_for_entity(self._player_entity, CTransform)
            self._player_c_surface = self.ecs_world.component_for_entity(self._player_entity, CSurface)
            self._player_c_cooldown = self.ecs_world.component_for_entity(self._player_entity, CCooldown)
            create_input_player(self.ecs_world)
            self._bullet_entity = create_bullet(self.ecs_world, pygame.Vector2(0, 0), self.config_bullet, 2.5)
            create_text(self.ecs_world, self.config_texts["1UP"], self.config_interface)
            self.score_entity = create_text(self.ecs_world, self.config_texts["SCORE_P1"], self.config_interface)
            create_text(self.ecs_world, self.config_texts["HIGH_SCORE"], self.config_interface)
            self.high_score_text_entity = create_text(self.ecs_world, self.config_texts["HIGH_SCORE_VALUE"], self.config_interface)
        else:
            self.spawner_entity = self.ecs_world.create_entity()
            self.ecs_world.add_component(self.spawner_entity, CEnemySpawner(self.config_enemies_list['enemy_spawn_events']))
            self.ecs_world.add_component(self.spawner_entity, CCooldown(2))
        ServiceLocator.sounds_service.play(self.config_texts["READY"]["sound"])
        self.attack_cooldown = self.ecs_world.create_entity()
        self.bullet_enemy_cooldown = self.ecs_world.create_entity()
        self.ecs_world.add_component(self.attack_cooldown, CCooldown(10))
        self.ecs_world.add_component(self.bullet_enemy_cooldown, CCooldown(3))
        create_lives_display(self.ecs_world)
        create_level_flags(self.ecs_world)
            
    def do_process_events(self, event:pygame.event):
        if event.type == pygame.QUIT:
            self.is_running = False
        
        elif self._player_c_cooldown.current_time > 0.1:
            return
        system_input_player(self.ecs_world, event, self.do_action, self.is_paused)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not self.is_paused:
                    self.is_paused = True
                    self.paused_text_entity = create_text(self.ecs_world, self.config_texts["PAUSED"], self.config_interface, blink=True, blink_rate=0.5)
                    ServiceLocator.sounds_service.play(self.config_interface["sound"])
                else:
                    self.is_paused = False
                    if self.paused_text_entity:
                        self.ecs_world.delete_entity(self.paused_text_entity)
                        self.paused_text_entity = None
    def do_update(self, delta_time: float):
        system_update_stars(self.ecs_world, delta_time, self.config_window["size"]["h"])
        if self.is_paused:
            system_blinking_text(self.ecs_world, delta_time)
        else:
            system_movement(self.ecs_world, delta_time)
            system_enemy_movement(self.ecs_world, self.screen, delta_time)
            system_screen_delete_bullet(self.ecs_world, self.screen)
            system_enemy_spawner(self.ecs_world, self.config_enemy, self.config_enemies_list,self)
            system_explosion(self.ecs_world)
            system_animation(self.ecs_world, delta_time)
            system_cooldown(world=self.ecs_world, delta_time=delta_time)
            system_update_score(self.ecs_world, self.global_score, self.score_entity, self.config_texts)
            system_update_high_score(self.ecs_world, self.global_score, self.config_texts, self.high_score_text_entity)
            system_enemy_state(world=self.ecs_world, delta_time=delta_time, screen_height=self.screen.get_rect().height, screen_width=self.screen.get_rect().width)

            self.ecs_world._clear_dead_entities()
            if self.enemies_initialized and system_check_all_enemies_defeated(self.ecs_world):
                self.enemies_initialized = False
                self.switch_scene("PLAY_SCENE")
                self.level += 1
            if self._game_engine.lives == -1 and not self.switch_game_over:
                self._game_engine.current_level = self.level
                self.switch_game_over = True
                self.time_init = pygame.time.get_ticks()
                system_clear_player_and_bullets(self.ecs_world)
            
            if not self.switch_game_over and self.ecs_world.entity_exists(self._player_entity):
               
                if not self.ecs_world.component_for_entity(self._player_entity, CCooldown).current_time > 0.1:
                    
                    system_enemy_bullet(self.ecs_world, self.config_enemy_bullet, self.bullet_enemy_cooldown)
                    system_choose_enemy_attack(self.ecs_world, self.attack_cooldown, self.config_enemy)
                    system_limit_player(self.ecs_world, self.screen)
                    system_collision_bullet_enemy(self.ecs_world, self._bullet_entity, self.config_enemy_explosion, self.update_global_score)
                    system_collision_bullet_player(self.ecs_world, self.config_player_explosion, self.config_level, self._bullet_entity, self)
                    system_collision_player_enemy(self.ecs_world, self._player_entity, self.config_level, self.config_player_explosion, self.update_global_score,self._bullet_entity, self)
                    self._bullet_entity = system_player_bullet(self.ecs_world, pygame.Vector2(self._player_c_transform.position.x + self._player_c_surface.area.width/2, self._player_c_transform.position.y), self.config_bullet, self._player_entity)
                    system_explosion(self.ecs_world)
                    system_animation(self.ecs_world, delta_time)

            elif self.switch_game_over:
                current_time = pygame.time.get_ticks()
                if (current_time - self.time_init) >= 2500:  
                    self.switch_game_over = False
                    self.enemies_initialized = False
                    self.global_score=0
                    self.level = 1
                    self.switch_scene("GAME_OVER_SCENE") 
            else:
                system_player_xd(self.ecs_world, self, self.config_level, self.config_player, self.config_texts, self.config_interface)            
                    

    def do_draw(self, screen):
        screen.fill((self.config_window['bg_color']['r'], self.config_window['bg_color']['g'], self.config_window['bg_color']['b']))
        system_render_stars(self.ecs_world, screen)
        system_rendering(self.ecs_world, screen)
        system_render_lives(self.ecs_world, screen, self._game_engine.lives)
        system_render_flags(self.ecs_world, screen, self.level, self.config_interface)    
        system_render_text(self.ecs_world, screen)
        pygame.display.flip()

    def do_clean(self):
        self.is_paused = False
        all_entities = list(self.ecs_world._entities.keys())
        entities_to_delete = [self.spawner_entity, self.ready_text_entity, self.level_text_entity]
        for entity in all_entities:
            if entity in entities_to_delete:
                self.ecs_world.delete_entity(entity)

    def do_action(self, action: CInputCommand):
        if action.name == "PLAYER_LEFT_kl" or action.name == "PLAYER_LEFT_a" or action.name == "PLAYER_RIGHT_d" or action.name == "PLAYER_RIGHT_kr":
            if action.phase == CommandPhase.START:
                self.active_keys.add(action.name)
            elif action.phase == CommandPhase.END:
                self.active_keys.discard(action.name)
            if {"PLAYER_LEFT_kl"} & self.active_keys and not {"PLAYER_LEFT_a", "PLAYER_RIGHT_kr", "PLAYER_RIGHT_d"} & self.active_keys:
                self._player_c_velocity.velocity.x = -self.config_player["input_velocity"]
            elif {"PLAYER_LEFT_a"} & self.active_keys and not {"PLAYER_LEFT_kl", "PLAYER_RIGHT_kr", "PLAYER_RIGHT_d"} & self.active_keys:
                self._player_c_velocity.velocity.x = -self.config_player["input_velocity"]
            elif {"PLAYER_RIGHT_d"} & self.active_keys and not {"PLAYER_LEFT_kl", "PLAYER_RIGHT_kr", "PLAYER_LEFT_a"} & self.active_keys:
                self._player_c_velocity.velocity.x = self.config_player["input_velocity"]
            elif {"PLAYER_RIGHT_kr"} & self.active_keys and not {"PLAYER_LEFT_kl", "PLAYER_RIGHT_d", "PLAYER_LEFT_a"} & self.active_keys:
                self._player_c_velocity.velocity.x = self.config_player["input_velocity"]
            elif {"PLAYER_RIGHT_kr"} & self.active_keys and {"PLAYER_RIGHT_d"} & self.active_keys and not {"PLAYER_LEFT_kl", "PLAYER_LEFT_a"} & self.active_keys:
                self._player_c_velocity.velocity.x = self.config_player["input_velocity"]
            elif {"PLAYER_LEFT_kl"} & self.active_keys and {"PLAYER_LEFT_a"} & self.active_keys and not {"PLAYER_RIGHT_kr", "PLAYER_RIGHT_d"} & self.active_keys:
                self._player_c_velocity.velocity.x = -self.config_player["input_velocity"]
            else:
                self._player_c_velocity.velocity.x = 0
        elif action.name == "PLAYER_FIRE":
            num_components = len(self.ecs_world.get_components(CTagBullet))
            if num_components != 0:
                bullet_tag = self.ecs_world.component_for_entity(self._bullet_entity, CTagBullet)
                if num_components == self.max_bullets and bullet_tag.active == False:
                    if action.phase == CommandPhase.START:
                        bullet_tag.active = True
                        self._bullet_c_v = self.ecs_world.component_for_entity(self._bullet_entity, CVelocity)
                        direction = pygame.math.Vector2(0, -1)
                        direction = direction.normalize()
                        self._bullet_c_v.velocity = direction*self.config_bullet["velocity"]
                        ServiceLocator.sounds_service.play(self.config_bullet["sound"])

    def update_global_score(self, score):
        self.global_score += score

    
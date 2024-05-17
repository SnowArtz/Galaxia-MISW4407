import esper
import pygame

from src.create.prefab_creator import create_text
from src.ecs.components.c_static_image import CStaticImage
from src.ecs.components.c_text import CText
from src.ecs.components.tags.c_tag_flag import CTagFlag


def system_render_flags(world: esper.World, screen: pygame.Surface, level_flags: int, config_interface: dict):
    for ent, (image, flag) in world.get_components(CStaticImage, CTagFlag):
        if level_flags < 6:
            for i in range(level_flags):
                position_x = image.start_position[0] + i * (image.image.get_width() - 3)
                position_y = image.start_position[1]
                screen.blit(image.image, (position_x, position_y))
        else:
            position_x = image.start_position[0]
            position_y = image.start_position[1]
            screen.blit(image.image, (position_x, position_y))
            
            # Configura el mensaje para mostrar el número de banderas
            number_text = f"{level_flags:02}"
            config_text = {
                "content": number_text,
                "font": "assets/fnt/PressStart2P.ttf",
                "size": 8,
                "color": "normal_text_color",  # Usa un color definido en config_interface
                "position": {
                    "x": position_x + image.image.get_width() ,  # Ajusta este desplazamiento si es necesario
                    "y": 28
                }
            }
            
            # Usa create_text para mostrar el número
            font_entity = create_text(world, config_text, config_interface)
            text_comp = world.component_for_entity(font_entity, CText)
            screen.blit(text_comp.font.render(text_comp.text, True, text_comp.color), text_comp.position)

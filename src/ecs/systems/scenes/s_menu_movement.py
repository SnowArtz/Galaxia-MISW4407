import esper

from src.ecs.components.c_static_image import CStaticImage
from src.ecs.components.c_text import CText
from src.ecs.components.c_transform import CTransform

def system_menu_movement(world: esper.World, delta_time:float) -> None:
    text_components = world.get_components(CTransform, CText)
    for ent, (transform, text) in text_components:
        if  transform.position.y > text.position.y:
            transform.position.y += -70 * delta_time
        else:
            transform.position.y = text.position.y
    image_components = world.get_components(CStaticImage, CTransform)
    for ent, (image, transform) in image_components:
        if not image.already_in_final_position and transform.position.y > image.start_position.y:
            transform.position.y += -70 * delta_time
        if transform.position.y <= image.start_position.y:
            image.already_in_final_position = True
            transform.position.y = image.start_position.y
            transform.position.x = image.start_position.x
 
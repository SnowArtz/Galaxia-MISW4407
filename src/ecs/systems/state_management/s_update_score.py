from src.ecs.components.c_text import CText
from src.ecs.components.c_transform import CTransform

def system_update_score(world, global_score, score_text_entity, config_interface):
    if score_text_entity is not None:
        score_text_component = world.component_for_entity(score_text_entity, CText)
        score_transform_component = world.component_for_entity(score_text_entity, CTransform)
        new_score_text = f"{global_score:02d}"
        score_text_component.text = new_score_text
        original_position_x = config_interface["SCORE_P1"]["position"]["x"]
        digit_width = 10 
        if len(new_score_text) > 2:
            adjustment = (len(new_score_text) - 2) * digit_width
            score_transform_component.position.x = original_position_x - adjustment
        else:
            score_transform_component.position.x = original_position_x


import json
import os
from src.ecs.components.c_text import CText
from pathlib import Path

def system_update_high_score(world, global_score, config_texts, high_score_text_entity):
    current_high_score = int(config_texts["HIGH_SCORE_VALUE"]["content"])
    if global_score > current_high_score:
        config_texts["HIGH_SCORE_VALUE"]["content"] = str(global_score)
        _save_configurations(config_texts)
        if high_score_text_entity:
            high_score_text_component = world.component_for_entity(high_score_text_entity, CText)
            high_score_text_component.text = f"{global_score:02d}"

def _save_configurations(config_texts):
    current_file_path = Path(__file__)
    base_path = current_file_path.parents[3]
    config_path = os.path.join(base_path, 'assets', 'cfg', 'texts.json')
    with open(config_path, 'w') as file:
        json.dump(config_texts, file, indent=4)



import esper
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_text import CText


def system_blinking_text(world: esper.World, delta_time: float) -> None:
    for ent, (text, blink) in world.get_components(CText, CBlink):
        blink.next_blink_time -= delta_time
        if blink.next_blink_time <= 0:
            blink.visible = not blink.visible
            blink.next_blink_time = blink.blink_rate
            if blink.visible:
                text.color.a = 255
            else:
                text.color.a = 0

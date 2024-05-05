from typing import List


class CAnimation:
    def __init__(self, animations:dict, offset:int=0) -> None:
        self.number_frames = animations["number_frames"]
        self.animations_list: List[AnimationData] = []
        for anim in animations["list"]:
            anim_data = AnimationData(anim["name"], anim["start"], anim["end"], anim["framerate"], offset)
            self.animations_list.append(anim_data)
        self.curr_anim = 0
        self.curr_anim_time = 0
        self.curr_frame = self.animations_list[self.curr_anim].start + self.animations_list[self.curr_anim].offset


class AnimationData:
    def __init__(self, name:str, start:int, end:int, framerate:float, offset:int) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate
        self.offset = offset
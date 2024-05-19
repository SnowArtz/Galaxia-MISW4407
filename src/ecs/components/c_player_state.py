import enum
import pygame

class PlayerState(enum.Enum):
    REVIVIR = 0
    ALIVE = 1
    DEAD = 2

class CPlayerState:
    def __init__(self):
        self.state = PlayerState.ALIVE

    def change_state(self, new_state: PlayerState):
        self.state = new_state

import enum
import pygame

class EnemyState(enum.Enum):
    IDLE = 0
    EMERGING = 1
    ATTACKING = 2
    RETURNING = 3

class CEnemyState:
    def __init__(self):
        self.state = EnemyState.IDLE
        self.emerge_angle = 0
        self.emerge_direction = 1
        self.sprite_angle = 0
        self.angle = 0
        self.speed = 75

    def change_state(self, new_state: EnemyState):
        self.state = new_state

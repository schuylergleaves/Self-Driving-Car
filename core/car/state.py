from enum import Enum


class State(Enum):
    RUNNING  = 1,
    CRASHED  = 2,
    FINISHED = 3,

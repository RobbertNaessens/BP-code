from enum import Enum


class MachineStatus(Enum):
    """
    Enum class to represent the different states of a machine.

    For simplification, these states are reduced to a waiting state and a running state
    """
    WAITING = 1
    RUNNING = 2

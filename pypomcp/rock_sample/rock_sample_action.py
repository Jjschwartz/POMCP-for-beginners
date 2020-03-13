import enum

from pypomcp.model import Action


NUM_BASE_ACTIONS = 5


class RobotMoveEnum(enum.IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
    SAMPLE = 4


class RockSampleAction(Action):

    def __init__(self, action_num):
        """
        Arguments
        ---------
        action_num : int
            action number
        """
        self.a_num = action_num

    def __str__(self):
        if self.a_num < NUM_BASE_ACTIONS:
            return RobotMoveEnum(self.a_num).name
        return f"CHECK_{self.a_num-NUM_BASE_ACTIONS}"

    def __hash__(self):
        return self.a_num

    def __eq__(self, other):
        return self.a_num == other.a_num

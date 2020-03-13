import enum

from pypomcp.model import Observation


NUM_MOVE_ACTIONS = 4


class RobotObsEnum(enum.Enum):
    GOOD = 0
    BAD = 1


class RockSampleObs(Observation):

    def __init__(self, obs_num):
        """
        Arguments
        ---------
        obs_num : int
            observation number
        """
        self.o_num = obs_num

    def __hash__(self):
        return self.o_num

    def __eq__(self, other):
        return self.o_num == other.o_num

    def __str__(self):
        return RobotObsEnum(self.o_num).name

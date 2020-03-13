from copy import deepcopy

from pypomcp.model import State


class RockSampleState(State):

    def __init__(self, robot_pos, rock_types):
        """
        Arguments
        ---------
        robot_pos : (int, int)
            position of rover
        rock_types : list[bools]
            list of bools where True=good, False=Bad
        """
        self.robot_pos = robot_pos
        self.rock_types = rock_types

    def rock_is_good(self, rock_idx):
        return self.rock_types[rock_idx]

    def set_rock_bad(self, rock_idx):
        self.rock_types[rock_idx] = False

    def copy(self):
        return RockSampleState(deepcopy(self.robot_pos), deepcopy(self.rock_types))

    def __str__(self):
        output = ["RockSampleState:"]
        output.append(f"  robot_pos={self.robot_pos}")
        output.append(f"  rock_types={self.rock_types}")
        return "\n".join(output)

    def __hash__(self):
        return hash(f"{self.robot_pos}_{self.rock_types}")

    def __eq__(self, other):
        return self.robot_pos == other.robot_pos and self.rock_types == other.rock_types

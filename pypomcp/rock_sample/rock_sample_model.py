import random

from pypomcp.model import POMDPModel, InitialBelief

from .rock_sample_map import RockSampleMap
from .rock_sample_state import RockSampleState
from .rock_sample_transition import RockSampleTransition
from .rock_sample_action import RockSampleAction, NUM_BASE_ACTIONS


class RockSampleModel(POMDPModel):

    def __init__(self, n, k, sensor_efficiency):
        """
        Arguments
        ---------
        n : int
            map size
        k : int
            number of rocks
        """
        assert k <= n*n
        self.n = n
        self.k = k
        self.map = self.construct_map()
        super().__init__(self.get_initial_belief(),
                         self.get_action_space(),
                         RockSampleTransition(n, k, self.map, sensor_efficiency))

    def get_action_space(self):
        """Get the action space for the problem """
        action_space = []
        for i in range(NUM_BASE_ACTIONS+self.k):
            a = RockSampleAction(i)
            action_space.append(a)
        return action_space

    def construct_map(self):
        """Construct the problem environment """
        robot_pos = (self.n//2, 0)
        rock_pos = []
        pos_added = set()
        while len(rock_pos) < self.k:
            pos = (random.randint(0, self.n-1), random.randint(0, self.n-1))
            if pos not in pos_added:
                rock_pos.append(pos)
                pos_added.add(pos)
        return RockSampleMap(self.n, robot_pos, rock_pos)

    def get_initial_belief(self):
        """Get the initial belief for problem """
        def init_belief_fn():
            rock_types = [random.random() > 0.5 for i in range(self.k)]
            return RockSampleState(self.map.init_robot_pos, rock_types)
        return InitialBelief(init_belief_fn)

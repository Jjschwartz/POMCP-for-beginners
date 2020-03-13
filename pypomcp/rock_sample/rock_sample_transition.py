import math
import random

from pypomcp.model import Transition

from .rock_sample_obs import RobotObsEnum, RockSampleObs
from .rock_sample_action import RobotMoveEnum, NUM_BASE_ACTIONS


class RockSampleTransition(Transition):

    def __init__(self, n, k, map, sensor_efficiency=0.9):
        self.n = n
        self.k = k
        self.map = map
        self.sensor_efficiency = sensor_efficiency

    def step(self, s, a):
        """Perform a step."""
        next_s = self.get_next_state(s, a)
        o = self.get_obs(s, a, next_s)
        r = self.get_reward(s, a, next_s)
        d = self.is_terminal(next_s)
        return next_s, o, r, d

    def get_next_state(self, s, a):
        # print(str(a))
        if a.a_num >= NUM_BASE_ACTIONS:
            # check action, so nothing to do
            # print(str(a))
            # print("Check, next_s=s")
            return s
        if a.a_num == RobotMoveEnum.SAMPLE:
            if not self.map.robot_at_rock(s.robot_pos):
                # print("Sample, robot not at rock, next_s=s")
                return s
            rock_num = self.map.get_rock_at_robot_pos(s.robot_pos)
            if not s.rock_is_good(rock_num):
                # print("Sample, robot at rock, rock already bad, next_s=s")
                return s
            next_s = s.copy()
            next_s.set_rock_bad(rock_num)
            # print("Sample, robot at rock, rock good, rock now bad")
            return next_s
        if a.a_num == RobotMoveEnum.NORTH:
            if s.robot_pos[0] == self.n-1:
                # print("North, robot at top, next_s=s")
                return s
            # print("North, robot moved down one")
            new_pos = (s.robot_pos[0]+1, s.robot_pos[1])
        elif a.a_num == RobotMoveEnum.SOUTH:
            if s.robot_pos[0] == 0:
                # print("South, robot at bottom, next_s=s")
                return s
            # print("South, robot moved down")
            new_pos = (s.robot_pos[0]-1, s.robot_pos[1])
        elif a.a_num == RobotMoveEnum.EAST:
            if s.robot_pos[1] == 0:
                # print("East, robot at left edge, next_s=s")
                return s
            # print("East, robot at moved left")
            new_pos = (s.robot_pos[0], s.robot_pos[1]-1)
        else:
            # print("West, robot moved west")
            new_pos = (s.robot_pos[0], s.robot_pos[1]+1)
        next_s = s.copy()
        next_s.robot_pos = new_pos
        return next_s

    def get_obs(self, s, a, next_s):
        # print(a)
        if a.a_num == RobotMoveEnum.SAMPLE:
            if not self.map.robot_at_rock(s.robot_pos):
                # print("Sample, robot not at rock r=0")
                # return default
                return RockSampleObs(RobotObsEnum.GOOD)
            rock_num = self.map.get_rock_at_robot_pos(s.robot_pos)
            if s.rock_is_good(rock_num):
                # print("Sample, robot at good rock r=10")
                return RockSampleObs(RobotObsEnum.GOOD)
            return RockSampleObs(RobotObsEnum.BAD)
        if a.a_num < NUM_BASE_ACTIONS:
            # print("Move Action, return default obs")
            return RockSampleObs(RobotObsEnum.GOOD)
        dist = self.map.get_distance_to_rock(s.robot_pos, a.a_num-NUM_BASE_ACTIONS)
        # print(f"Dist to rock = {dist}")
        obs_prob = max(0.5, math.pow(self.sensor_efficiency, dist))
        # print(f"Obs prob = {obs_prob}")
        rock_good = s.rock_is_good(a.a_num-NUM_BASE_ACTIONS)
        if random.random() < obs_prob:
            # print("Observation correct")
            obs = RobotObsEnum.GOOD if rock_good else RobotObsEnum.BAD
        else:
            # print("Observation incorrect")
            obs = RobotObsEnum.BAD if rock_good else RobotObsEnum.GOOD
        return RockSampleObs(obs)

    def get_reward(self, s, a, next_s):
        if a.a_num == RobotMoveEnum.SAMPLE:
            if not self.map.robot_at_rock(s.robot_pos):
                # print("Sample, robot not at rock r=0")
                return 0
            rock_num = self.map.get_rock_at_robot_pos(s.robot_pos)
            if s.rock_is_good(rock_num):
                # print("Sample, robot at good rock r=10")
                return 10
            # print("Sample, robot at bad rock r=-10")
            return -10
        # print("Other action, r=0")
        if self.is_terminal(next_s):
            # print("s is terminal r=10")
            return 10
        return 0

    def is_terminal(self, next_s):
        return next_s.robot_pos[1] >= self.n

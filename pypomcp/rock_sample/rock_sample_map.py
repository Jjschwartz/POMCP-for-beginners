import math


class RockSampleMap:

    def __init__(self, n, init_robot_pos, rock_pos):
        self.n = n
        self.init_robot_pos = init_robot_pos
        self.rock_pos = rock_pos

    def robot_at_rock(self, robot_pos):
        return robot_pos in self.rock_pos

    def get_rock_at_robot_pos(self, robot_pos):
        try:
            return self.rock_pos.index(robot_pos)
        except ValueError:
            return None

    def get_rock_pos(self, rock_idx):
        return self.rock_pos[rock_idx]

    def get_distance_to_rock(self, robot_pos, rock_idx):
        rock_pos = self.get_rock_pos(rock_idx)
        x_dis = (robot_pos[0] - rock_pos[0])**2
        y_dis = (robot_pos[1] - rock_pos[1])**2
        return math.sqrt(x_dis+y_dis)

    def __str__(self):
        output = ["RockSampleMap:"]
        output.append(f"  init_robot_pos = {self.init_robot_pos}")
        output.append(f"  Rock_pos = {self.rock_pos}")
        return "\n".join(output)

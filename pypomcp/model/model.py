

class POMDPModel:

    def __init__(self, initial_belief, action_space, transition):
        """Expects:
        initial_belief : Belief
        action_space : list of Action
        transition : Transition
        """
        self.b0 = initial_belief
        self.A = action_space
        self.G = transition

    def step(self, s, a):
        return self.G.step(s, a)

    def is_terminal(self, s):
        return self.G.is_terminal(s)

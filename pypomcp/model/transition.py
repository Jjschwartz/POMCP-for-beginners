

class Transition:
    """An abstract transition model """

    def step(self, s, a):
        """Perform a step.

        Arguments
        ---------
        s : State
            the state where action is being performed
        a : Action
            the action being performed

        Returns
        -------
        next_s : State
            the next state
        o : Observation
            the observation
        r : float
            the reward for performing action a in state s
        d : bool
            whether the next_s is terminal or not
        """
        raise NotImplementedError

import random


class Belief:
    """An abstract belief class """

    def sample(self):
        """Returns a state from the belief """
        raise NotImplementedError

    def sample_k(self, k):
        """Sample k states from the belief """
        raise NotImplementedError

    def is_depleted(self):
        """Returns true if belief is depleted, so cannot be sampled """
        raise NotImplementedError

    def size(self):
        """Returns the size of the belief, or None if not applicable """
        raise NotImplementedError


class InitialBelief(Belief):
    """The initial belief for a problem """

    def __init__(self, initial_belief_fn):
        """Expects initial_belief_fn returns a random initial
        state when called
        """
        self.I_fn = initial_belief_fn

    def sample(self):
        return self.I_fn()

    def sample_k(self, k):
        samples = []
        for i in range(k):
            samples.append(self.sample())
        return samples

    def is_depleted(self):
        return False

    def size(self):
        return None


class ParticleBelief(Belief):
    """A belief represented by state particles """

    def __init__(self):
        super().__init__()
        self.particles = list()

    def sample(self):
        return random.choice(self.particles)

    def sample_k(self, k):
        return random.choices(self.particles, k=k)

    def add_particle(self, s):
        self.particles.append(s)

    def add_particles(self, ss):
        self.particles.extend(ss)

    def is_depleted(self):
        return len(self.particles) == 0

    def size(self):
        return len(self.particles)

    def get_dist(self):
        unique_particles = list(set(self.particles))
        dist = []
        for p in unique_particles:
            dist.append(self.particles.count(p))
        return dist

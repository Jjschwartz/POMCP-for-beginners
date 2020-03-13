import time
import math
import random

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

from .node import Node
from pypomcp.model import ParticleBelief


class SearchTree:
    """A search tree in the POMCP algorithm """

    def __init__(self, model, c=10, gamma=0.95, epsilon=0.01, K=100):
        self.M = model
        self.c = c
        self.gamma = gamma
        self.epsilon = epsilon
        self.K = K
        self.actual_history = []
        self.init_root()

    def init_root(self):
        self.root = Node(None, None, ParticleBelief())
        particles = self.M.b0.sample_k(self.K)
        self.root.belief.add_particles(particles)

    def set_root(self, node):
        """Set the root of tree to be the given node """
        self.root = node

    def update(self, a, o):
        """Update/prune tree given real action and observation """
        # print(f"Tree update with:\na={a}\no={o}")
        self.actual_history.append((a, o))
        a_node = None
        for child in self.root.children:
            if child.h == a:
                a_node = child
                break
        o_node = self.get_obs_node(a_node, o)
        self.invigorate_belief(self.root, o_node, a, o)
        self.set_root(o_node)

    def invigorate_belief(self, parent, child, a, o):
        """Fill child belief with particles """
        child_size = child.belief.size()
        while child_size < self.K:
            s = parent.belief.sample()
            next_s, sampled_o, r, d = self.M.step(s, a)
            if sampled_o == o:
                child.belief.add_particle(next_s)
                child_size += 1

    def search(self, timeout):
        """Run search to get next action """
        start_time = time.time()

        if len(self.root.children) == 0:
            self.expand(self.root)

        while time.time() - start_time < timeout:
            s = self.root.belief.sample()
            self.simulate(s, self.root, 0)
        return self.greedy_action(self.root)

    def simulate(self, s, node, d):
        """Simulate a step in search tree """
        if self.gamma**d < self.epsilon:
            return 0

        if len(node.children) == 0:
            self.expand(node)
            roll_r = self.rollout(s, d)
            # print(rol_r)
            return roll_r

        a, a_node = self.uct_action(node)
        next_s, o, r, d = self.M.step(s, a)
        o_node = self.get_obs_node(a_node, o)

        if d:
            sim_r = r
        else:
            sim_r = r + self.gamma*self.simulate(next_s, o_node, d+1)

        if node.h is not None:
            node.belief.add_particle(s)
        node.n += 1
        a_node.n += 1
        a_node.v += (sim_r-a_node.v)/a_node.n
        return sim_r

    def rollout(self, s, d):
        """Run a random rollout """
        if self.gamma**d < self.epsilon:
            # print(f"max rollout depth, {d}, reached")
            return 0
        a = self.random_action()
        next_s, o, r, done = self.M.step(s, a)
        if done:
            # print("rollout terminal reached")
            return r
        return r + self.gamma*self.rollout(next_s, d+1)

    def expand(self, parent):
        """Expands a node, adding children for each action in problem """
        for a in self.M.A:
            new_node = Node(a, parent, ParticleBelief())
            parent.children.append(new_node)

    def get_obs_node(self, a_node, o):
        """Get the observation node from given action node, adding a new node if necessary """
        for child in a_node.children:
            if child.h == o:
                return child

        o_node = Node(o, a_node, ParticleBelief())
        a_node.children.append(o_node)
        return o_node

    def greedy_action(self, node):
        """Get action with largest value """
        max_a, max_v = None, None
        for child in node.children:
            if max_v is None or child.v > max_v:
                max_v = child.v
                max_a = child.h
        return max_a

    def uct_action(self, node):
        """Get action based on UCT action selection """
        if node.n == 0:
            child = random.choice(node.children)
            return child.h, child

        log_n = math.log(node.n)
        max_a, max_v, max_child = None, None, None
        for child in node.children:
            if child.n == 0:
                return child.h, child
            child_uct_v = child.v + self.c*math.sqrt(log_n/child.n)
            # print("uct", child.v, child.n, log_n, child_v)
            if max_v is None or child_uct_v > max_v:
                max_v = child_uct_v
                max_a = child.h
                max_child = child
        return max_a, max_child

    def random_action(self, node=None):
        """Get action uniformly at random """
        return random.sample(self.M.A, 1)[0]

    def display(self, depth_limit=3):
        """Render a networkx plot of the tree """
        G = nx.DiGraph()
        G.add_node(self.root, v=self.root.v, n=self.root.n, h=self.root.h)
        self.recursively_build_tree(G, self.root, 0, depth_limit)

        pos = graphviz_layout(G, prog='dot')
        nx.draw(G, pos, with_labels=True)
        plt.show()

    def recursively_build_tree(self, G, parent, d, depth_limit):
        """Recursively adds nodes to the graph """
        if len(parent.children) == 0 or d == depth_limit:
            return

        for child in parent.children:
            G.add_node(child, v=child.v, n=child.n, h=child.h)
            G.add_edge(parent, child)
            self.recursively_build_tree(G, child, d+1, depth_limit)

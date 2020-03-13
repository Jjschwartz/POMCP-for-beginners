

class Node:
    """A Node in the search tree """

    # class variable
    node_count = 0

    def __init__(self, h, parent, belief, v_init=0, n_init=0):
        self.id = Node.node_count
        Node.node_count += 1
        self.parent = parent
        self.h = h
        self.v = v_init
        self.n = n_init
        self.belief = belief
        self.children = list()

    def __str__(self):
        output = f"N{self.id}\nh={self.h}\nv={self.v:.2f}\nn={self.n}"
        return output

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

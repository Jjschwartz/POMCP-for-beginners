from pypomcp.tree.tree import SearchTree


class POMCP:

    def __init__(self, model):
        self.M = model
        self.T = SearchTree(model)

    def search(self, timeout):
        """Run search to get next action """
        return self.T.search(timeout)

    def update(self, a, o):
        """Update/prune tree given real action and observation """
        self.T.update(a, o)

    def display(self):
        """Render the tree, from the current root """
        self.T.display()

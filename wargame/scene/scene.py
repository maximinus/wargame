from wargame.nodes import Node

# a scene is a collection of nodes that we draw


class Scene(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def render(self, surface):
        for node in self.nodes:
            node.render(surface)

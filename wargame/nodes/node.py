class Node:
    def render(self, surface):
        # draw this node to this surface
        pass

    @property
    def container(self):
        # does this node contain children?
        return False

    @property
    def children(self):
        # return the children of this node
        return []

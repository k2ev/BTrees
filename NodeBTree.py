class NodeBTree:
    __slots__ = ["_item", "_left", "_right"]

    def __init__(self, item=None, left=None, right=None):
        self.item = item
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.item)

    def __lt__(self, other):
        return True if self.item < other.item else False

    def __eq__(self, other):
        return True if self.item == other.item else False

    def __ne__(self, other):
        return True if self.item != other.item else False

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item
        return

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, node):
        assert node is None or isinstance(node, NodeBTree)
        self._left = node

    @right.setter
    def right(self, node):
        assert node is None or isinstance(node, NodeBTree)
        self._right = node

    def is_leaf(self):
        return True if self.left is None and self.right is None else False

    def children(self):
        yield self.left
        yield self.right
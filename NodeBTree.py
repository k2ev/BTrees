class NodeBTree:
    __slots__ = ["_item", "_left", "_right"]

    def __init__(self, item=None, left=None, right=None):
        self._item = item
        self._left = left
        self._right = right

    def is_leaf(self):
        return True if self._left is None and self._right is None else False

    def __lt__(self, other):
        return True if self._item < other._item else False

    def __eq__(self, other):
        return True if self._item == other._item else False

    def __ne__(self, other):
        return True if self._item != other._item else False

    def get_item(self):
        return self._item

    def set_item(self, item):
        self._item = item
        return

    def get_left(self):
        return self._left

    def get_right(self):
        return self._right

    def set_left(self, left):
        self._left = left

    def set_right(self, right):
        self._right = right

    def __str__(self):
        return " " + str(self._item)





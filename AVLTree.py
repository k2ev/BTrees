from BST import BstRegular
from constants import *

class BstAVL(BstRegular):
    node_type = "AVL"

    def __init__(self, node=None):
        super().__init__(node)

    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right)

    def _fix_height(self, node):
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return

    def insert(self, val):
        node = super().insert(val)
        self._balance(node)
        return node

    def _rotate_right(self, node):
        left_child = node.left
        super()._rotate_right(node)
        self._fix_height(node)
        self._fix_height(left_child)

    def _rotate_left(self, node):
        right_child = node.right
        super()._rotate_left(node)
        self._fix_height(node)
        self._fix_height(right_child)

    def _balance(self, node):
        if node:
            current = node.parent
            if current:
                self._fix_height(current)
                balance_factor = self._get_balance(current)

                if balance_factor > 1:
                    if self._get_balance(current.left) < 0:
                        self._rotate_left(current.left)
                    self._rotate_right(current)

                if balance_factor < -1:
                    if self._get_balance(current.right) > 0:
                        self._rotate_right(current.right)
                    self._rotate_left(current)

            self._balance(current)
        return








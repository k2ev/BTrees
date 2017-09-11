from BST import BstRegular
from constants import *

class BstSplay(BstRegular):

    node_type = "splay"

    def __init__(self, node=None):
        super().__init__(node)

    def contains(self, val, current=sentinel):
        node_contains_info = self._contains_with_info(val, current)
        node_found = node_contains_info.get("flag", False)
        node_prior = node_contains_info.get("prior", None)
        node = node_contains_info.get("node", None)
        if node_found:
            self._splay(node)
            return node
        else:
            if node_prior:
                self._splay(node_prior)
            return None

    def _splay(self, node):
        if node is None or node is self.root:
            return
        elif node.parent is self.root:
            if node.is_left_child():
                self._rotate_right(node.parent)  # referred to as zig
            elif node.is_right_child():
                self._rotate_left(node.parent) # referred to as zag
        elif node.parent.parent:
            if node.is_left_child() and node.parent.is_left_child():
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node.is_right_child() and node.parent.is_right_child():
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            elif node.parent.is_left_child() and node.is_right_child():
                self._rotate_left(node.parent)
                self._rotate_right(node.parent)  #node.parent has changed
            elif node.parent.is_right_child() and node.is_left_child():
                self._rotate_right(node.parent)
                self._rotate_left(node.parent)  #node.parent has changed
            self._splay(node)

    def insert(self, val):
        node = super().insert(val)
        if node:
            self._splay(node)
            return node
        else:
            return None

    def remove(self, val):
        if self.root:
            node_remove_info = self._remove_with_info(val)
            node_remove_flag = node_remove_info.get("flag", False)
            node_prior = node_remove_info.get("prior", None)

            if node_remove_flag:
                self._splay(node_prior.parent)

            return node_remove_flag


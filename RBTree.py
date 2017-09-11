from BST import BstRegular
import constants


class BstRB(BstRegular):

    node_type = "RB"

    def __init__(self, node=None):
        super().__init__(node)

    def insert(self, val):
        node = self.get_node(val)
        node = super().insert(node)
        if node:
            node.color = constants.color_red
            self.rebalance(node)
        return node

    def rebalance(self, node):
        if node is self.root:  # node is root
            node.color = constants.color_black
        elif node.parent is self.root:   # node parent is a root
            assert node.parent.color is constants.color_black
        elif node.parent.color is constants.color_black:
            pass
        elif node.get_uncle() and node.get_uncle().color is constants.color_red: # node uncle is red in color
            node.parent.color = constants.color_black
            node.get_uncle().color = constants.color_black
            node.get_grandparent().color = constants.color_red
            self.rebalance(node.get_grandparent())
        else:  # uncle black in color
            if node.parent.is_left_child() and node.is_left_child():
                self._right_rotate_swap(node)
            elif node.parent.is_left_child() and node.is_right_child():
                self._left_right_rotate_swap(node)
            elif node.parent.is_right_child() and node.is_right_child():
                self._left_rotate_swap(node)
            elif node.parent.is_right_child() and node.is_left_child():
                self._right_left_rotate_swap(node)
        return

    def _swap_colors(self, node_a, node_b):
        if node_a and node_b:
            temp = node_a.color
            node_a.color = node_b.color
            node_b.color = temp
        elif node_a:
            node_a.color = constants.color_black
        elif node_b:
            node_b.color = constants.color_black
        return

    # right_right_case
    def _left_rotate_swap(self, node):
        grand_parent = node.get_grandparent()
        self._rotate_left(grand_parent)
        self._swap_colors(grand_parent, grand_parent.parent)
        return

    # left_left case
    def _right_rotate_swap(self, node):
        grand_parent = node.get_grandparent()
        self._rotate_right(grand_parent)
        self._swap_colors(grand_parent, grand_parent.parent)
        return

    # left right case
    def _left_right_rotate_swap(self, node):
        parent = node.parent
        grand_parent = node.get_grandparent()
        self._rotate_left(parent)
        self._rotate_right(grand_parent)
        self._swap_colors(grand_parent, grand_parent.parent)
        return

    # right left case
    def _right_left_rotate_swap(self, node):
        parent = node.parent
        grand_parent = node.get_grandparent()
        self._rotate_right(parent)
        self._rotate_left(grand_parent)
        self._swap_colors(grand_parent, grand_parent.parent)
        return

    def remove(self, val):
        node = self.val_to_node(val)
        node = super().remove(node)

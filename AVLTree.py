from BST import BstRegular

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
        if node.parent:
            self._balance(node.parent)
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

    def _balance(self, node, recurse=False):
            if node:
                self._fix_height(node)
                balance_factor = self._get_balance(node)
                balanced_node = False if abs(balance_factor) > 1 else True

                if not balanced_node:
                    if balance_factor > 1:
                        if self._get_balance(node.left) < 0:
                            self._rotate_left(node.left)
                        self._rotate_right(node)

                    if balance_factor < -1:
                        if self._get_balance(node.right) > 0:
                            self._rotate_right(node.right)
                        self._rotate_left(node)

                if recurse or balanced_node:
                    self._balance(node.parent) if node.parent else None
            return

    def remove(self, val):
        if self.root:
            node_remove_info = self._remove_with_info(val)
            node_remove_flag = node_remove_info.get("flag", False)
            node_prior = node_remove_info.get("prior", None)

            if node_remove_flag:
                self._balance(node_prior, True) # apply balancing all the way to root

            return node_remove_flag






from BTree import BTreeLinked
from constants import sentinel


class BST(BTreeLinked):

    def __init__(self, node=None):
        super().__init__(node)
        # use as a second pointer to store parent node as and when needed for any node
        # _parent_node as of any time may not give anything meaningful
        # however, def such as contains and min_value_node etc set it to be some value
        # it should be copied over immediately thereafter else value may get corrupted by some other setter method
        # A more memory expensive approach would have been to have nodes that have pointer to parent
        self._parent_node = None

    @property
    def parent_node(self):
        return self._parent_node

    @parent_node.setter
    def parent_node(self, node):
        self._parent_node = node
        return

    def contains(self, node, current=sentinel):
        node = self.val_to_node(node)
        if current is sentinel:
            current = self.root
            self.parent_node = None  # a second pointer is being maintained as BTreeNode doesnt have a parent pointer

        if current is not None:
            if current.item == node.item:
                return current
            elif node.item < current.item:
                self.parent_node = current
                return self.contains(node, current.left)
            elif node.item > current.item:
                self.parent_node = current
                return self.contains(node, current.right)
        else:
            return None

    def min_value_node(self, current=sentinel):
        current = self.get_root_default(current)
        self.parent_node = None
        while current.left is not None:
            self.parent_node = current
            current = current.left
        return current

    def max_value_node(self, current=sentinel):
        current = self.get_root_default(current)
        self.parent_node = None
        while current.right is not None:
            self.parent_node = current
            current = current.right
        return current

    def insert(self, val):
        node = self.val_to_node(val)
        current = self.root
        prior = None

        while current is not None:
            prior = current
            if node.item <= current.item:
                current = current.left
            elif node.item > current.item:
                current = current.right

        if prior is not None:
            if node.item <= prior.item:
                prior.left = node
            else:
                prior.right = node

            return True
        else:
            return False

    def remove(self, val):
        node = self.val_to_node(val)
        node = self.contains(node)
        node_parent = self.parent_node

        if node is not None:
            if node.right:
                min_node = self.min_value_node(node.right)
                min_node_parent = self.parent_node
                if min_node_parent.left is node:
                    min_node_parent.left = None
                else:
                    min_node_parent.right = None
                node.item = min_node.item
            elif node.left:
                node.item = node.left.item
                node.left = None
            else:
                if node_parent:
                    if node_parent.left is node:
                        node_parent.left = None
                    else:
                        node_parent.right = None
                else:
                    self.root = None   # if it doesnt have a left or right node nor a parent then its a root node

            return True
        else:
            return False

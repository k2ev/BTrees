from BTree import *
from constants import sentinel


class BstRegular(BTreeLinked):

    node_type = "regular"

    def __init__(self, node=None):
        super().__init__(node)

    def _contains_no_frills(self, val, current=sentinel):
        node_contains_info = self._contains_with_info(val, current)
        node_found = node_contains_info.get("flag", False)
        node = node_contains_info.get("node", None)
        if node_found:
            return node
        else:
            return None

    def _contains_with_info(self, node, current=sentinel, prior=sentinel):
        node = self.get_node(node)
        if current is sentinel:
            current = self.root
            prior = None

        if current is not None:
            if current == node:
                return dict(flag=True, node=current, prior=current.parent)
            elif node< current:
                prior = current
                return self._contains_with_info(node, current.left, prior)
            elif node > current:
                prior = current
                return self._contains_with_info(node, current.right, prior)
        else:
            return dict(flag=False, node=node, prior=prior)

    def contains(self, val, current=sentinel):
        return self._contains_no_frills(val, current)

    def min_value_node(self, current=sentinel):
        current = self.get_root_default(current)
        while current.left is not None:
            current = current.left
        return current

    def max_value_node(self, current=sentinel):
        current = self.get_root_default(current)
        self.parent_node = None
        while current.right is not None:
            current = current.right
        return current

    def insert(self, val):
        node = self.get_node(val)
        current = self.root
        prior = None

        if current is None:
            self.root = node
            return node
        else:
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
                node.parent = prior

                return node
            else:
                return None

    def remove(self, val):
        node_remove_info = self._remove_with_info(val)
        node_remove_flag = node_remove_info.get("flag", False)
        return node_remove_flag

    def _remove_with_info(self, val):
        node = self.get_node(val)
        node = self._contains_no_frills(node)
        flag, prior = False, None #  prior is parent of deleted node

        if self.root and node:
            if node is self.root:
                self.root = None
                prior = None
            elif node.is_leaf():
                if node.is_left_child():
                    node.parent.left = None
                    prior = node.parent
                    node.parent = None
                else:
                    node.parent.right = None
                    prior = node.parent
                    node.parent = None
            elif node.has_one_child() and node.left:
                prior = node.left
                node.left.parent = node.parent
                if node.is_left_child():
                    node.parent.left = prior
                else:
                    node.parent.right = prior
            elif node.right:
                if node.right.left:
                    min_node = self.min_value_node(node.right)
                    node.item = min_node.item
                    prior = min_node.parent
                    if min_node.is_left_child():
                        min_node.parent.left = None
                    else:
                        min_node.parent.right = None
                else:
                    prior = node.right
                    node.right.parent = node.parent
                    if node.is_left_child():
                        node.parent.left = prior
                    else:
                        node.parent.right = prior
            flag = True

            return dict(flag=flag, node=node, prior=prior)

    def _rotate(self, node, dir = "left"):
        grand_parent = node
        grand_parent_is_right_child = grand_parent.is_right_child()
        parent = node.right if dir == "left" else node.left
        great_grand_parent = grand_parent.parent

        ## left rotate g, making p as parent of g

        # p in g position with ggp as parent
        if great_grand_parent:
            parent.parent = great_grand_parent
            if grand_parent_is_right_child:
                great_grand_parent.right = parent
            else:
                great_grand_parent.left = parent
        else:
            self.root = parent
            parent.parent = None

        # put g as a right child of p
        grand_parent.parent = parent
        if dir == "left":
            branch_to_move = parent.left
            grand_parent.right = parent.left
            parent.left = grand_parent
        else:
            branch_to_move = parent.right
            grand_parent.left = parent.right
            parent.right = grand_parent

        if branch_to_move:
            branch_to_move.parent = grand_parent
        return

    def _rotate_left(self, node):
        return self._rotate(node, dir="left")

    def _rotate_right(self, node):
        return self._rotate(node, dir="right")


class BstSimple(BTreeLinked):
    # doesnt provide rotate method

    node_type = "simple"

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
        node = self.get_node(node)
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
        node = self.get_node(val)
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

            return node
        else:
            return None

    def remove(self, val):
        node = self.get_node(val)
        node = self.contains(node)
        node_parent = self.parent_node

        if node is not None:
            if node.right:
                min_node = self.min_value_node(node.right)
                if min_node is node.right:
                    min_node_parent = node
                else:
                    min_node_parent = self.parent_node
                if min_node_parent.left is not None and min_node_parent.left is node:
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

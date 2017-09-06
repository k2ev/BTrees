from NodeBTree import NodeBTree
from constants import sentinel


class BTreeLinked:
    ###################
    # Class Variables #
    ###################
    traverse_type = "_bft_iterative"

    ###################
    # Magic Methods   #
    ###################

    def __init__(self, root=None):
        root = self.val_to_node(root)
        self.root = root

    def __str__(self):
        current = self.root
        queue, level, num_nodes_current_level, num_nodes_next_level = [current], 0, 1, 0
        height = self.height()
        level_length= 2*(2**height-1) - 2*(2**(height-1))
        node_space_length = 2 + 2 * 2**height
        start_length = level_length+2
        s = ""
        # this is a modified form of bft for pretty printing. Even null nodes are inserted into queue
        while level < height:
            level_length = level_length//2 - 1
            node_space_length = node_space_length//2 + 1
            start_length = level_length + 2
            current = queue.pop(0)  # used as a queue
            num_nodes_current_level -= 1
            if num_nodes_next_level == 0:
                width = int(start_length)
            else:
                width = int(node_space_length)
            if current and current.item is not None and current.left and current.left.item is not None:
                fill = '_'
            else:
                fill = ' '
            s += '{:{fill}{align}{width}}'.format("", fill=fill, align='>', width=width)
            width = level_length + 2
            if current and current.item is not None and current.right and current.right.item is not None:
                fill = '_'
            else:
                fill = ' '
            s += '{:{fill}{align}{width}}'.format(str(current), fill=fill, align='>', width=width)
            width = max(width-2,0)
            fill = ' '
            s += '{:{fill}{align}{width}}'.format("", fill=fill, align='>', width=width)

            for child in current.children():
                if child is None:
                    child = NodeBTree()
                queue.append(child)
                num_nodes_next_level += 1

            if num_nodes_current_level == 0:
                s += "\n"
                level += 1
                num_nodes_current_level = num_nodes_next_level
                num_nodes_next_level = 0
                level_length = level_length//2
        return s

    def __len__(self):
        count_ = 0
        for _ in self:
            count_ += 1
        return count_

    def __iter__(self):
        return self.traverse()

    ###################
    # Public Methods  #
    ###################

    def get_left(self):
        return self.get_subtree(self.root.left)

    def get_right(self):
        return self.get_subtree(self.root.right)

    @property
    def root(self):
        return self._root
    
    @root.setter
    def root(self, node):
        assert node is None or isinstance(node, NodeBTree)
        self._root = node

    def traverse(self):
        name = self.__class__.get_traverse_method()
        fn = getattr(self, name)
        return fn()

    def get_root_default(self, node):
        return self.root if node is sentinel else node  # if node is None then its returned as None

    def height(self):
        return self._height(self._root)

    def level(self, node):
        return self._level(node, self._root)

    def distance(self, node_a, node_b):
        dist_common = self._level(node_a, node_b)  # distance from B->A assuming direct path
        if dist_common < 0:
            dist_common = self._level(node_b, node_a)  # distance from A->B assuming direct path
        if dist_common < 0:
            dist_common = self.level(node_a) + self.level(node_b) - 2 * self.level(self.common_parent(node_a, node_b))
        return dist_common

    def contains(self, node, current=sentinel):
        current = self.get_root_default(current)
        if type(node) is not NodeBTree:
            if type(node) is int or float:
                node = NodeBTree(node)
        return False if self._level(node, current) < 0 else True

    def common_parent(self, node_a, node_b):
        if self.contains(node_a, node_b):
            root = node_b
        elif self.contains(node_b, node_a):
            root = node_a
        else:
            root, queue = self.root, [self.root]
            while queue:
                current = queue.pop(0)
                if current == node_a or current == node_b:
                    break
                elif self.contains(node_a, current) and self.contains(node_b, current):
                    root = current
                    for child in current.children():
                        queue.append(child) if child else None
        return root

    def breadth(self, root=None):
        root = root or self.root
        queue, max_width = [root], 1
        while queue:
            count_ = len(queue)
            max_width = max(count_, max_width)
            while count_ > 0:
                count_ -= 1
                current = queue.pop(0)
                for child in current.children():
                    queue.append(child) if child else None
        return max_width

    def sum_max_depth(self):
        return self._sum_max_depth(self.root)

    def sum_value(self):
        sum_ = 0
        for node in self:
            sum_ += node.item
        return sum_

    ###################
    # Private Methods #
    ###################

    def _pre_order(self, current=sentinel):
        current = self.get_root_default(current)
        if current is not None:
            yield current
            yield from self._pre_order(current.left)
            yield from self._pre_order(current.right)

    def _post_order(self, current=sentinel):
        current = self.get_root_default(current)
        if current is not None:
            yield from self._post_order(current.left)
            yield from self._post_order(current.right)
            yield current

    def _in_order(self, current=sentinel):
        current = self.get_root_default(current)
        if current is not None:
            yield from self._in_order(current.left)
            yield current
            yield from self._in_order(current.right)

    def _bft_iterative(self, current=sentinel):
        current = self.get_root_default(current)
        queue = [current]
        while queue:
            current = queue.pop(0)  # used as a queue
            yield current
            for child in current.children():
                queue.append(child) if child else None

    def _pre_order_iterative(self, current=sentinel):
        current = self.get_root_default(current)
        stack = [current]
        while stack:
            current = stack.pop()
            if current:
                yield current
                stack.append(current.right) if current.right else None
                stack.append(current.left) if current.left else None

    def _in_order_iterative(self, current=sentinel):
        current = self.get_root_default(current)
        stack = [current]
        while stack:
            current = current.left
            if current:
                stack.append(current)
            else:
                right_node_insert = False
                while not right_node_insert and stack:
                    current = stack.pop()
                    yield current
                    if current.right:
                        stack.append(current.right)
                        current = current.right
                        right_node_insert = True

    def _post_order_iterative(self, current=sentinel):
        current = self.get_root_default(current)
        stack, stack_aux = [current], []
        while stack:
            current = stack.pop()
            for child in current.children():
                stack.append(child) if child else None
            stack_aux.append(current)

        while stack_aux:
            current = stack_aux.pop()
            yield current

    def _height(self, node):
        if node:
            height = max(self._height(node.left), self._height(node.right)) + 1
        else:
            height = 0
        return height

    def _level(self, node, current=sentinel):
        current = self.get_root_default(current)
        depth = -1  # not found
        if current:
            if current == node:
                depth = 0  # found
            else:
                lower_levels = max(self._level(node, current.left), self._level(node, current.right))
                depth = lower_levels + 1 if lower_levels >= 0 else -1
        return depth

    def _sum_max_depth(self, node=None):
        sum_ = 0
        if node:
            sum_ += node.item
            height_left = self._height(node.left)
            height_right = self._height(node.right)
            if height_left > height_right:
                sum_ += self._sum_max_depth(node.left)
            elif height_left < height_right:
                sum_ += self._sum_max_depth(node.right)
            else:
                sum_ += max(self._sum_max_depth(node.left), self._sum_max_depth(node.right))
        return sum_

    #################
    # Class Methods #
    #################

    @classmethod
    def get_subtree(cls, node):
        return cls(node)

    @classmethod
    def get_traverse_method(cls):
        return cls.traverse_type

    @classmethod
    def set_traverse_method(cls, name):
        allowed_methods = [
            "_pre_order",
            "_in_order",
            "_post_order",
            "_bst_iterative",
            "_pre_order_iterative",
            "_in_order_iterative",
            "_post_order_iterative"
        ]
        if name in allowed_methods:
            cls.traverse_type = name
        else:
            print(name, "is not permissible input. Allowed methods are:", allowed_methods)

    @staticmethod
    def val_to_node(val):
        if type(val) is NodeBTree:
            return val
        else:
            if type(val) is int or float:
                return NodeBTree(val)

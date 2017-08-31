from NodeBTree import NodeBTree


class BTreeLinked:
    def __init__(self, root=None):
        self._root = root

    def get_left(self):
        return BTreeLinked(self._root.get_left())

    def get_right(self):
        return BTreeLinked(self._root.get_right())

    def get_subtree(self, node):
        return BTreeLinked(node)

    def _pre_order(self, current):
        s = ""
        if current is not None:
            s += str(current)
            s += self._pre_order(current.get_left())
            s += self._pre_order(current.get_right())
        return s

    def _post_order(self, current):
        s = ""
        if current is not None:
            s += self._post_order(current.get_left())
            s += self._post_order(current.get_right())
            s += str(current)
        return s

    def _in_order(self, current):
        s = ""
        if current is not None:
            s += self._in_order(current.get_left())
            s += str(current)
            s += self._in_order(current.get_right())
        return s

    def _bft(self, current):
        s, queue = "", [current]
        while queue:
            count = len(queue)
            while count > 0:
                count -= 1
                out_node = queue.pop(0)
                s += str(out_node)
                in_left_node = out_node.get_left()
                in_right_node = out_node.get_right()
                if in_left_node is not None:
                  queue.append(out_node.get_left())
                if in_right_node is not None:
                    queue.append(out_node.get_right())
            s += "\n"
        return s

    def get_root(self):
        return self._root

    def depth(self, node):
        return self._depth(node, self._root)

    def _depth(self, node, root):
        depth = 0
        if root:
            if root == node:
                depth += 0
            else:
                d_left = self._depth(node, root.get_left())
                d_right = self._depth(node, root.get_right())
                d_max = max(d_left, d_right) + 1
                depth += d_max if d_max > 0 else -1
        else:
            depth -= 1
        return depth

    def height(self):
        return self._height(self._root)

    def _height(self, node):
        if node is not None:
            height = max(self._height(node.get_left()), self._height(node.get_right())) + 1
        else:
            height = 0
        return height

    def sum_max_depth(self):
        return self._sum_max_depth(self._root)

    def _sum_max_depth(self, node=None):
        sum_ = 0
        if node:
            sum_ += node.get_item()
            height_left = self._height(node.get_left())
            height_right = self._height(node.get_right())
            if height_left > height_right:
                sum_ += self._sum_max_depth(node.get_left())
            elif height_left < height_right:
                sum_ += self._sum_max_depth(node.get_right())
            else:
                sum_ += max(self._sum_max_depth(node.get_left()), self._sum_max_depth(node.get_right()))
        return sum_

    def diameter(self, nodeA, nodeB):
        pass

    def distance(self, nodeA, nodeB):
            dist_common = self._depth(nodeA, nodeB) # distance from B->A assuming direct path
            if dist_common < 0:
                dist_common = self._depth(nodeB, nodeA) # dustance from A->B assuming direct path
            if dist_common < 0:
                dist_common = self.depth(nodeA) + self.depth(nodeB) - 2*self.depth(self.common_parent(nodeA, nodeB))
            return dist_common

    def contains(self, node, root=None):
        root = root or self._root
        return False if self._depth(node, root) < 0 else True

    def common_parent(self, nodeA, nodeB):
        root = None
        if self.contains(nodeA, nodeB):
            root = nodeB
        elif self.contains(nodeB, nodeA):
            root = nodeA
        else:
            root, queue = self._root, [self._root]
            while queue:
                current = queue.pop(0)
                if current == nodeA or current == nodeB:
                    break
                elif self.contains(nodeA, current) and self.contains(nodeB, current):
                    root = current
                    queue.append(current.get_left()) if current.get_left() else None
                    queue.append(current.get_right()) if current.get_right() else None
        return root

    def breadth(self, root=None):
        root = root or self._root
        queue, max_width = [root], 1
        while queue:
            count_ = len(queue)
            max_width = max(count_,max_width)
            while count_ > 0:
                count_ -= 1
                current = queue.pop(0)
                if current.get_left() is not None:
                    queue.append(current.get_left())
                if current.get_right() is not None:
                    queue.append(current.get_right())
        return max_width

    def __str__(self):
        return self.traverse()

    def traverse(self, type_="bft"):
        if type_ == "pre":
            return self._pre_order(self._root)
        elif type_ == "post":
            return self._post_order(self._root)
        elif type_ == "in":
            return self._in_order(self._root)
        elif type_ == "bft":
            return self._bft(self._root)

    def __iter__(self, type = "post"):
        # iterate in a bst way
        current, stack_queue = self._root, [self._root]
        if type == "bst":
            while stack_queue:
                current = stack_queue.pop(0)  # used as a queue
                yield current
                stack_queue.append(current.get_left()) if current.get_left() else None
                stack_queue.append(current.get_right()) if current.get_right() else None
        elif type == "in":
            current = current.get_left()
            while stack_queue:
                if current:
                    stack_queue.append(current)
                    current = current.get_left()
                else:
                    current = stack_queue.pop()
                    yield current
                    current = current.get_right()
                    if current and current == self._root.get_right():
                        stack_queue.append(current)
                        current = current.get_left()
        elif type is "pre":
            while stack_queue:
                current = stack_queue.pop()
                if current:
                    yield current
                    stack_queue.append(current.get_right()) if current.get_right() else None
                    stack_queue.append(current.get_left()) if current.get_left() else None
        elif type is "post":
            # this uses two stacks
            stack_queue_aux = []
            while stack_queue:
                current = stack_queue.pop()
                if current.get_left():
                    stack_queue.append(current.get_left())
                if current.get_right():
                    stack_queue.append(current.get_right())
                stack_queue_aux.append(current)

            while stack_queue_aux:
                current = stack_queue_aux.pop()
                yield current














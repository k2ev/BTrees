from abc import ABCMeta, abstractmethod

class NodeBTree(metaclass=ABCMeta):

    @property
    @abstractmethod
    def item(self):
        pass

    @property
    @abstractmethod
    def left(self):
        pass

    @property
    @abstractmethod
    def right(self):
        pass

class NodeSimple(NodeBTree):
    def __init__(self, *args, **kwargs):
        self.item = args[0] if len(args) else None
        self.left = kwargs.pop('left', None)
        self.right = kwargs.pop('right', None)

    def __str__(self):
        return str(self.item) if self.item else " "

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
        self._left = node

    @right.setter
    def right(self, node):
        self._right = node

    def is_leaf(self):
        return True if self.left is None and self.right is None else False

    def is_null(self):
        if self.item is None and self.is_leaf():
            flag = True
        elif self.item is None and (self.left is None or self.left.item is None) and (
                self.right is None or self.right.item is None):
            flag = True
        else:
            flag = False

        return flag

    def has_one_child(self):
        return False if self.is_leaf() or (self.left and self.right) else True

    def children(self):
        yield self.left
        yield self.right

    def min_child_if_exists(self):
        if self.left:
            if self.right:
                if self.left < self.right:
                    return self.left
                else:
                    return self.right
            else:
                return self.left
        elif self.right:
            if self.left:
                if self.left < self.right:
                    return self.left
                else:
                    return self.right
            else:
                return self.right
        else:
            return None

    def max_child_if_exists(self):
        if self.left:
            if self.right:
                if self.left > self.right:
                    return self.left
                else:
                    return self.right
            else:
                return self.left
        elif self.right:
            if self.left:
                if self.left > self.right:
                    return self.left
                else:
                    return self.right
            else:
                return self.right
        else:
            return None

class NodeWithParent(NodeSimple):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = kwargs.pop('parent', None)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        self._parent = node

    def is_left_child(self):
        if self.parent and self.parent.left and self.parent.left is self:
            return True
        else:
            return False

    def is_right_child(self):
        if self.parent and self.parent.right and self.parent.right is self:
            return True
        else:
            return False

    def get_sibling(self):
        if self is not None:
            if self.parent is not None:
                if self.parent.left and self.parent.left is self:
                    return self.parent.right
                elif self.parent.right and self.parent.right is self:
                    return self.parent.left
        return None

    def get_grandparent(self):
        if self is not None:
            if self.parent is not None:
                return self.parent.parent
        return None

    def get_uncle(self):
        grandparent = self.get_grandparent()
        if self and self.parent and grandparent:
            if grandparent.left and grandparent.left is self.parent:
                return grandparent.right
            elif grandparent.right and grandparent.right is self.parent:
                return grandparent.left
        return None

class NodeWithColor(NodeWithParent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = kwargs.pop('color', None)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        assert color is None or color is True or color is False
        color = color if color is True else False   # default color is black i.e. False
        self._color = color

class NodeWithHeight(NodeWithParent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.height = kwargs.pop('height', 1)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        assert val is None or (val >= 0 and type(val) is int)
        self._height = val


class NodeFactory:
    _node_map = { 'simple': NodeSimple,
                 'regular': NodeWithParent,
                 'RB': NodeWithColor,
                 'AVL': NodeWithHeight,
                 'splay': NodeWithParent }

    def __init__(self):
        pass

    @classmethod
    def get_node(cls, *args, **kwargs):
        if cls is NodeFactory:
            val = args[0] if len(args) else None
            if isinstance(val, NodeBTree):
                return val
            else:
                node_type = kwargs.pop('node_type', 'regular')
                node_type_class = cls._node_map.get(node_type, NodeWithParent)
                return node_type_class(*args, **kwargs)
        else:
            super().__new__(*args, **kwargs)
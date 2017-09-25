from BST import BstRegular
from constants import *

def BstAVL(BstRegular):
    node_type = "AVL"

    def __init__(self):
        super().__init()

    @staticmethod
    def get_height(node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def insert(self, val):
        node = super().insert(val)
        if node:
            # do something
            return node
        else:
            return None

    def _avl_balancing_on_insert(node):
        # do something






from BST import BstRegular
from constants import *

def BstAVL(BstRegular):
    node_type = "AVL"

    def __init__(self):
        super().__init()

    @staticmethod
    def height(node):
        return node.height if node else 0

    def balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    





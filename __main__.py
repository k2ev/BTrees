from NodeBTree import *
from BTree import BTreeLinked
from BST import BST


def run_btree():
    #               a(10)
    #            /        \
    #          b(5)        c(2)
    #         /    \         \
    #       d(15)   f(20)    e(19)
    #      /
    #     g(25)
    a = NodeBTree(10)
    b = NodeBTree(5)
    c = NodeBTree(2)
    d = NodeBTree(15)
    e = NodeBTree(19)
    f = NodeBTree(20)
    g = NodeBTree(25)
    a.left = b
    b.left = d
    d.left = g
    a.right = c
    b.right = f
    c.right = e

    t = BTreeLinked(a)
    print(t)
    print("height of tree:", t.height())
    print("sum of nodes on max depth:", t.sum_max_depth())
    print("breadth of tree:", t.breadth())
    print("level of node f:", t.level(f))
    print("distance between node f and g:", t.distance(f, g))
    print("total nodes in tree:", len(t))
    print("value of all nodes:", t.sum_value())
    print("iterate")
    t.set_traverse_method("_in_order_iterative")
    for node in t:
        print(node)


def run_bst():
    a = BST(10)
    a.insert(20)
    a.insert(5)
    a.insert(2)
    a.remove(5)

    print( "length of BST is:", len(a))

    for x in a:
        print(x)


def main():
    # run_btree()
    run_bst()


if __name__ == "__main__":
    main()

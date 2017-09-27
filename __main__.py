from Nodes import *
from BST import *
from RBTree import *
from SplayTree import *
from AVLTree import *


def run_btree():
    #               a(10)
    #            /        \
    #          b(5)        c(2)
    #         /    \         \
    #       d(15)   f(20)    e(19)
    #      /
    #     g(25)
    a = NodeSimple(10)
    b = NodeSimple(5)
    c = NodeSimple(2)
    d = NodeSimple(15)
    e = NodeSimple(19)
    f = NodeSimple(20)
    g = NodeSimple(25)
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
    a = BstRegular(10)
    a.insert(20)
    a.insert(5)
    a.insert(7)
    a.insert(22)
    a.insert(4)
    a.insert(15)
    a.remove(5)

    print( "length of BstSimple is:", len(a))

    print(a)

def run_rbt():
    a = BstRB(8)
    a.insert(18)
    a.insert(5)
    a.insert(15)
    a.insert(17)
    a.insert(25)
    a.insert(40)
    a.insert(80)


    print(a)

def run_splay():
    a = BstSplay(8)
    a.insert(10)
    a.insert(7)
    a.insert(6)
    a.insert(5)
    a.insert(9)
    a.remove(7)

    print(a)

def run_avl():
    a = BstAVL(14)
    a.insert(71)
    a.insert(3)
    a.insert(52)
    a.insert(68)
    a.insert(92)
    a.insert(59)
    a.insert(37)
    a.insert(22)
    a.insert(49)
    a.insert(41)

    print(a)

def run_avl2():
    a = BstAVL.from_list("629148B357ACD")
    a.remove("1")
    print(a)

def main():
    #run_btree()
    #run_bst()
    #run_rbt()
    #run_splay()
    #run_avl()
    run_avl2()


if __name__ == "__main__":
    main()

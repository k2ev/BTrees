from NodeBTree import *
from BTree import *

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
a.set_left(b)
b.set_left(d)
d.set_left(g)
a.set_right(c)
b.set_right(f)
c.set_right(e)

t = BTreeLinked(a)
print(t)
print(t.height())
print(t.sum_max_depth())
print(t.breadth())
print(t.depth(f))
print(t._depth(b,b))
print(t.distance(f,g))
for node in t:
    print(node)
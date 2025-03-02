import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

class SplayTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

def splay(root, key):
    if root is None or root.key == key:
        return root

    if key < root.key:
        if root.left is None:
            return root
        if key < root.left.key:
            root.left.left = splay(root.left.left, key)
            root = rotate_right(root)
        elif key > root.left.key:
            root.left.right = splay(root.left.right, key)
            if root.left.right:
                root.left = rotate_left(root.left)
        return rotate_right(root) if root.left else root
    else:
        if root.right is None:
            return root
        if key > root.right.key:
            root.right.right = splay(root.right.right, key)
            root = rotate_left(root)
        elif key < root.right.key:
            root.right.left = splay(root.right.left, key)
            if root.right.left:
                root.right = rotate_right(root.right)
        return rotate_left(root) if root.right else root

def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    return y

def rotate_right(x):
    y = x.left
    x.left = y.right
    y.right = x
    return y

def insert(root, key, value):
    if root is None:
        return SplayTreeNode(key, value)
    root = splay(root, key)
    if root.key == key:
        return root
    new_node = SplayTreeNode(key, value)
    if key < root.key:
        new_node.right = root
        new_node.left = root.left
        root.left = None
    else:
        new_node.left = root
        new_node.right = root.right
        root.right = None
    return new_node

def search(root, key):
    return splay(root, key)

def fibonacci_splay(n, tree):
    tree = search(tree, n)
    if tree and tree.key == n:
        return tree.value, tree
    if n < 2:
        return n, insert(tree, n, n)
    val1, tree = fibonacci_splay(n - 1, tree)
    val2, tree = fibonacci_splay(n - 2, tree)
    result = val1 + val2
    tree = insert(tree, n, result)
    return result, tree

n_values = list(range(0, 951, 50))
lru_times = []
splay_times = []

for n in n_values:
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10) / 10
    lru_times.append(lru_time)

    tree = None
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree)[0], number=10) / 10
    splay_times.append(splay_time)

plt.figure(figsize=(10, 5))
plt.plot(n_values, lru_times, marker='o', label='LRU Cache')
plt.plot(n_values, splay_times, marker='s', label='Splay Tree')
plt.xlabel('n')
plt.ylabel('Час виконання (с)')
plt.title('Порівняння продуктивності методів Fibonacci')
plt.legend()
plt.grid()
plt.show()

print("n         LRU Cache Time (s)  Splay Tree Time (s)")
print("--------------------------------------------------")
for i in range(len(n_values)):
    print(f"{n_values[i]:<10}{lru_times[i]:<20.8f}{splay_times[i]:<20.8f}")

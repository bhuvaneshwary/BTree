import logging       
class BTreeNode:
    def __init__(self, order, leaf=False):
        self.order = order
        self.leaf = leaf
        self.keys = []  # Stores keys
        self.child = []  # Stores child keys

class BTree:
    def __init__(self, order):
        self.root = BTreeNode(order, leaf=True)
        self.order = order

    def insert(self, key):
        root = self.root
        if len(root.keys) == self.order - 1:  # root = full so split
            new_root = BTreeNode(self.order, leaf=False)
            new_root.child.append(root)
            self.split_child(new_root, 0)
            self.root = new_root
            self.insert_when_free(new_root, key)
        else:
            self.insert_when_free(root, key)

    def insert_when_free(self, node, key):
        if node.leaf:
            node.keys.append(key)
            node.keys.sort()  
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.child[i].keys) == self.order - 1:  # if child =  full split it
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self.insert_when_free(node.child[i], key)

    def split_child(self, parent, i):
        order = self.order
        node = parent.child[i]
        middle_index = (order - 1) // 2
        middle_value = node.keys[middle_index]

        # keepng old nodes to left and new to right
        right_node = BTreeNode(order, leaf=node.leaf)
        right_node.keys = node.keys[middle_index + 1:]
        node.keys = node.keys[:middle_index]

        if not node.leaf:
            right_node.child = node.child[middle_index + 1:]
            node.child = node.child[:middle_index + 1]

        # midddle key as parent
        parent.keys.insert(i, middle_value)
        parent.child.insert(i + 1, right_node)

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        print("Level", level, ":", node.keys)
        for child in node.child:
            self.print_tree(child, level + 1)


btree = BTree(order=4)  
values = [10, 20, 30, 40, 50, 60]
for v in values:
    btree.insert(v)
    print(f"\nInserted {v}:")
    btree.print_tree()

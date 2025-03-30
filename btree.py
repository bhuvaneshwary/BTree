import main 
import logging  
import result
logger = logging.getLogger(__name__)

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
        logger.info("Entering insert function")
        root = self.root
        if len(root.keys) == self.order - 1:  # root = full so split
            logger.info("Node is not full")
            new_root = BTreeNode(self.order, leaf=False)
            new_root.child.append(root)
            self.split_child(new_root, 0)
            self.root = new_root
            self.insert_when_free(new_root, key)
        else:
            self.insert_when_free(root, key)
        logger.info("Exiting insert function")

    def insert_when_free(self, node, key):
        logger.info("Entering insert_when_free")
        if node.leaf:
            logger.info("The node is a leaf")
            node.keys.append(key)
            node.keys.sort()  
        else:
            logger.info("Inserting into a non-leaf node")
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.child[i].keys) == self.order - 1:  # if child =  full split it
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self.insert_when_free(node.child[i], key)
            logger.info("Exiting insert_when_free")

    def split_child(self, parent, i):
        logger.info("Entering split_child")
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
        logger.info("Exiting split_child")

    def print_tree(self, node=None, level=0):
        logger.info("Entering print_tree")
        if node is None:
            node = self.root
        print("Level", level, ":", node.keys)
        for child in node.child:
            self.print_tree(child, level + 1)
        logger.info("Exiting print_tree")


def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Started')
if __name__ == "__main__":
    main()
    print(__name__)

btree = BTree(order=4)   
values = [10, 20, 30, 40, 50, 60]
for v in values:
    btree.insert(v)
    print(f"\nInserted {v}:")
    btree.print_tree()

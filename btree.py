import main 
import logging  
import result
logger = logging.getLogger(__name__)

class BTreeNode:
    def __init__(self, order, leaf=False):
        logger.info("Creating a BTree Node")
        self.order = order
        self.leaf = leaf
        self.keys = []  # Stores keys
        self.child = []  # Stores child keys

class BTree:
    def __init__(self, order):
        logger.info("Creating a BTree")
        self.root = BTreeNode(order, leaf=True)
        self.order = order

    def insert(self, key)->result.ret_val:
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
        ret = result.ret_val("insertion completed successfully",1)
        return ret
        

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
   
    def delete(self, key):
        if not self.root:
            print("Tree is empty")
            return

        self.delete_(self.root, key)

        if len(self.root.keys) == 0:
            if not self.root.leaf:
                self.root = self.root.children[0]
            else:
                self.root = None
    def delete_(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == key:
            if node.leaf:
                node.keys.pop(i)
            else:
                if len(node.children[i].keys) >= (self.order // 2):
                    predecessor = self.get_predecessor(node, i)
                    node.keys[i] = predecessor
                    self.delete_(node.children[i], predecessor)
                elif len(node.children[i + 1].keys) >= (self.order // 2):
                    successor = self.get_successor(node, i)
                    node.keys[i] = successor
                    self.delete_(node.children[i + 1], successor)
                else:
                    self.merge(node, i)
                    self.delete_(node.children[i], key)
        else:
            if node.leaf:
                print(f"Key {key} not found")
                return

            is_last_child = (i == len(node.keys))
            if len(node.children[i].keys) < (self.order // 2):
                self.fill(node, i)

            if is_last_child and i > len(node.keys):
                self.delete_(node.children[i - 1], key)
            else:
                self.delete_(node.children[i], key)
    def get_predecessor(self, node, i):
        cur = node.children[i]
        while not cur.leaf:
            cur = cur.children[-1]
        return cur.keys[-1]

    def get_successor(self, node, i):
        cur = node.children[i + 1]
        while not cur.leaf:
            cur = cur.children[0]
        return cur.keys[0]

    def fill(self, node, i):
        if i != 0 and len(node.children[i - 1].keys) >= (self.order // 2):
            self.borrow_from_prev(node, i)
        elif i != len(node.keys) and len(node.children[i + 1].keys) >= (self.order // 2):
            self.borrow_from_next(node, i)
        else:
            if i != len(node.keys):
                self.merge(node, i)
            else:
                self.merge(node, i - 1)

    def borrow_from_prev(self, node, i):
        child = node.children[i]
        sibling = node.children[i - 1]

        child.keys.insert(0, node.keys[i - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

        node.keys[i - 1] = sibling.keys.pop()

    def borrow_from_next(self, node, i):
        child = node.children[i]
        sibling = node.children[i + 1]

        child.keys.append(node.keys[i])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))

        node.keys[i] = sibling.keys.pop(0)
    
    def merge(self, node, i):
        child = node.children[i]
        sibling = node.children[i + 1]

        child.keys.append(node.keys.pop(i))
        child.keys.extend(sibling.keys)

        if not child.leaf:
            child.children.extend(sibling.children)

        node.children.pop(i + 1)



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

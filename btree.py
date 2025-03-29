import logger
class BTreeNode:
    def __init__(self, order, leaf=False):
        self.order = order         
        self.leaf = leaf           
        self.keys = []             
        self.children = []         
class BTree:
    def __init__(self, order):
        self.root = BTreeNode(order, leaf=True) 
        self.order = order 
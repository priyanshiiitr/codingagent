from collections import deque

class Node:
    """
    A class to represent a node in a binary tree.
    Each node has a value, and pointers to its left and right children.
    """
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None

class BinaryTree:
    """
    A class to represent a binary tree and its core operations.
    This implementation uses level-order insertion to build the tree.
    """
    def __init__(self):
        self.root = None

    def insert(self, data):
        """
        Inserts a new node into the tree in the first available spot,
        using level order (breadth-first) traversal.
        """
        new_node = Node(data)
        if self.root is None:
            self.root = new_node
            return

        # Use a queue for level order insertion
        q = deque([self.root])
        while q:
            temp = q.popleft()

            # Check for left child
            if not temp.left:
                temp.left = new_node
                break
            else:
                q.append(temp.left)

            # Check for right child
            if not temp.right:
                temp.right = new_node
                break
            else:
                q.append(temp.right)

    def inorder_traversal(self):
        """
        Performs inorder traversal (Left, Root, Right) of the tree.
        Returns a list of node values.
        """
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)

    def preorder_traversal(self):
        """
        Performs preorder traversal (Root, Left, Right) of the tree.
        Returns a list of node values.
        """
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.val)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder_traversal(self):
        """
        Performs postorder traversal (Left, Right, Root) of the tree.
        Returns a list of node values.
        """
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.val)

    def levelorder_traversal(self):
        """
        Performs level order traversal (breadth-first) of the tree.
        Returns a list of node values.
        """
        if not self.root:
            return []

        result = []
        q = deque([self.root])
        while q:
            node = q.popleft()
            result.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        return result

# --- Main execution block to demonstrate the Binary Tree ---
if __name__ == "__main__":
    # Create a binary tree instance
    tree = BinaryTree()

    # Insert elements into the tree. The insertion is level by level.
    nodes_to_insert = [1, 2, 3, 4, 5, 6, 7]
    for node_val in nodes_to_insert:
        tree.insert(node_val)

    # The resulting tree structure will be a complete binary tree:
    #        1
    #       / \
    #      2   3
    #     / \ / \
    #    4  5 6  7

    print(f"Binary Tree created with values: {nodes_to_insert}")
    print("-" * 40)

    # Demonstrate the different traversal methods
    print("Inorder traversal (Left, Root, Right):")
    print(tree.inorder_traversal()) # Expected: [4, 2, 5, 1, 6, 3, 7]
    print("-" * 40)

    print("Preorder traversal (Root, Left, Right):")
    print(tree.preorder_traversal()) # Expected: [1, 2, 4, 5, 3, 6, 7]
    print("-" * 40)

    print("Postorder traversal (Left, Right, Root):")
    print(tree.postorder_traversal()) # Expected: [4, 5, 2, 6, 7, 3, 1]
    print("-" * 40)

    print("Level-order traversal (Breadth-First):")
    print(tree.levelorder_traversal()) # Expected: [1, 2, 3, 4, 5, 6, 7]
    print("-" * 40)

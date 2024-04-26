from collections import deque


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = set()
        self.parent = None

    def add_parent(self, parent_node):
        self.parent = parent_node

    def add_child(self, child_node):
        self.children.add(child_node)

    def is_equal(self, node: "TreeNode"):
        return self.value == node.value

    def __str__(self):
        return f"TreeNode(value={self.value},num_of_children={len(self.children)})"


class Tree:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = 0

    def add_edge(self, parent: "TreeNode", child: "TreeNode"):
        parent.add_child(child)
        child.add_parent(parent)

    def get_path(self, start_node: "TreeNode", target_node: "TreeNode"):
        # BFS
        queue = deque()
        queue.append((start_node, [start_node]))
        visited = [start_node]

        while queue:
            current_node, path = queue.popleft()
            if current_node == target_node:
                return path
            children = current_node.children
            for child in children:
                if child in visited:
                    continue
                queue.append((child, path + [child]))
                visited.append(child)

        return []

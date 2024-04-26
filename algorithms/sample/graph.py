from collections import deque


class GraphNode:
    def __init__(self, value):
        self.value = value
        self.neighbors = set()

    def add_neighbor(self, neighbor_node):
        self.neighbors.add(neighbor_node)

    def __str__(self):
        return f"GraphNode(value={self.value},num_of_neighbors={len(self.neighbors)})"


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = 0

    def add_edge(self, node1: "GraphNode", node2: "GraphNode"):
        node1.add_neighbor(node2)
        node2.add_neighbor(node1)

    def get_path(self, start_node: "GraphNode", target_node: "GraphNode"):
        queue = deque()
        queue.append((start_node, [start_node]))
        visited = [start_node]

        while queue:
            current_node, path = queue.popleft()
            if current_node == target_node:
                return path
            neighbors = current_node.neighbors
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                queue.append((neighbor, path + [neighbor]))
                visited.append(neighbor)

        return []

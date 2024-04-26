from algorithms.sample.graph import Graph, GraphNode
from utils import point


class PRM:
    q_init = None
    q_target = None
    graph: Graph = None
    domain: list = []
    k: int = None
    step: int = 1
    obstacles: list = [[], []]

    def set_attributes(self, domain, step, obstacles = [[], []]):
        self.graph = Graph()
        self.domain = domain
        self.obstacles = obstacles

    def plan(self, q_init, q_target, density = 1):
        if isinstance(q_init, list) and isinstance(q_target, list):
            q_init = GraphNode(q_init)
            q_target = GraphNode(q_target)
        self.map()
        print("Mapping done.")
        self.prm(q_init, q_target)
        return self.graph.get_path(q_init, q_target)

    def prm(self, q_init, q_target):
        # local mapping
        node_close_init = self.get_k_nearest_neighbors(q_init, 1)[0]
        node_close_target = self.get_k_nearest_neighbors(q_target, 1)[0]
        self.graph.add_node(q_init)
        self.graph.add_node(q_target)
        self.graph.add_edge(q_init, node_close_init)
        self.graph.add_edge(q_target, node_close_target)

    def map(self, density = 5):
        for _ in range(self.domain[0] * (len(self.domain) ** density)):
            self.graph.add_node(self.get_sample_node())

        visited = []

        for node in self.graph.nodes:
            k_neighbors = self.get_k_nearest_neighbors(node, 4)
            visited.append(node)
            for neighbor in k_neighbors:
                self.graph.add_edge(node, neighbor)
                visited.append(neighbor)

    def get_k_nearest_neighbors(self, target_node, k = 1):
        dist_dict = {float("inf"): None}
        for current_node in self.graph.nodes:
            dist = point.find_distance(target_node.value, current_node.value)
            dist_dict[dist] = current_node
        if len(dist_dict) == 0:
            return []
        sorted_node_indices = sorted(dist_dict)
        k_neighbors = [dist_dict[i] for i in sorted_node_indices[:k] if dist_dict[i] is not None]
        return k_neighbors

    def get_sample_node(self):
        p = point.get_sample_point(self.domain)
        return GraphNode(p)

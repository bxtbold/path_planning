from algorithms.sample.tree import Tree
from utils import point


class PRM:
    q_init = None
    q_target = None
    tree: Tree = None
    domain: list = []
    k: int = None
    step: int = 1
    obstacles: list = [[], []]

    def set_attributes(self, q_init, q_target, domain, k, step, obstacles = [[], []]):
        self.tree = Tree(q_init)
        self.q_init = q_init
        self.q_target = q_target
        self.domain = domain
        self.obstacles = obstacles

    def plan(self):
        self.map()

        # local map
        node_close_init = point.get_nearest_point(self.q_init, self.tree.vertices)
        node_close_target = point.get_nearest_point(self.q_target, self.tree.vertices)
        path = self.tree.get_path(node_close_init, node_close_target)

        path.insert(0, [node_close_init, self.q_init])
        path.append([node_close_target, self.q_target])

        return path

    def map(self):
        for _ in range(self.domain[0] * (len(self.domain) + 1)):
            self.tree.add_vertex(self.get_sample_vertex())

        k = 5
        for vertex in self.tree.vertices:
            k_neighbors = point.get_k_nearest_point(vertex, self.tree.vertices, k)
            for neighbor in k_neighbors:
                self.tree.add_edge([vertex, neighbor])

    def get_sample_vertex(self):
        return point.get_sample_point(self.domain)

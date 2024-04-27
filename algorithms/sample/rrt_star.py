from algorithms.sample.tree import Tree, TreeNode
from utils import point


class RRTStar:
    q_init = None
    q_target = None
    tree: Tree = None
    domain: list = []
    k: int = None
    step: int = 1
    obstacles: list = [[], []]

    def set_attributes(self, domain, step, obstacles = [[], []]):
        self.tree = Tree()
        self.domain = domain
        self.step = step
        self.obstacles = obstacles

    def plan(self, q_init, q_target, k = 1000):
        if isinstance(q_init, list) and isinstance(q_target, list):
            q_init = TreeNode(q_init)
            q_target = TreeNode(q_target)

        if self.rrt_star(q_init, q_target, k):
            return self.tree.get_path(q_init, q_target)
        return []

    def rrt_star(self, q_init, q_target, k = 1000):
        result = False
        self.tree.add_node(q_init)
        i = 0
        distance = point.find_distance(q_init.value, q_target.value)
        while i < k:
            i += 1
            # sample a new config
            q_random = self.get_sample_node()
            q_nearest_nodes = self.get_k_nearest_neighbors(q_random, 6)

            costs = {}
            for each_nearest in q_nearest_nodes:
                q_new = self.steer(q_random, each_nearest)
                distance = point.find_distance(q_new.value, each_nearest.value) + \
                            point.find_distance(each_nearest.value, q_init.value)
                costs[distance] = [q_new, each_nearest]

            q_new, q_nearest = costs[min(costs.keys())]
            q_new = self.steer(q_new, q_nearest)
            # add the new config to the tree
            self.update_tree(q_nearest, q_new)
            # check if the new config is close to target
            distance = point.find_distance(q_new.value, q_target.value)
            if distance < self.step:
                self.update_tree(q_nearest, q_target)
                result = True

        return result

    def update_tree(self, q_nearest, q_new):
        self.tree.add_node(q_new)
        self.tree.add_edge(q_nearest, q_new)

    def get_sample_node(self):
        p = point.get_sample_point(self.domain)
        return TreeNode(p)

    def get_nearest_neighbor(self, target_node):
        nearest_points = self.get_k_nearest_neighbors(target_node, 1)
        return nearest_points[0]

    def get_k_nearest_neighbors(self, target_node, k = 1):
        dist_dict = {float("inf"): None}
        for current_node in self.tree.nodes:
            dist = point.find_distance(target_node.value, current_node.value)
            dist_dict[dist] = current_node
        if len(dist_dict) == 0:
            return []
        sorted_node_indices = sorted(dist_dict)
        k_neighbors = [dist_dict[i] for i in sorted_node_indices[:k] if dist_dict[i] is not None]
        return k_neighbors

    def steer(self, q, q_nearest):
        return TreeNode(
            value=point.get_new_point(q.value, q_nearest.value, self.step)
        )

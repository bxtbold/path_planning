from algorithms.sample.tree import Tree
from utils.point import find_distance, get_nearest_point, get_sample_point, steer, get_k_nearest_point
from utils.plot import *


class RRTStar:
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
        self.k = k
        self.step = step
        self.obstacles = obstacles

    def plan(self):
        if self.traverse_k_times(self.k):
            print("Solution found.")
            return self.tree.get_path(self.q_init, self.q_target)
        print(f"No solution found in {self.k} steps :(")
        return []

    def traverse_k_times(self, k):
        result = False
        i = 0
        # distance = find_distance(self.q_init, self.q_target)
        while i < k:
            i += 1
            # sample a new config
            q_random = self.get_sample_vertex()
            q_k_nearest = self.get_k_nearest_neighbors(q_random, 5)
            costs = []
            for each_nearest in q_k_nearest:
                q_new = self.steer(q_random, each_nearest)
                cost = find_distance(q_new, each_nearest) + find_distance(self.q_init, each_nearest)
                costs.append(cost)

            q_nearest = q_k_nearest[costs.index(min(costs))]
            q_new = self.steer(q_random, q_nearest)

            if find_distance(q_new, self.q_target) < self.step:
                self.update_tree(q_nearest, self.q_target)
                result = True
                break
            else:
                self.update_tree(q_nearest, q_new)


        return result

    def is_collision_free(self, q):
        for origin, radius in zip(self.obstacles[0], self.obstacles[1]):
            if find_distance(q, origin) > radius:
                return False
        return True

    def update_tree(self, q_nearest, q_new):
        self.tree.add_vertex(q_new)
        self.tree.add_edge([q_nearest, q_new])

    def get_sample_vertex(self):
        return get_sample_point(self.domain)

    def get_nearest_neighbor(self, vertex):
        return get_nearest_point(vertex, self.tree.vertices)

    def get_k_nearest_neighbors(self, vertex, k):
        return get_k_nearest_point(vertex, self.tree.vertices, k)

    def steer(self, q, q_nearest):
        return steer(q, q_nearest, self.step)

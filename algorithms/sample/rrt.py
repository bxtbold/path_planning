from algorithms.sample.tree import Tree
from utils.point import find_distance, get_nearest_point, get_sample_point, get_new_point
from utils.plot import *


class RRT:
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
        distance = find_distance(self.q_init, self.q_target)
        while i < k:
            i += 1
            # sample a new config
            q_new, q_nearest = self.traverse_once()
            # check collision
            # if not self.is_collision_free(q_new):
                # continue
            # check if the new config is close to target
            distance = find_distance(q_new, self.q_target)
            if distance < self.step:
                self.update_tree(q_nearest, self.q_target)
                result = True
                break

        return result

    def traverse_once(self):
        q_random = self.get_sample_vertex()
        q_nearest = self.get_nearest_neighbor(q_random)
        q_new = self.get_new_vertex(q_random, q_nearest)
        self.update_tree(q_nearest, q_new)
        return q_new, q_nearest

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

    def get_new_vertex(self, q, q_nearest):
        return get_new_point(q, q_nearest, self.step)

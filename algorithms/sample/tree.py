import time

class Tree:
    edges: list = []
    vertices: list = []

    def __init__(self, q_init):
        self.add_vertex(q_init)

    def add_edge(self, edge):
        self.edges.append(edge)

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def reset(self):
        self.edges.clear()
        self.vertices.clear()

    def get_path(self, start, end):
        # TODO: improve local planning (use djikstra instead)
        path = []
        current_vertex = end
        start = time.time()
        while current_vertex != start:
            for edge in self.edges:
                if edge[1] == current_vertex:
                    q1, q2 = edge
                    path.append((q1, q2))
                    current_vertex = q1
                    break
        path.reverse()
        return path

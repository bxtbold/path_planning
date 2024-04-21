import math
import numpy as np
import random


def get_new_point(q, q_nearest, step):
    try:
        vector = (np.array(q) - np.array(q_nearest)) / find_distance(q, q_nearest)
    except Exception as e:
        print("get_new_point: ", e)
        return []
    result = list(np.array(q_nearest) + vector * step)
    return [round(i, 3) for i in result]


def get_sample_point(domain, obstacles = []):
    # TODO: check if the sample is free of obstacles
    return [round(random.randint(0, domain[i]), 4) for i in range(len(domain))]


def find_distance(a, b):
    tmp = 0
    for i, j in zip(a, b):
        tmp += (i - j) ** 2
    return math.sqrt(tmp)


def get_nearest_point(point, vertices):
    dist = []
    for i in vertices:
        dist.append(find_distance(point, i))
    m = dist.index(min(dist))
    return vertices[m]


def get_k_nearest_point(point, vertices, k = 1):
    if k < 1:
        return []

    dist = []
    for i in range(len(vertices)):
        d = find_distance(vertices[i], point)
        dist.append((d, i))

    sorted_array = sorted(dist, key=lambda x: x[0])

    k_neighbors = []
    for d, i in sorted_array[:k]:
        k_neighbors.append(vertices[i])

    return k_neighbors

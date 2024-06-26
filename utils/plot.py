import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def init_plot(domain):
    fig = plt.figure()
    if len(domain) == 2:
        ax = fig.add_subplot(111)
    elif len(domain) == 3:
        ax = fig.add_subplot(111, projection="3d")
    plt.ion()
    return ax


def plot(ax, q1, q2, color1 = "gray", color2 = "gray"):
    try:
        if len(q1) == len(q2) == 2:
            ax.plot([q1[0], q2[0]], [q1[1], q2[1]], color=color1, marker='.', markersize=5)
        elif len(q1) == len(q2) == 3:
            ax.scatter(*q1, s=4, c=color1)
            ax.scatter(*q2, s=4, c=color1)
            ax.plot([q2[0], q1[0]], [q2[1], q1[1]], [q2[2], q1[2]], color=color2)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")


def scatter(ax, q, size, color="gray"):
    try:
        if len(q) == 3:
            ax.scatter(*q, s=size, c=color)
        elif len(q) == 2:
            ax.plot(q[0], q[1], '.', color=color, markersize=size)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")


def draw_sphere(ax, radius, origin = (0, 0, 0), color = "yellow"):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 2 * radius * np.outer(np.cos(u), np.sin(v))
    y = 2 * radius * np.outer(np.sin(u), np.sin(v))
    z = 2 * radius * np.outer(np.ones(np.size(u)), np.cos(v))

    x += origin[0]
    y += origin[1]
    z += origin[2]

    # Plot the surface
    ax.plot_surface(x, y, z, color = color)


def draw_circle(ax, radius, origin = (0, 0), color = "yellow"):
    circle = plt.Circle(origin, radius)
    circle.set_facecolor(color)
    ax.add_patch(circle)


def pause(duration):
    try:
        plt.pause(duration)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")


def draw_path(q_init, q_target, planner_name, planner, path, frame_update: int = 0.5):
    ax = init_plot(planner.domain)

    if len(planner.obstacles) > 0:
        # draw planner
        draw_obstacle = draw_sphere if len(planner.domain) == 3 else draw_circle
        for origin, radius in zip(planner.obstacles[0], planner.obstacles[1]):
            draw_obstacle(ax, radius, origin)

    scatter(ax, q_init, 15, 'green')
    scatter(ax, q_target, 15, 'blue')

    # draw a tree
    if hasattr(planner, "tree"):
        plt.title(f"{planner_name} {len(planner.tree.nodes) - 2} steps")
        for node in planner.tree.nodes:
            for child in node.children:
                plot(ax, node.value, child.value)

    elif hasattr(planner, "graph"):
        plt.title(f"{planner_name}")
        for node in planner.graph.nodes:
            for child in node.neighbors:
                plot(ax, node.value, child.value)

    # draw a path
    for i in range(len(path)):
        if i < len(path) - 1:
            plot(ax, path[i].value, path[i+1].value, "red", "red")

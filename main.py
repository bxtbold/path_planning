import time

from algorithms.sample.rrt import RRT
from algorithms.sample.rrt_star import RRTStar
from utils.plot import *
from utils.point import *


should_plot = True


def random_obstacles(domain):
    origins = []
    radii = []
    for _ in range(8):
        np.random.seed()
        radius = np.random.randint(2, 5)
        origin = get_sample_point(domain)
        origins.append(origin)
        radii.append(radius)
    return [origins, radii]


if __name__ == "__main__":
    k = 1000
    step = 5
    domain = (100, 100)  # (100, 100, 100)
    # obstacles = random_obstacles(domain)
    obstacles = []

    # get collision free start and end configs
    q_init = get_sample_point(domain)
    q_target = get_sample_point(domain)
    # while not is_collision_free(q_init, obstacles) and not is_collision_free(q_target, obstacles):
    #     q_init = get_sample_point(domain)
    #     q_target = get_sample_point(domain)

    # rrt = RRT()
    rrt = RRTStar()
    rrt.set_attributes(q_init, q_target, domain, k, step, obstacles)
    path = rrt.plan()

    print("path: ", path)

    if should_plot and len(path) > 0:
        ax = init_plot(domain) if should_plot else None
        plt.title(f"RRT planner {len(rrt.tree.edges)} steps")

        if len(obstacles) > 0:
            # draw obstacles
            draw_obstacle = draw_sphere if len(domain) == 3 else draw_circle
            for origin, radius in zip(obstacles[0], obstacles[1]):
                draw_obstacle(ax, radius, origin)

        scatter(ax, q_init, 15, 'green')
        scatter(ax, q_target, 15, 'blue')

        # draw a graph
        last_updated_time = 0
        for q1, q2 in rrt.tree.edges:
            plot(ax, q1, q2)
            if time.time() - last_updated_time > 0.5:
                pause(1 / 10 ** (len(q1) * 3))
                last_updated_time = time.time()
            time.sleep(0.01)

        # draw a path
        for q1, q2 in path:
            plot(ax, q1, q2, "red", "red")
        pause(5)

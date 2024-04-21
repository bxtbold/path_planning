import time

from algorithms.sample.rrt import RRT
from algorithms.sample.rrt_star import RRTStar
from utils.plot import *
from utils.point import *
from utils.config_parser import load_configs


PLANNERS = {
    "RRT": RRT(),
    "RRT*": RRTStar()
}


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
    configs = load_configs()
    planner_name = configs["planner"]
    k = configs["k"]
    step = configs["step"]
    domain = [configs["domain"]] * configs["dimensions"]  # (100, 100, 100)
    obstacles = random_obstacles(domain) if configs["use_obstacle"] else []
    should_plot = configs["should_visualize"]

    # get collision free start and end configs
    q_init = get_sample_point(domain, obstacles)
    q_target = get_sample_point(domain, obstacles)

    planner = PLANNERS[planner_name]
    planner.set_attributes(q_init, q_target, domain, k, step, obstacles)
    path = planner.plan()

    print("path: ", path)

    if should_plot and len(path) > 0:
        ax = init_plot(domain) if should_plot else None
        plt.title(f"{planner_name} {len(planner.tree.edges)} steps")

        if len(obstacles) > 0:
            # draw obstacles
            draw_obstacle = draw_sphere if len(domain) == 3 else draw_circle
            for origin, radius in zip(obstacles[0], obstacles[1]):
                draw_obstacle(ax, radius, origin)

        scatter(ax, q_init, 15, 'green')
        scatter(ax, q_target, 15, 'blue')

        # draw a graph
        last_updated_time = 0
        pause(10)
        for q1, q2 in planner.tree.edges:
            plot(ax, q1, q2)
            if time.time() - last_updated_time > 0.1:
                pause(1 / 10 ** (len(q1) * 3))
                last_updated_time = time.time()
            time.sleep(0.01)

        # draw a path
        for q1, q2 in path:
            plot(ax, q1, q2, "red", "red")
        pause(5)

import numpy as np

from algorithms.sample import rrt, rrt_star, prm
from utils import plot, point, config_parser


PLANNERS = {
    "PRM": prm.PRM(),
    "RRT": rrt.RRT(),
    "RRT*": rrt_star.RRTStar()
}


def random_obstacles(domain):
    origins = []
    radii = []
    for _ in range(8):
        np.random.seed()
        radius = np.random.randint(2, 5)
        origin = point.get_sample_point(domain)
        origins.append(origin)
        radii.append(radius)
    return [origins, radii]


if __name__ == "__main__":
    # parse configuration from config.yaml
    configs = config_parser.load_configs()
    planner_name = configs["planner"]
    k = configs["k"]
    step = configs["step"]
    domain = [configs["domain"]] * configs["dimensions"]  # (100, 100, 100)
    obstacles = random_obstacles(domain) if configs["use_obstacle"] else []
    should_plot = configs["should_visualize"]
    frame_update = configs["frame_update"]

    # get collision free random two samples
    q_init = point.get_sample_point(domain, obstacles)
    q_target = point.get_sample_point(domain, obstacles)

    # plan
    planner = PLANNERS[planner_name]
    planner.set_attributes(domain, step, obstacles)
    path = planner.plan(q_init, q_target, k)

    if len(path) < 0:
        print("No solution found :(")
    print("Solution found.")

    # visualize
    if should_plot:
        plot.draw_path(q_init, q_target, planner_name, planner, path, frame_update)
        plot.pause(10)

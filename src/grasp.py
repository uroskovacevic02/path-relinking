
import random

from construction import greedy_randomized
from local_search import two_opt
from path_relinking import (path_relink, path_relink_backward,
                            path_relink_back_and_forward, path_relink_mixed)
from elite import EliteSet


# maps a variant name to the function that performs it
PR_VARIANTS = {
    "forward": path_relink,
    "backward": path_relink_backward,
    "back_and_forward": path_relink_back_and_forward,
    "mixed": path_relink_mixed,
}


def grasp_pr(instance, iterations=100, alpha=0.3, elite_size=10, min_diff=3,
             use_pr=True, variant="forward", seed=None):
    if seed is not None:
        random.seed(seed)

    relink = PR_VARIANTS[variant]   # pick the chosen PR variant

    elite = EliteSet(instance, max_size=elite_size, min_diff=min_diff)

    best_tour = None
    best_cost = float("inf")
    history = []                  

    for _ in range(iterations):
        # 1. build a solution: greedy randomized construction + 2-opt
        tour = two_opt(instance, greedy_randomized(instance, alpha=alpha))
        cost = instance.tour_cost(tour)

        # 2. path relinking with a random tour from the elite set
        if use_pr and len(elite.members) > 0:
            guide = elite.random_member()
            pr_tour, _ = relink(instance, tour, guide)
            if pr_tour is not None:
                pr_tour = two_opt(instance, pr_tour)  
                pr_cost = instance.tour_cost(pr_tour)
                if pr_cost < cost:
                    tour, cost = pr_tour, pr_cost

        elite.add(tour)

        if cost < best_cost:
            best_cost = cost
            best_tour = tour

        history.append(best_cost)

    return best_tour, best_cost, history

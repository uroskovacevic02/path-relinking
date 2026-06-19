
import random

from construction import greedy_randomized
from local_search import two_opt
from path_relinking import path_relink
from elite import EliteSet


def grasp_pr(instance, iterations=100, alpha=0.3,
             elite_size=10, min_diff=3, use_pr=True, seed=None):
    if seed is not None:
        random.seed(seed)

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
            pr_tour, _ = path_relink(instance, tour, guide)
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


import random


def greedy_randomized(instance, alpha=0.3, start=None):
    n = instance.n
    dist = instance.dist

    if start is None:
        start = random.randrange(n)   # random starting city

    visited = [False] * n
    tour = [start]
    visited[start] = True
    current = start

    for _ in range(n - 1):
        candidates = []
        for city in range(n):
            if not visited[city]:
                candidates.append((dist[current][city], city))

        cmin = min(c[0] for c in candidates)
        cmax = max(c[0] for c in candidates)

        # RCL: keep candidates whose distance is "good enough"
        threshold = cmin + alpha * (cmax - cmin)
        rcl = []
        for d, city in candidates:
            if d <= threshold:
                rcl.append(city)

        next_city = random.choice(rcl)

        tour.append(next_city)
        visited[next_city] = True
        current = next_city

    return tour

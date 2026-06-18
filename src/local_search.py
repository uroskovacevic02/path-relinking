

def two_opt(instance, tour):
    dist = instance.dist
    n = len(tour)
    tour = tour[:]   # copy

    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                a = tour[i - 1]
                b = tour[i]
                c = tour[j]
                d = tour[(j + 1) % n]

                
                old = dist[a][b] + dist[c][d]
                new = dist[a][c] + dist[b][d]

                if new < old:   # shorter -> apply the move
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improved = True

    return tour

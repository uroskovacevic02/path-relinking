
def edge_set(tour):
    
    edges = set()
    n = len(tour)
    for k in range(n):
        a = tour[k]
        b = tour[(k + 1) % n]
        edges.add(frozenset((a, b))) #frozenset because in frozenset (7,3) == (3,7)
    return edges


def path_relink(instance, init, guide):
    dist = instance.dist
    n = len(init)

    current = init[:]     # copy
    current_cost = instance.tour_cost(current)
    guide_edges = edge_set(guide)

    best = None                            
    best_cost = float("inf")

    while True:
        # look for the best move that brings us CLOSER to the guide
        move = None
        move_delta = float("inf")

        for i in range(1, n - 1):
            for j in range(i + 1, n):
                a = current[i - 1]
                b = current[i]
                c = current[j]
                d = current[(j + 1) % n]

                # edges we would remove and add by reversing tour[i..j]
                removed = (frozenset((a, b)) in guide_edges) + (frozenset((c, d)) in guide_edges)
                added = (frozenset((a, c)) in guide_edges) + (frozenset((b, d)) in guide_edges)

                # keep only moves that increase the number of guide edges !
                if added - removed <= 0:
                    continue

                delta = (dist[a][c] + dist[b][d]) - (dist[a][b] + dist[c][d])
                if delta < move_delta:
                    move_delta = delta
                    move = (i, j)

        if move is None:
            break

        i, j = move
        current[i:j + 1] = reversed(current[i:j + 1])
        current_cost += move_delta

        if current_cost < best_cost and current != guide:
            best_cost = current_cost
            best = current[:]

    return best, best_cost


def path_relink_backward(instance, init, guide):
    # backward = relink in the opposite direction
    return path_relink(instance, guide, init)


def path_relink_back_and_forward(instance, init, guide):
    # run both directions, keep whichever found the better tour
    fb, fc = path_relink(instance, init, guide)
    bb, bc = path_relink(instance, guide, init)

    if fb is None:          # forward found nothing -> take backward
        return bb, bc
    if bb is None:          # backward found nothing -> take forward
        return fb, fc

    if fc <= bc:            # both found something -> take the cheaper one
        return fb, fc
    return bb, bc

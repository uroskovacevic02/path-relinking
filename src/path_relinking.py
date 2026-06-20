
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
    # run both directions, keep which found the better tour
    fb, fc = path_relink(instance, init, guide)
    bb, bc = path_relink(instance, guide, init)

    if fb is None:         
        return bb, bc
    if bb is None:          
        return fb, fc

    if fc <= bc:            # take cheaper one
        return fb, fc
    return bb, bc


def path_relink_mixed(instance, init, guide):
    dist = instance.dist
    n = len(init)

    a = init[:]            # starts at init, moves toward b
    b = guide[:]           # starts at guide, moves toward a
    cost_a = instance.tour_cost(a)
    cost_b = instance.tour_cost(b)

    best = None
    best_cost = float("inf")

    move_a = True          # whose turn it is to move this step

    while a != b:
        # pick the moving tour and its target (the other tour)
        if move_a:
            current, current_cost, target = a, cost_a, b
        else:
            current, current_cost, target = b, cost_b, a
        target_edges = edge_set(target)

        # best 2-opt move that brings `current` closer to `target`
        move = None
        move_delta = float("inf")
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                x = current[i - 1]
                y = current[i]
                z = current[j]
                w = current[(j + 1) % n]

                removed = (frozenset((x, y)) in target_edges) + (frozenset((z, w)) in target_edges)
                added = (frozenset((x, z)) in target_edges) + (frozenset((y, w)) in target_edges)
                if added - removed <= 0:
                    continue

                delta = (dist[x][z] + dist[y][w]) - (dist[x][y] + dist[z][w])
                if delta < move_delta:
                    move_delta = delta
                    move = (i, j)

        if move is None:
            break          # cannot bring them closer -> stop

        # apply the move on the current tour
        i, j = move
        current[i:j + 1] = reversed(current[i:j + 1])
        current_cost += move_delta
        if move_a:
            cost_a = current_cost
        else:
            cost_b = current_cost

        # remember the best intermediate (not the two original endpoints)
        if current_cost < best_cost and current != init and current != guide:
            best_cost = current_cost
            best = current[:]

        move_a = not move_a   # alternate sides

    return best, best_cost

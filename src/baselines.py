
def nearest_neighbor(instance, start=0):
   
    n = instance.n
    dist = instance.dist

    visited = [False] * n
    tour = [start]
    visited[start] = True
    current = start

    
    for _ in range(n - 1):
        nearest_city = -1
        nearest_dist = float("inf")   

        for city in range(n):
            if not visited[city] and dist[current][city] < nearest_dist:
                nearest_dist = dist[current][city]
                nearest_city = city

        
        tour.append(nearest_city)
        visited[nearest_city] = True
        current = nearest_city

    return tour

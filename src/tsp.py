
import math


class TSPInstance:

    def __init__(self, coords):

        self.coords = coords
        self.n = len(coords)  # number of cities

        self.dist = self._build_distance_matrix()

    def _build_distance_matrix(self):
        n = self.n
        
        dist = []
        for i in range(n):
            row = [0.0] * n
            dist.append(row)

        for i in range(n):
            for j in range(n):
                if i != j:
                    xi, yi = self.coords[i]
                    xj, yj = self.coords[j]
                    #distance: sqrt((xi-xj)^2 + (yi-yj)^2).
                    dx = xi - xj
                    dy = yi - yj
                    dist[i][j] = math.sqrt(dx * dx + dy * dy)
        return dist

    def tour_cost(self, tour):
        
        total = 0.0
        for k in range(len(tour)):
            a = tour[k]
            # (k + 1) % len(tour): after the last city the index go back to 0.
            b = tour[(k + 1) % len(tour)]
            total += self.dist[a][b]
        return total


def load_tsplib(path):
    
    #loads a TSPLIB file (.tsp) and returns a TSPInstance.
    coords = []
    reading_coords = False  

    with open(path, "r") as f:
        for line in f:
            line = line.strip() 

            # once we hit this line, the following lines are coordinates
            if line == "NODE_COORD_SECTION":
                reading_coords = True
                continue

            
            if line == "EOF" or line == "":
                break

            #format is "city_number  x  y".
            if reading_coords:
                parts = line.split()        
                x = float(parts[1])          
                y = float(parts[2])
                coords.append((x, y))

    return TSPInstance(coords)

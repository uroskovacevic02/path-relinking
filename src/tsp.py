"""
tsp.py - core structures for the Traveling Salesman Problem (TSP).

Defines:
  - how we store a problem instance (city coordinates),
  - the distance matrix between all pairs of cities,
  - a function that computes the length of a tour,
  - a loader for TSPLIB (.tsp) files.
"""

import math


class TSPInstance:
    """A single TSP instance: a set of cities given by coordinates."""

    def __init__(self, coords):
        # coords is a list of (x, y) pairs, e.g. [(0, 0), (1, 5), (3, 2)].
        # A city's index in the list is its "number" (0, 1, 2, ...).
        self.coords = coords
        self.n = len(coords)  # number of cities

        # Precompute the distance matrix so we don't recompute it every time.
        self.dist = self._build_distance_matrix()

    def _build_distance_matrix(self):
        """Builds an n x n matrix where dist[i][j] is the distance from city i to city j."""
        n = self.n
        # Start from a matrix filled with zeros: n rows, each row has n zeros.
        dist = []
        for i in range(n):
            row = [0.0] * n
            dist.append(row)

        for i in range(n):
            for j in range(n):
                if i != j:
                    xi, yi = self.coords[i]
                    xj, yj = self.coords[j]
                    # Euclidean distance: sqrt((xi-xj)^2 + (yi-yj)^2).
                    dx = xi - xj
                    dy = yi - yj
                    dist[i][j] = math.sqrt(dx * dx + dy * dy)
        return dist

    def tour_cost(self, tour):
        """
        Computes the total length of a tour.

        tour is a permutation of city indices, e.g. [0, 2, 1].
        The tour is closed: after the last city we return to the first one.
        """
        total = 0.0
        for k in range(len(tour)):
            a = tour[k]
            # (k + 1) % len(tour): after the last city the index wraps back to 0.
            b = tour[(k + 1) % len(tour)]
            total += self.dist[a][b]
        return total


def load_tsplib(path):
    """
    Loads a TSPLIB file (.tsp) and returns a TSPInstance.

    Supports only the EUC_2D type (cities given by x, y coordinates).
    """
    coords = []
    reading_coords = False  # whether we have reached the coordinates section

    with open(path, "r") as f:
        for line in f:
            line = line.strip()  # remove whitespace and newline from the ends

            # Once we hit this line, the following lines are coordinates.
            if line == "NODE_COORD_SECTION":
                reading_coords = True
                continue

            # End of file.
            if line == "EOF" or line == "":
                break

            # While reading coordinates: the format is "city_number  x  y".
            if reading_coords:
                parts = line.split()        # split on whitespace
                x = float(parts[1])         # parts[0] is the city number, we skip it
                y = float(parts[2])
                coords.append((x, y))

    return TSPInstance(coords)

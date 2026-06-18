
import random

from path_relinking import edge_set


class EliteSet:
    def __init__(self, instance, max_size=10, min_diff=3):
        self.instance = instance
        self.max_size = max_size      # how many tours we keep
        self.min_diff = min_diff      # min number of different edges to count as "diverse"
        self.members = []             

    def _difference(self, tour_a, tour_b):
        # how many edges of tour_a are NOT in tour_b
        ea = edge_set(tour_a)
        eb = edge_set(tour_b)

        diff = 0
        for edge in ea:
            if edge not in eb:
                diff += 1
        return diff

    def add(self, tour):
        cost = self.instance.tour_cost(tour)

        for c, t in self.members:
            if self._difference(tour, t) < self.min_diff: 
                if cost < c:
                    self.members.remove((c, t))
                    self.members.append((cost, tour))
                    self.members.sort(key=lambda x: x[0])
                return

        if len(self.members) < self.max_size:
            self.members.append((cost, tour))
            self.members.sort(key=lambda x: x[0])
            return

        # full: replace the worst tour if we are better than it
        worst_cost = self.members[-1][0]
        if cost < worst_cost:
            self.members[-1] = (cost, tour)
            self.members.sort(key=lambda x: x[0])

    def best(self):
        return self.members[0]        # (cost, tour)

    def random_member(self):
        cost, tour = random.choice(self.members)
        return tour

import os
import sys
import matplotlib.pyplot as plt

plt.switch_backend("Agg")        

sys.path.insert(0, os.path.dirname(__file__))
from tsp import load_tsplib      
from grasp import grasp_pr       

BASE = os.path.dirname(os.path.dirname(__file__))
RESULTS = os.path.join(BASE, "results")


def plot_tour(instance, tour, title, path):
    order = tour + [tour[0]]        # close the loop: end where we started

    xs = []
    ys = []
    for c in order:
        x, y = instance.coords[c]
        xs.append(x)
        ys.append(y)
    plt.figure()
    plt.plot(xs, ys, "-o", markersize=4)
    plt.title(title)
    plt.savefig(path)
    plt.close()


def plot_convergence(history, title, path):
    plt.figure()
    plt.plot(history)
    plt.xlabel("iteration")
    plt.ylabel("best length")
    plt.title(title)
    plt.savefig(path)
    plt.close()


if __name__ == "__main__":
    if not os.path.exists(RESULTS):
        os.makedirs(RESULTS)

    inst = load_tsplib(os.path.join(BASE, "data", "berlin52.tsp"))
    tour, cost, history = grasp_pr(inst, iterations=50,
                                   variant="back_and_forward", seed=1)

    plot_tour(inst, tour, f"berlin52  length={cost:.0f}",
              os.path.join(RESULTS, "tour_berlin52.png"))
    plot_convergence(history, "convergence (berlin52)",
                     os.path.join(RESULTS, "convergence_berlin52.png"))
    print("saved figures to results/")

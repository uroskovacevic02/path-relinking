"""
experiments.py - compares plain GRASP and the PR variants across instances.

For each instance and each method we run several seeds and report the
average / best tour length, the average gap to the known optimum, and time.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from tsp import load_tsplib
from grasp import grasp_pr

# folders (relative to the project root)
BASE = os.path.dirname(os.path.dirname(__file__))
DATA = os.path.join(BASE, "data")
RESULTS = os.path.join(BASE, "results")

# known optimal tour lengths (from TSPLIB)
OPTIMA = {
    "berlin52": 7542,
    "eil51": 426,
    "st70": 675,
    "kroA100": 21282,
}

# the methods we compare: a label and the grasp_pr arguments
METHODS = [
    ("GRASP (no PR)", dict(use_pr=False)),
    ("forward", dict(use_pr=True, variant="forward")),
    ("backward", dict(use_pr=True, variant="backward")),
    ("back_and_forward", dict(use_pr=True, variant="back_and_forward")),
    ("mixed", dict(use_pr=True, variant="mixed")),
]


def run_one(instance, label, kwargs, iterations, seeds):
    costs = []
    total_time = 0.0
    for s in range(seeds):
        t0 = time.time()
        _, cost, _ = grasp_pr(instance, iterations=iterations, seed=s, **kwargs)
        total_time += time.time() - t0
        costs.append(cost)

    avg = sum(costs) / len(costs)
    best = min(costs)
    return avg, best, total_time / seeds


def run_experiment(instance_names, iterations=30, seeds=5):
    if not os.path.exists(RESULTS):
        os.makedirs(RESULTS)

    lines = []
    for name in instance_names:
        instance = load_tsplib(os.path.join(DATA, name + ".tsp"))
        opt = OPTIMA[name]

        header = f"\n=== {name}  (n={instance.n}, optimum={opt}) ==="
        print(header)
        print(f"{'method':18s} | {'avg':>9s} | {'best':>9s} | {'gap%':>6s} | {'time':>6s}")
        print("-" * 60)
        lines.append(header)

        for label, kwargs in METHODS:
            avg, best, t = run_one(instance, label, kwargs, iterations, seeds)
            gap = 100 * (avg - opt) / opt
            row = f"{label:18s} | {avg:9.1f} | {best:9.1f} | {gap:5.2f}% | {t:5.1f}s"
            print(row)
            lines.append(row)

    # save a copy of the table
    out = os.path.join(RESULTS, "experiments.txt")
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nSaved results to {out}")


if __name__ == "__main__":
    run_experiment(["eil51", "berlin52", "st70", "kroA100"], iterations=30, seeds=5)

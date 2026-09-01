import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from weekend_optimizer.hungarian import minimize, solve  # noqa: E402


def brute_force_min(cost):
    """O(n!) reference solver for small matrices."""
    from itertools import permutations
    n = len(cost)
    best = None
    for perm in permutations(range(n)):
        total = sum(cost[i][perm[i]] for i in range(n))
        if best is None or total < best:
            best = total
    return best


def test_trivial():
    assert minimize([]) == ([], 0)
    assert minimize([[5]]) == ([0], 5)


def test_known_small():
    cost = [
        [4, 1, 3],
        [2, 0, 5],
        [3, 2, 2],
    ]
    assignment, total = minimize(cost)
    assert total == 5                     # 4 + 0 + ... optimal is 4+0+... = 5
    assert sorted(assignment) == [0, 1, 2]  # a valid permutation


def test_matches_brute_force():
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 6)
        cost = [[rng.randint(0, 20) for _ in range(n)] for _ in range(n)]
        _, total = minimize(cost)
        assert total == brute_force_min(cost)


def test_maximize():
    value = [
        [10, 1],
        [1, 10],
    ]
    assignment, total = solve(value, maximize=True)
    assert assignment == [0, 1]
    assert total == 20


def test_more_rows_than_cols_drops_least_valuable():
    # 3 activities, 2 slots. The worst activity should be dropped.
    value = [
        [9, 8],   # great everywhere
        [7, 6],   # good
        [1, 1],   # weak -> should be the one left out
    ]
    assignment, total = solve(value, maximize=True)
    assert assignment[2] is None
    assert total == 9 + 6 or total == 8 + 7  # both keep the two strong rows


def test_more_cols_than_rows_leaves_slots_empty():
    value = [
        [5, 1, 1],
        [1, 5, 1],
    ]
    assignment, total = solve(value, maximize=True)
    assert None not in assignment          # every activity is scheduled
    assert total == 10


def test_matches_scipy_if_available():
    try:
        import numpy as np
        from scipy.optimize import linear_sum_assignment
    except ImportError:
        return  # scipy not installed; skip silently
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randint(2, 12)
        cost = [[rng.randint(0, 50) for _ in range(n)] for _ in range(n)]
        _, total = minimize(cost)
        r, c = linear_sum_assignment(np.array(cost))
        assert total == sum(cost[r[i]][c[i]] for i in range(n))

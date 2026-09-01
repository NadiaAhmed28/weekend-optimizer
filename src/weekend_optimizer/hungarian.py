"""
Hungarian algorithm (Kuhn-Munkres) for the linear assignment problem.

Pure-Python, O(n^3) implementation with no third-party dependencies.

Given an n x n cost matrix, `minimize` finds the one-to-one assignment of
rows to columns that minimizes total cost. `solve` wraps it to handle
rectangular inputs and maximization, which is what the scheduler needs.
"""

from __future__ import annotations

INF = float("inf")


def minimize(cost):
    """Minimize total cost over a square matrix.

    Args:
        cost: n x n matrix (list of lists) of numbers.

    Returns:
        (assignment, total) where assignment[i] is the column assigned to
        row i, and total is the summed cost of that assignment.

    This is the O(n^3) potentials-and-augmenting-paths formulation. It runs
    one row at a time, keeping dual potentials u (rows) and v (columns) so
    that reduced costs stay non-negative, and augments along the shortest
    path to a free column each iteration.
    """
    n = len(cost)
    if n == 0:
        return [], 0
    for row in cost:
        if len(row) != n:
            raise ValueError("cost matrix must be square")

    # 1-indexed internally; index 0 is a sentinel used to start each path.
    u = [0.0] * (n + 1)          # row potentials
    v = [0.0] * (n + 1)          # column potentials
    p = [0] * (n + 1)            # p[j] = row currently matched to column j
    way = [0] * (n + 1)          # predecessor column, used to walk back

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (n + 1)   # cheapest reduced cost to reach each column
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            # Shift potentials so the reached column becomes tight.
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:       # reached a free column: stop and augment
                break
        # Walk the augmenting path back, flipping matches.
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1

    assignment = [0] * n
    for j in range(1, n + 1):
        if p[j] != 0:
            assignment[p[j] - 1] = j - 1
    total = sum(cost[i][assignment[i]] for i in range(n))
    return assignment, total


def solve(matrix, maximize=False):
    """Solve a possibly-rectangular assignment problem.

    Args:
        matrix: n x m matrix of numbers.
        maximize: if True, maximize total value instead of minimizing cost.

    Returns:
        (assignment, total) where assignment[i] is the column assigned to
        row i, or None when row i is left unassigned (only happens when
        there are more rows than columns). total sums the real, non-padding
        assignments only.

    Rectangular inputs are padded to a square with neutral 0-cost dummy
    rows/columns. Because every dummy cell has the same cost, dummies never
    bump a real row off a better column; they just absorb the surplus, which
    means the surplus rows dropped are always the least valuable ones.
    """
    if not matrix or not matrix[0]:
        return [], 0
    n = len(matrix)
    m = len(matrix[0])
    size = max(n, m)

    if maximize:
        hi = max(max(row) for row in matrix)
        square = [
            [(hi - matrix[i][j]) if (i < n and j < m) else 0.0
             for j in range(size)]
            for i in range(size)
        ]
    else:
        square = [
            [matrix[i][j] if (i < n and j < m) else 0.0
             for j in range(size)]
            for i in range(size)
        ]

    col_for_row, _ = minimize(square)

    assignment = []
    total = 0.0
    for i in range(n):
        j = col_for_row[i]
        if j < m:
            assignment.append(j)
            total += matrix[i][j]
        else:
            assignment.append(None)   # matched to a padding column
    return assignment, total

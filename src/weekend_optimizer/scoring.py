"""Combine event value (maximize) and flight cost (minimize) into one score.

Both signals are normalized across every city/weekend cell to a 0..1 range so
they are comparable, then blended with a tunable weight. The result is a value
matrix the Hungarian solver maximizes.
"""

from __future__ import annotations

from dataclasses import dataclass

EVENT_WEIGHT = {
    "favorite_artist": 10.0,
    "festival": 8.0,
    "concert": 5.0,
}


@dataclass
class Weights:
    """How much to care about catching events vs paying less for flights."""
    event: float = 0.5
    flight: float = 0.5

    def normalized(self) -> tuple[float, float]:
        total = (self.event + self.flight) or 1.0
        return self.event / total, self.flight / total


def event_value(events) -> float:
    return sum(EVENT_WEIGHT.get(e.category, 2.0) for e in events)


def _normalize(matrix):
    """Scale all non-None cells to 0..1; None stays None."""
    flat = [v for row in matrix for v in row if v is not None]
    if not flat:
        return [[0.0 for _ in row] for row in matrix]
    lo, hi = min(flat), max(flat)
    span = (hi - lo) or 1.0
    return [[((v - lo) / span if v is not None else None) for v in row] for row in matrix]


def build_value_matrix(raw_event, raw_flight, weights: Weights):
    """Blend normalized event value and flight cheapness into a value matrix.

    A missing flight price is treated as the worst possible (cheapness 0), so
    unreachable city/weekend pairs are naturally avoided.
    """
    w_event, w_flight = weights.normalized()
    ev = _normalize(raw_event)
    fl = _normalize(raw_flight)
    n = len(raw_event)
    m = len(raw_event[0]) if raw_event else 0
    out = []
    for i in range(n):
        row = []
        for j in range(m):
            e = ev[i][j] or 0.0
            f = fl[i][j]
            cheapness = (1.0 - f) if f is not None else 0.0
            row.append(100.0 * (w_event * e + w_flight * cheapness))
        out.append(row)
    return out

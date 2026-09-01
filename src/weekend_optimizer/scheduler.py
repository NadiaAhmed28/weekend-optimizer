"""Turn a weekend into an assignment problem and solve it.

The scheduler builds a value matrix (how good is activity a in block b?),
then hands it to the Hungarian solver to maximize total value across the
whole weekend, one activity per block.
"""

from __future__ import annotations

from dataclasses import dataclass

from .hungarian import solve
from .models import Activity, TimeBlock, ENERGY, default_weekend


def score(activity: Activity, block: TimeBlock) -> float:
    """How good is it to do `activity` during `block`? Higher is better.

    This is the one function to customize. The defaults reward:
      - putting an activity in its preferred part of the day,
      - matching the activity's energy demand to the block's energy,
      - doing high-priority things at all.
    """
    # Time-of-day fit.
    if activity.preferred_period == block.period:
        period_fit = 10.0
    elif activity.preferred_period == "any":
        period_fit = 5.0
    else:
        period_fit = 0.0

    # Energy fit: full marks when demand meets availability, less as they
    # diverge. Distance is 0, 1, or 2 on the low/medium/high scale.
    distance = abs(ENERGY[activity.energy] - ENERGY[block.energy])
    energy_fit = 5.0 - 2.5 * distance

    # Priority: a flat reward for scheduling important things.
    priority_fit = 2.0 * activity.priority

    return period_fit + energy_fit + priority_fit


@dataclass
class Assignment:
    block: TimeBlock
    activity: Activity
    value: float


@dataclass
class Schedule:
    assignments: list[Assignment]
    unscheduled: list[Activity]
    total_value: float

    def show(self) -> str:
        lines = []
        for a in sorted(self.assignments, key=lambda x: x.block.label):
            lines.append(f"{a.block.label:<20} {a.activity.name:<24} (+{a.value:.1f})")
        if self.unscheduled:
            names = ", ".join(a.name for a in self.unscheduled)
            lines.append(f"\nNot scheduled: {names}")
        lines.append(f"\nTotal value: {self.total_value:.1f}")
        return "\n".join(lines)


def optimize_weekend(
    activities: list[Activity],
    blocks: list[TimeBlock] | None = None,
) -> Schedule:
    """Assign activities to time blocks to maximize total weekend value.

    Rows are activities, columns are time blocks. When they differ in count,
    the solver leaves the surplus unscheduled (extra activities) or the
    surplus empty (extra blocks).
    """
    if blocks is None:
        blocks = default_weekend()

    value_matrix = [[score(a, b) for b in blocks] for a in activities]
    row_to_col, total = solve(value_matrix, maximize=True)

    assignments = []
    unscheduled = []
    for i, activity in enumerate(activities):
        col = row_to_col[i]
        if col is None:
            unscheduled.append(activity)
        else:
            assignments.append(
                Assignment(block=blocks[col], activity=activity, value=value_matrix[i][col])
            )
    return Schedule(assignments=assignments, unscheduled=unscheduled, total_value=total)

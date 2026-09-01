"""Run a sample weekend through the optimizer.

    python examples/sample_weekend.py
"""

import sys
from pathlib import Path

# Make the package importable when running the file directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from weekend_optimizer import Activity, optimize_weekend  # noqa: E402


def main():
    activities = [
        Activity("Long run",            preferred_period="morning",   energy="high",   priority=4),
        Activity("Deep work: side project", preferred_period="morning", energy="high", priority=5),
        Activity("Grocery run",         preferred_period="afternoon", energy="medium", priority=3),
        Activity("Laundry",             preferred_period="afternoon", energy="low",    priority=2),
        Activity("Call family",         preferred_period="evening",   energy="low",    priority=4),
        Activity("Read",                preferred_period="evening",   energy="low",    priority=2),
        Activity("Meal prep",           preferred_period="any",       energy="medium", priority=3),
    ]

    schedule = optimize_weekend(activities)
    print(schedule.show())


if __name__ == "__main__":
    main()

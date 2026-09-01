import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from weekend_optimizer import Activity, TimeBlock, optimize_weekend, score  # noqa: E402


def test_period_preference_is_rewarded():
    morning = TimeBlock("Saturday", "morning", "high")
    evening = TimeBlock("Saturday", "evening", "low")
    a = Activity("Run", preferred_period="morning", energy="high", priority=3)
    assert score(a, morning) > score(a, evening)


def test_each_block_used_once():
    activities = [Activity(f"task{i}") for i in range(6)]
    schedule = optimize_weekend(activities)
    labels = [a.block.label for a in schedule.assignments]
    assert len(labels) == len(set(labels))   # no block reused


def test_surplus_activities_are_unscheduled():
    activities = [Activity(f"task{i}") for i in range(8)]  # 8 > 6 blocks
    schedule = optimize_weekend(activities)
    assert len(schedule.assignments) == 6
    assert len(schedule.unscheduled) == 2

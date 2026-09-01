"""Data models for the weekend scheduling problem."""

from __future__ import annotations

from dataclasses import dataclass, field

# Ordered so scoring can compare "distance" between energy levels.
ENERGY = {"low": 0, "medium": 1, "high": 2}
PERIODS = ("morning", "afternoon", "evening")


@dataclass
class Activity:
    """Something you want to get done this weekend.

    preferred_period: "morning" | "afternoon" | "evening" | "any"
    energy:           demand of the activity: "low" | "medium" | "high"
    priority:         1 (nice-to-have) .. 5 (must-do)
    """
    name: str
    preferred_period: str = "any"
    energy: str = "medium"
    priority: int = 3


@dataclass
class TimeBlock:
    """A slot in the weekend you can fill with one activity."""
    day: str          # e.g. "Saturday"
    period: str       # one of PERIODS
    energy: str = "medium"   # how much energy you tend to have then

    @property
    def label(self) -> str:
        return f"{self.day} {self.period}"


def default_weekend() -> list[TimeBlock]:
    """A typical energy curve: mornings high, evenings low."""
    blocks = []
    curve = {"morning": "high", "afternoon": "medium", "evening": "low"}
    for day in ("Saturday", "Sunday"):
        for period in PERIODS:
            blocks.append(TimeBlock(day=day, period=period, energy=curve[period]))
    return blocks

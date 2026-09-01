"""Weekend Optimizer: schedule a weekend with the Hungarian algorithm."""

from .hungarian import minimize, solve
from .models import Activity, TimeBlock, default_weekend
from .scheduler import optimize_weekend, score, Schedule, Assignment

__all__ = [
    "minimize",
    "solve",
    "Activity",
    "TimeBlock",
    "default_weekend",
    "optimize_weekend",
    "score",
    "Schedule",
    "Assignment",
]

__version__ = "0.1.0"

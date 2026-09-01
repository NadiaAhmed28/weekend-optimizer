"""Weekend Optimizer: plan a semester of weekend trips with the Hungarian algorithm."""

from .hungarian import minimize, solve
from .models import City, Weekend, MADRID, SUGGESTED_CITIES, semester_weekends
from .providers import (
    Event,
    EventProvider,
    FlightProvider,
    SampleEventProvider,
    SampleFlightProvider,
)
from .scoring import Weights, build_value_matrix, event_value
from .optimizer import plan_trips, TripPlan, TripAssignment

__all__ = [
    "minimize",
    "solve",
    "City",
    "Weekend",
    "MADRID",
    "SUGGESTED_CITIES",
    "semester_weekends",
    "Event",
    "EventProvider",
    "FlightProvider",
    "SampleEventProvider",
    "SampleFlightProvider",
    "Weights",
    "build_value_matrix",
    "event_value",
    "plan_trips",
    "TripPlan",
    "TripAssignment",
]

__version__ = "0.2.0"

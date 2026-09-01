"""Plan a semester of weekend trips.

Assign each city to a weekend so total value (good events, cheap flights) is
maximized, one city per weekend, using the Hungarian algorithm. Extra cities
are left unplaced; extra weekends are left free.
"""

from __future__ import annotations

from dataclasses import dataclass

from .hungarian import solve
from .models import City, Weekend, MADRID
from .providers import (
    Event,
    EventProvider,
    FlightProvider,
    SampleEventProvider,
    SampleFlightProvider,
)
from .scoring import Weights, build_value_matrix, event_value


@dataclass
class TripAssignment:
    weekend: Weekend
    city: City
    price: float | None
    events: list[Event]
    score: float


@dataclass
class TripPlan:
    assignments: list[TripAssignment]
    unplaced_cities: list[City]
    free_weekends: list[Weekend]
    total_score: float

    def show(self) -> str:
        lines = []
        for a in sorted(self.assignments, key=lambda x: x.weekend.index):
            ev = a.events[0].name if a.events else "-"
            price = f"EUR {a.price:.0f}" if a.price is not None else "n/a"
            lines.append(f"{a.weekend.label}  ->  {a.city.name:<11} {price:>8}   {ev}")
        if self.unplaced_cities:
            lines.append("\nNot placed: " + ", ".join(c.name for c in self.unplaced_cities))
        if self.free_weekends:
            lines.append("Free weekends: " + ", ".join(w.label for w in self.free_weekends))
        lines.append(f"\nTotal score: {self.total_score:.1f}")
        return "\n".join(lines)


def plan_trips(
    cities: list[City],
    weekends: list[Weekend],
    origin: City = MADRID,
    flight_provider: FlightProvider | None = None,
    event_provider: EventProvider | None = None,
    weights: Weights | None = None,
) -> TripPlan:
    flight_provider = flight_provider or SampleFlightProvider()
    event_provider = event_provider or SampleEventProvider()
    weights = weights or Weights()

    usable = [w for w in weekends if w.available]

    raw_event, raw_flight = [], []
    events_cache, price_cache = {}, {}
    for i, city in enumerate(cities):
        erow, frow = [], []
        for j, wk in enumerate(usable):
            evs = event_provider.events(city, wk)
            price = flight_provider.price(origin, city, wk)
            events_cache[(i, j)] = evs
            price_cache[(i, j)] = price
            erow.append(event_value(evs))
            frow.append(price)
        raw_event.append(erow)
        raw_flight.append(frow)

    value = build_value_matrix(raw_event, raw_flight, weights)
    row_to_col, total = solve(value, maximize=True)

    assignments, unplaced, used = [], [], set()
    for i, city in enumerate(cities):
        j = row_to_col[i]
        if j is None:
            unplaced.append(city)
        else:
            used.add(j)
            assignments.append(
                TripAssignment(
                    weekend=usable[j],
                    city=city,
                    price=price_cache[(i, j)],
                    events=events_cache[(i, j)],
                    score=value[i][j],
                )
            )
    free = [wk for j, wk in enumerate(usable) if j not in used]
    return TripPlan(
        assignments=assignments,
        unplaced_cities=unplaced,
        free_weekends=free,
        total_score=total,
    )

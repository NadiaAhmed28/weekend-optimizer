"""Flight-price and event data providers.

Two small interfaces plus deterministic sample implementations. The optimizer
only knows about the interfaces, so real sources can be dropped in later
without touching the algorithm:

  events  -> Ticketmaster Discovery API (free key), Bandsintown, etc.
  flights -> a paid tier / affiliate feed / scraper once you pick one

The sample providers return reproducible fake data so the whole thing runs
and is testable today.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .models import City, Weekend


@dataclass(frozen=True)
class Event:
    name: str
    category: str          # "favorite_artist" | "festival" | "concert"
    city: str
    weekend_index: int


class EventProvider:
    """Return the events happening in a city on a given weekend."""

    def events(self, city: City, weekend: Weekend) -> list[Event]:
        raise NotImplementedError


class FlightProvider:
    """Return a round-trip price estimate in EUR, or None if unavailable."""

    def price(self, origin: City, dest: City, weekend: Weekend) -> float | None:
        raise NotImplementedError


def _hash(*parts) -> int:
    raw = "|".join(str(p) for p in parts).encode()
    return int(hashlib.md5(raw).hexdigest()[:8], 16)


class SampleFlightProvider(FlightProvider):
    """Deterministic pseudo-prices: nearby cities cheaper, small weekly swing."""

    BASE = {  # rough round-trip baseline from Madrid, EUR
        "LIS": 60, "OPO": 70, "BCN": 50, "SVQ": 45,
        "CDG": 110, "FCO": 120, "BER": 140, "AMS": 130,
        "LHR": 120, "RAK": 90, "MXP": 115, "VIE": 150,
    }

    def price(self, origin: City, dest: City, weekend: Weekend) -> float | None:
        base = self.BASE.get(dest.airport, 130)
        swing = _hash(dest.airport, weekend.index) % 80 - 20   # -20..+59
        return float(max(30, base + swing))


class SampleEventProvider(EventProvider):
    """A few seeded events, including favorite-artist shows worth chasing."""

    def __init__(self, favorite_artists: list[str] | None = None):
        self.favorite_artists = favorite_artists or []
        # keyed by (airport, weekend index)
        self._seed = {
            ("LIS", 2): Event("Lisbon indie night", "concert", "Lisbon", 2),
            ("SVQ", 3): Event("Feria de Sevilla", "festival", "Seville", 3),
            ("AMS", 4): Event("Amsterdam Dance Event", "festival", "Amsterdam", 4),
            ("BER", 5): Event("Favorite artist live", "favorite_artist", "Berlin", 5),
            ("FCO", 7): Event("Rome Jazz Festival", "festival", "Rome", 7),
        }

    def events(self, city: City, weekend: Weekend) -> list[Event]:
        hit = self._seed.get((city.airport, weekend.index))
        return [hit] if hit else []

"""Data models for the weekend travel optimizer."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class City:
    name: str
    country: str
    airport: str          # IATA code, e.g. "LIS"

    def __str__(self) -> str:
        return f"{self.name} ({self.country})"


@dataclass(frozen=True)
class Weekend:
    index: int
    start: date           # Friday
    end: date             # Sunday
    available: bool = True

    @property
    def label(self) -> str:
        return f"W{self.index:02d} {self.start.strftime('%b %d')}-{self.end.strftime('%d')}"


def semester_weekends(start: date, end: date) -> list[Weekend]:
    """Every Friday-to-Sunday weekend between start and end."""
    d = start
    while d.weekday() != 4:            # 4 = Friday
        d += timedelta(days=1)
    weekends = []
    i = 1
    while d <= end:
        weekends.append(Weekend(index=i, start=d, end=d + timedelta(days=2)))
        d += timedelta(days=7)
        i += 1
    return weekends


MADRID = City("Madrid", "Spain", "MAD")

# Built-in candidates for the "suggest destinations too" path: cities that
# make sense as a weekend trip from Madrid.
SUGGESTED_CITIES = [
    City("Lisbon", "Portugal", "LIS"),
    City("Porto", "Portugal", "OPO"),
    City("Barcelona", "Spain", "BCN"),
    City("Seville", "Spain", "SVQ"),
    City("Paris", "France", "CDG"),
    City("Rome", "Italy", "FCO"),
    City("Berlin", "Germany", "BER"),
    City("Amsterdam", "Netherlands", "AMS"),
    City("London", "United Kingdom", "LHR"),
    City("Marrakech", "Morocco", "RAK"),
    City("Milan", "Italy", "MXP"),
    City("Vienna", "Austria", "VIE"),
]

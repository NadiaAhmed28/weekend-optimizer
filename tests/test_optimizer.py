import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from weekend_optimizer import (  # noqa: E402
    City,
    Weights,
    plan_trips,
    semester_weekends,
)
from weekend_optimizer.scoring import build_value_matrix  # noqa: E402


def _cities(n):
    base = [
        City("Lisbon", "Portugal", "LIS"),
        City("Barcelona", "Spain", "BCN"),
        City("Berlin", "Germany", "BER"),
        City("Rome", "Italy", "FCO"),
        City("Paris", "France", "CDG"),
        City("Amsterdam", "Netherlands", "AMS"),
    ]
    return base[:n]


def test_weekends_are_fri_to_sun():
    wks = semester_weekends(date(2027, 1, 18), date(2027, 3, 1))
    assert wks and all(w.start.weekday() == 4 for w in wks)   # Friday
    assert all(w.end.weekday() == 6 for w in wks)             # Sunday


def test_one_city_per_weekend():
    wks = semester_weekends(date(2027, 1, 18), date(2027, 5, 15))
    plan = plan_trips(_cities(4), wks)
    used = [a.weekend.index for a in plan.assignments]
    assert len(used) == len(set(used))
    assert len(plan.assignments) == 4


def test_surplus_cities_are_unplaced():
    wks = semester_weekends(date(2027, 1, 18), date(2027, 2, 10))[:3]
    plan = plan_trips(_cities(6), wks)
    assert len(plan.assignments) == 3
    assert len(plan.unplaced_cities) == 3


def test_extra_weekends_left_free():
    wks = semester_weekends(date(2027, 1, 18), date(2027, 5, 15))
    plan = plan_trips(_cities(3), wks)
    assert not plan.unplaced_cities
    assert len(plan.free_weekends) == len(wks) - 3


def test_event_weighting_chases_favorite_artist():
    # The sample provider seeds a favorite-artist show in Berlin on weekend 5.
    wks = semester_weekends(date(2027, 1, 18), date(2027, 5, 15))
    plan = plan_trips(_cities(6), wks, weights=Weights(event=0.95, flight=0.05))
    berlin = next(a for a in plan.assignments if a.city.name == "Berlin")
    assert any(e.category == "favorite_artist" for e in berlin.events)


def test_build_value_matrix_handles_missing_price():
    m = build_value_matrix([[8.0, 0.0]], [[None, 50.0]], Weights(0.5, 0.5))
    assert len(m) == 1 and len(m[0]) == 2
    assert all(v >= 0 for v in m[0])

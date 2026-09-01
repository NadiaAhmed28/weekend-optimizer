"""Plan a semester of weekend trips from Madrid.

    python examples/plan_semester.py
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from weekend_optimizer import (  # noqa: E402
    City,
    SUGGESTED_CITIES,
    SampleEventProvider,
    Weights,
    plan_trips,
    semester_weekends,
)


def main():
    # Spring semester in Madrid.
    weekends = semester_weekends(date(2027, 1, 18), date(2027, 5, 15))

    # Your must-visit list...
    my_list = [
        City("Lisbon", "Portugal", "LIS"),
        City("Barcelona", "Spain", "BCN"),
        City("Berlin", "Germany", "BER"),
    ]
    # ...plus the tool's suggestions, de-duplicated by name.
    names = {c.name for c in my_list}
    cities = my_list + [c for c in SUGGESTED_CITIES if c.name not in names]

    plan = plan_trips(
        cities=cities,
        weekends=weekends,
        weights=Weights(event=0.6, flight=0.4),   # lean slightly toward events
        event_provider=SampleEventProvider(favorite_artists=["your favorite"]),
    )
    print(plan.show())


if __name__ == "__main__":
    main()

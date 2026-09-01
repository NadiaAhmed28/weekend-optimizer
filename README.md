# Weekend Optimizer

Plan a semester of weekend trips by treating it as an assignment problem and
solving it with the Hungarian algorithm.

You're based in one city (Madrid, in the default example) for a semester. You
have a set of weekends and a set of places you'd like to visit. Each
city/weekend pairing is worth more when something good is happening there
(a festival, an artist you like) and when the flight is cheap. The optimizer
scores every pairing and assigns one city per weekend to maximize total value
across the whole semester.

The Hungarian (Kuhn-Munkres) solver is implemented from scratch in pure
Python, O(n^3), with no third-party dependencies in the core.

## How it works

1. **Model** the semester as cities (rows) and weekends (columns).
2. **Score** each city/weekend pair: normalize event value and flight cost
   across all pairs, then blend them with a weight you control.
3. **Solve** the value matrix with the Hungarian algorithm for the highest
   total-value assignment.

More cities than weekends: the least valuable cities are left unplaced. More
weekends than cities: the extra weekends stay free. Both fall out of padding
the matrix to a square.

## Data providers

Flight prices and events come through two small interfaces
(`FlightProvider`, `EventProvider`), so the optimizer is decoupled from any
one data source. The repo ships deterministic sample providers so everything
runs and is testable immediately. Real sources plug in behind the same
interfaces:

- **Events** — the Ticketmaster Discovery API gives a free key on signup with
  global coverage; searching by artist name covers "is someone I like
  playing." Favorite artists can later be pulled from Spotify.
- **Flights** — flight-price APIs are in flux (Amadeus and Kiwi closed their
  free developer tiers in 2026), so the flight provider is a clean seam to
  drop in whatever source you settle on.

## Install

```bash
git clone https://github.com/<your-username>/weekend-optimizer.git
cd weekend-optimizer
```

The core has no dependencies. For the tests (the solver is validated against
`scipy.optimize.linear_sum_assignment`):

```bash
pip install -r requirements-dev.txt
```

## Usage

```python
from datetime import date
from weekend_optimizer import City, plan_trips, semester_weekends, Weights

weekends = semester_weekends(date(2027, 1, 18), date(2027, 5, 15))
cities = [
    City("Lisbon", "Portugal", "LIS"),
    City("Barcelona", "Spain", "BCN"),
    City("Berlin", "Germany", "BER"),
]

plan = plan_trips(cities, weekends, weights=Weights(event=0.6, flight=0.4))
print(plan.show())
```

Run the full example:

```bash
python examples/plan_semester.py
```

Sample output:

```
W03 Feb 05-07  ->  Seville     EUR 40    Feria de Sevilla
W05 Feb 19-21  ->  Berlin      EUR 149   Favorite artist live
W07 Mar 05-07  ->  Rome        EUR 128   Rome Jazz Festival
W09 Mar 19-21  ->  Barcelona   EUR 34    -
...
Total score: 522.5
```

## Layout

```
src/weekend_optimizer/
  hungarian.py    from-scratch Hungarian algorithm (minimize + solve)
  models.py       City, Weekend, semester weekend generation
  providers.py    Flight/Event interfaces + sample implementations
  scoring.py      normalize + blend events and flight cost into a value matrix
  optimizer.py    build the matrix from providers and solve
examples/         runnable demo
tests/            unit tests, solver validated against scipy
```

## Tests

```bash
python -m pytest tests/ -q
```

## Roadmap

- Ticketmaster Discovery provider for real events
- A real flight-price provider behind `FlightProvider`
- Pull favorite artists from Spotify to drive event search
- Mark weekends as no-travel; pin a city to a fixed weekend
- FastAPI backend + React front end to enter trips and view the plan
- Export the plan to `.ics` / Google Calendar

## License

MIT

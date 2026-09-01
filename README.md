# Weekend Optimizer

Schedule a weekend by treating it as an assignment problem and solving it with
the Hungarian algorithm.

You have time blocks (Saturday morning, Sunday evening, ...) and a list of
things you want to get done. Each activity is worth more in some blocks than
others — a run is better in the morning, a call home is better in the evening.
The optimizer scores every activity/block pair and finds the one-to-one
assignment that maximizes total value across the whole weekend.

The Hungarian (Kuhn-Munkres) solver is implemented from scratch in pure Python,
O(n^3), with no third-party dependencies in the core.

## How it works

1. **Model** the weekend as activities (rows) and time blocks (columns).
2. **Score** each pair with a customizable value function that rewards
   time-of-day fit, energy fit, and priority.
3. **Solve** the resulting value matrix with the Hungarian algorithm to get the
   assignment with the highest total value.

When there are more activities than blocks, the least valuable activities are
left unscheduled. When there are more blocks than activities, the extra blocks
stay empty. Both fall out of padding the matrix to a square.

## Install

```bash
git clone https://github.com/<your-username>/weekend-optimizer.git
cd weekend-optimizer
```

The core has no dependencies. For the tests (correctness is validated against
`scipy.optimize.linear_sum_assignment`):

```bash
pip install -r requirements-dev.txt
```

## Usage

```python
from weekend_optimizer import Activity, optimize_weekend

activities = [
    Activity("Long run",   preferred_period="morning", energy="high", priority=4),
    Activity("Side project", preferred_period="morning", energy="high", priority=5),
    Activity("Call family", preferred_period="evening", energy="low",  priority=4),
]

schedule = optimize_weekend(activities)
print(schedule.show())
```

Run the full example:

```bash
python examples/sample_weekend.py
```

Sample output:

```
Saturday morning     Deep work: side project  (+25.0)
Saturday afternoon   Grocery run              (+21.0)
Saturday evening     Call family              (+23.0)
Sunday morning       Long run                 (+23.0)
Sunday afternoon     Laundry                  (+16.5)
Sunday evening       Read                     (+19.0)

Not scheduled: Meal prep
Total value: 127.5
```

## Layout

```
src/weekend_optimizer/
  hungarian.py    from-scratch Hungarian algorithm (minimize + solve)
  models.py       Activity, TimeBlock, default weekend
  scheduler.py    scoring + optimize_weekend
examples/         runnable demo
tests/            unit tests, validated against scipy
```

The scoring function in `scheduler.py` is the part meant to be tuned — it is a
single function so preferences are easy to change.

## Tests

```bash
python -m pytest tests/ -q
```

Tests check the solver against a brute-force reference on small matrices and
against scipy on larger random ones.

## Roadmap

- FastAPI backend exposing the optimizer
- React front end to enter activities and view the schedule
- Learn scoring weights from user feedback instead of hand-tuning them
- Hard constraints (fixed events) and multi-block activities
- Export the schedule to `.ics` / Google Calendar

## License

MIT

"""FastAPI backend exposing the trip optimizer."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from typing import Optional

from .optimizer import plan_trips
from .models import City, MADRID, SUGGESTED_CITIES, semester_weekends
from .providers import BudgetCappedFlightProvider, SampleEventProvider, SampleFlightProvider
from .scoring import Weights

app = FastAPI(title="Weekend Optimizer")

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CityIn(BaseModel):
    name: str
    country: str = "Europe"
    airport: str


class PlanRequest(BaseModel):
    cities: list[CityIn]
    start_date: date
    end_date: date
    origin: Optional[CityIn] = None
    event_weight: float = 0.6
    flight_weight: float = 0.4
    favorite_artists: list[str] = []
    max_budget: Optional[float] = None


class EventOut(BaseModel):
    name: str
    category: str


class CityOut(BaseModel):
    name: str
    country: str
    airport: str


class WeekendOut(BaseModel):
    index: int
    label: str
    start: date
    end: date


class AssignmentOut(BaseModel):
    weekend: WeekendOut
    city: CityOut
    price: Optional[float]
    events: list[EventOut]
    score: float


class PlanResponse(BaseModel):
    assignments: list[AssignmentOut]
    unplaced_cities: list[CityOut]
    free_weekends: list[WeekendOut]
    total_score: float


def _weekend_out(wk) -> WeekendOut:
    return WeekendOut(index=wk.index, label=wk.label, start=wk.start, end=wk.end)


def _city_out(city: City) -> CityOut:
    return CityOut(name=city.name, country=city.country, airport=city.airport)


@app.post("/plan")
def plan_trips_endpoint(request: PlanRequest) -> PlanResponse:
    """Plan a semester of weekend trips."""
    cities = [City(c.name, c.country, c.airport) for c in request.cities]
    origin = City(request.origin.name, request.origin.country, request.origin.airport) if request.origin else MADRID
    weekends = semester_weekends(request.start_date, request.end_date)
    weights = Weights(event=request.event_weight, flight=request.flight_weight)

    flight_provider = SampleFlightProvider()
    if request.max_budget is not None:
        flight_provider = BudgetCappedFlightProvider(flight_provider, request.max_budget)

    plan = plan_trips(
        cities,
        weekends,
        origin=origin,
        weights=weights,
        event_provider=SampleEventProvider(request.favorite_artists),
        flight_provider=flight_provider,
    )
    return PlanResponse(
        assignments=[
            AssignmentOut(
                weekend=_weekend_out(a.weekend),
                city=_city_out(a.city),
                price=a.price,
                events=[EventOut(name=e.name, category=e.category) for e in a.events],
                score=a.score,
            )
            for a in sorted(plan.assignments, key=lambda x: x.weekend.index)
        ],
        unplaced_cities=[_city_out(c) for c in plan.unplaced_cities],
        free_weekends=[_weekend_out(w) for w in plan.free_weekends],
        total_score=plan.total_score,
    )


@app.get("/suggested-cities")
def suggested_cities() -> list[CityOut]:
    return [_city_out(c) for c in SUGGESTED_CITIES]


@app.get("/health")
def health_check():
    return {"status": "ok"}

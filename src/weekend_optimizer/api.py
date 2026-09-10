"""FastAPI backend exposing the trip optimizer."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date

from .optimizer import plan_trips
from .models import City, semester_weekends
from .providers import SampleEventProvider, SampleFlightProvider
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


class PlanRequest(BaseModel):
    cities: list[str]
    airports: list[str]
    start_date: date
    end_date: date
    event_weight: float = 0.6
    flight_weight: float = 0.4


class TripResponse(BaseModel):
    plan: str


@app.post("/plan")
def plan_trips_endpoint(request: PlanRequest) -> TripResponse:
    """Plan a semester of weekend trips."""
    cities = [
        City(name, "Europe", airport)
        for name, airport in zip(request.cities, request.airports)
    ]
    weekends = semester_weekends(request.start_date, request.end_date)
    weights = Weights(event=request.event_weight, flight=request.flight_weight)
    
    plan = plan_trips(
        cities,
        weekends,
        weights=weights,
        event_provider=SampleEventProvider(),
        flight_provider=SampleFlightProvider(),
    )
    return TripResponse(plan=plan.show())


@app.get("/health")
def health_check():
    return {"status": "ok"}

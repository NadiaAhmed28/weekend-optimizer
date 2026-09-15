export interface CityIn {
  name: string
  country: string
  airport: string
}

export interface EventOut {
  name: string
  category: string
}

export interface WeekendOut {
  index: number
  label: string
  start: string
  end: string
}

export interface AssignmentOut {
  weekend: WeekendOut
  city: CityIn
  price: number | null
  events: EventOut[]
  score: number
}

export interface PlanResponse {
  assignments: AssignmentOut[]
  unplaced_cities: CityIn[]
  free_weekends: WeekendOut[]
  total_score: number
}

export interface PlanRequest {
  cities: CityIn[]
  start_date: string
  end_date: string
  origin?: CityIn
  event_weight: number
  flight_weight: number
  favorite_artists: string[]
  max_budget?: number
}

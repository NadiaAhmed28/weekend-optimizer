import type { CityIn, PlanRequest, PlanResponse } from './types'

export async function fetchSuggestedCities(): Promise<CityIn[]> {
  const res = await fetch('/api/suggested-cities')
  if (!res.ok) throw new Error(`Failed to load suggested cities (${res.status})`)
  return res.json()
}

export async function fetchPlan(request: PlanRequest): Promise<PlanResponse> {
  const res = await fetch('/api/plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  })
  if (!res.ok) {
    const detail = await res.text()
    throw new Error(`Plan request failed (${res.status}): ${detail}`)
  }
  return res.json()
}

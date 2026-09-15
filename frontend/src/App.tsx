import { useEffect, useState } from 'react'
import { fetchPlan, fetchSuggestedCities } from './api'
import SegmentedControl from './SegmentedControl'
import { iconicEventsInRange } from './sampleEvents'
import { FALLBACK_SUGGESTED_CITIES } from './suggestedCities'
import type { CityIn, PlanResponse } from './types'
import './App.css'

const DEFAULT_ORIGIN: CityIn = { name: 'Madrid', country: 'Spain', airport: 'MAD' }

const COST_CARE_LEVELS = [
  { value: 0.15, label: "Don't really care" },
  { value: 0.4, label: 'A little' },
  { value: 0.65, label: 'Keep it cheap' },
  { value: 0.9, label: "I'm on a tight budget" },
]

const EVENT_CARE_LEVELS = [
  { value: 0.15, label: 'Not really' },
  { value: 0.4, label: 'A nice bonus' },
  { value: 0.65, label: 'I want good events' },
  { value: 0.9, label: 'Chase every show' },
]

function App() {
  const [origin, setOrigin] = useState<CityIn>(DEFAULT_ORIGIN)
  const [cities, setCities] = useState<CityIn[]>([])
  const [suggested, setSuggested] = useState<CityIn[]>(FALLBACK_SUGGESTED_CITIES)
  const [newCity, setNewCity] = useState<CityIn>({ name: '', country: '', airport: '' })

  const [startDate, setStartDate] = useState('2027-01-18')
  const [endDate, setEndDate] = useState('2027-05-15')
  const [costCare, setCostCare] = useState(0.4)
  const [maxBudget, setMaxBudget] = useState('')
  const [eventsCare, setEventsCare] = useState(0.65)
  const [favoriteArtists, setFavoriteArtists] = useState('')

  const [plan, setPlan] = useState<PlanResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchSuggestedCities()
      .then(setSuggested)
      .catch(() => {
        // Backend unreachable — keep the bundled fallback list so there
        // are always candidate cities to pick from.
      })
  }, [])

  function addCity(city: CityIn) {
    if (!city.name || !city.airport) return
    if (cities.some((c) => c.airport === city.airport)) return
    setCities([...cities, city])
  }

  function removeCity(airport: string) {
    setCities(cities.filter((c) => c.airport !== airport))
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setPlan(null)
    try {
      const result = await fetchPlan({
        cities,
        start_date: startDate,
        end_date: endDate,
        origin,
        event_weight: eventsCare,
        flight_weight: costCare,
        favorite_artists: favoriteArtists
          .split(',')
          .map((a) => a.trim())
          .filter(Boolean),
        max_budget: maxBudget ? Number(maxBudget) : undefined,
      })
      setPlan(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err))
    } finally {
      setLoading(false)
    }
  }

  const availableSuggestions = suggested.filter(
    (s) => !cities.some((c) => c.airport === s.airport),
  )
  const iconicSample = iconicEventsInRange(startDate, endDate).slice(0, 5)

  return (
    <div className="page">
      <header>
        <h1>Plan Your Trips Abroad!!!</h1>
        <p className="subtitle">
          Assign one city per weekend to maximize events you'd love, minus flight cost.
        </p>
      </header>

      <form onSubmit={handleSubmit} className="layout">
        <section className="panel">
          <h2>Semester</h2>
          <div className="field-row">
            <label>
              Start date
              <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} required />
            </label>
            <label>
              End date
              <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} required />
            </label>
          </div>
          <div className="field-row">
            <label>
              Origin city
              <input
                value={origin.name}
                onChange={(e) => setOrigin({ ...origin, name: e.target.value })}
              />
            </label>
            <label>
              Origin airport
              <input
                value={origin.airport}
                onChange={(e) => setOrigin({ ...origin, airport: e.target.value.toUpperCase() })}
              />
            </label>
          </div>
          <label className="field-block">
            Favorite artists (comma separated)
            <input
              value={favoriteArtists}
              onChange={(e) => setFavoriteArtists(e.target.value)}
              placeholder="e.g. Rosalía, Bad Bunny"
            />
          </label>

          <div className="field-block">
            <span>How much do you care about cost?</span>
            <SegmentedControl options={COST_CARE_LEVELS} value={costCare} onChange={setCostCare} />
          </div>
          <label className="field-block">
            Max budget per trip, round-trip (optional)
            <input
              type="number"
              min={0}
              inputMode="numeric"
              placeholder="e.g. 150"
              value={maxBudget}
              onChange={(e) => setMaxBudget(e.target.value)}
            />
          </label>

          <div className="field-block">
            <span>How much do you care about catching events?</span>
            <SegmentedControl options={EVENT_CARE_LEVELS} value={eventsCare} onChange={setEventsCare} />
          </div>
          {iconicSample.length > 0 && (
            <div className="iconic-events">
              <p className="iconic-caption">
                Some things you might catch between now and then, for inspiration:
              </p>
              <ul>
                {iconicSample.map((ev) => (
                  <li key={ev.name}>
                    <strong>{ev.name}</strong> — {ev.place}. {ev.blurb}.
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>

        <section className="panel">
          <h2>Candidate cities</h2>
          <div className="field-row">
            <input
              placeholder="City"
              value={newCity.name}
              onChange={(e) => setNewCity({ ...newCity, name: e.target.value })}
            />
            <input
              placeholder="Country"
              value={newCity.country}
              onChange={(e) => setNewCity({ ...newCity, country: e.target.value })}
            />
            <input
              placeholder="Airport (IATA)"
              value={newCity.airport}
              onChange={(e) => setNewCity({ ...newCity, airport: e.target.value.toUpperCase() })}
            />
            <button
              type="button"
              onClick={() => {
                addCity(newCity)
                setNewCity({ name: '', country: '', airport: '' })
              }}
            >
              Add
            </button>
          </div>

          {availableSuggestions.length > 0 && (
            <div className="chip-row">
              {availableSuggestions.map((c) => (
                <button type="button" key={c.airport} className="chip" onClick={() => addCity(c)}>
                  + {c.name}
                </button>
              ))}
            </div>
          )}

          <ul className="city-list">
            {cities.map((c) => (
              <li key={c.airport}>
                {c.name} ({c.airport})
                <button type="button" className="remove" onClick={() => removeCity(c.airport)} aria-label={`Remove ${c.name}`}>
                  ×
                </button>
              </li>
            ))}
            {cities.length === 0 && <li className="empty">No cities added yet.</li>}
          </ul>
        </section>

        <button type="submit" className="primary" disabled={loading || cities.length === 0}>
          {loading ? 'Planning…' : 'Plan my semester'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {plan && (
        <section className="panel results">
          <h2>Plan</h2>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Weekend</th>
                  <th>City</th>
                  <th>Price</th>
                  <th>Event</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {plan.assignments.map((a) => (
                  <tr key={a.weekend.index}>
                    <td>{a.weekend.label}</td>
                    <td>{a.city.name}</td>
                    <td>{a.price !== null ? `€${a.price.toFixed(0)}` : 'n/a'}</td>
                    <td>{a.events[0]?.name ?? '-'}</td>
                    <td>{a.score.toFixed(1)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {plan.unplaced_cities.length > 0 && (
            <p>
              <strong>Not placed:</strong>{' '}
              {plan.unplaced_cities.map((c) => c.name).join(', ')}
            </p>
          )}
          {plan.free_weekends.length > 0 && (
            <p>
              <strong>Free weekends:</strong>{' '}
              {plan.free_weekends.map((w) => w.label).join(', ')}
            </p>
          )}
          <p className="total">Total score: {plan.total_score.toFixed(1)}</p>
        </section>
      )}
    </div>
  )
}

export default App

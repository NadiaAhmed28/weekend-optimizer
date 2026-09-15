import type { CityIn } from './types'

// Mirrors weekend_optimizer.models.SUGGESTED_CITIES. Used as the initial
// (and fallback) list so candidate-city chips always render even if the
// backend is unreachable or /suggested-cities fails.
export const FALLBACK_SUGGESTED_CITIES: CityIn[] = [
  { name: 'Lisbon', country: 'Portugal', airport: 'LIS' },
  { name: 'Porto', country: 'Portugal', airport: 'OPO' },
  { name: 'Barcelona', country: 'Spain', airport: 'BCN' },
  { name: 'Seville', country: 'Spain', airport: 'SVQ' },
  { name: 'Paris', country: 'France', airport: 'CDG' },
  { name: 'Rome', country: 'Italy', airport: 'FCO' },
  { name: 'Berlin', country: 'Germany', airport: 'BER' },
  { name: 'Amsterdam', country: 'Netherlands', airport: 'AMS' },
  { name: 'London', country: 'United Kingdom', airport: 'LHR' },
  { name: 'Marrakech', country: 'Morocco', airport: 'RAK' },
  { name: 'Milan', country: 'Italy', airport: 'MXP' },
  { name: 'Vienna', country: 'Austria', airport: 'VIE' },
]

export interface IconicEvent {
  name: string
  place: string
  months: number[] // 1 = January
  blurb: string
}

// Illustrative only — recurring, well-known European events shown for
// inspiration while answering "how much do you care about events?".
// Not the data the optimizer actually scores against (see providers.py).
export const ICONIC_EVENTS: IconicEvent[] = [
  { name: 'Carnival of Venice', place: 'Venice, Italy', months: [2], blurb: 'Masked balls and canal parades' },
  { name: 'Feria de Abril', place: 'Seville, Spain', months: [4], blurb: 'Flamenco, sherry, and an all-night fairground' },
  { name: "King's Day", place: 'Amsterdam, Netherlands', months: [4], blurb: 'The whole city turns orange' },
  { name: 'Eurovision Song Contest', place: 'varies', months: [5], blurb: "Europe's biggest pop spectacle" },
  { name: 'Cannes Film Festival', place: 'Cannes, France', months: [5], blurb: 'Red carpets and premieres on the Riviera' },
  { name: 'Primavera Sound', place: 'Barcelona, Spain', months: [6], blurb: 'Huge indie/electronic lineup by the beach' },
  { name: 'Glastonbury Festival', place: 'Somerset, UK', months: [6], blurb: 'Legendary festival, if you can get tickets' },
  { name: 'Running of the Bulls', place: 'Pamplona, Spain', months: [7], blurb: 'Bulls, bonfires, a sea of white and red' },
  { name: 'Tomorrowland', place: 'Boom, Belgium', months: [7], blurb: "One of the world's biggest EDM festivals" },
  { name: 'Sziget Festival', place: 'Budapest, Hungary', months: [8], blurb: 'Week-long festival on a Danube island' },
  { name: 'Notting Hill Carnival', place: 'London, UK', months: [8], blurb: 'Caribbean carnival through West London' },
  { name: 'La Tomatina', place: 'Buñol, Spain', months: [8], blurb: "The world's biggest tomato fight" },
  { name: 'Oktoberfest', place: 'Munich, Germany', months: [9, 10], blurb: 'Beer tents, brass bands, lederhosen' },
  { name: 'Rome Film Festival', place: 'Rome, Italy', months: [10], blurb: 'Premieres and screenings across the city' },
  { name: 'Christmas Markets', place: 'across Europe', months: [12], blurb: 'Mulled wine and markets from Vienna to Strasbourg' },
]

// Parses a "YYYY-MM-DD" input value into plain year/month numbers,
// deliberately avoiding `new Date(dateString)` — that parses as UTC
// midnight, which `.getMonth()` then reads back in local time and can
// shift a month early in negative-UTC-offset timezones.
function yearMonth(isoDate: string): [number, number] | null {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(isoDate)
  if (!match) return null
  return [Number(match[1]), Number(match[2])]
}

export function monthsInRange(startDate: string, endDate: string): Set<number> {
  const months = new Set<number>()
  const start = yearMonth(startDate)
  const end = yearMonth(endDate)
  if (!start || !end) return months

  let [year, month] = start
  const [endYear, endMonth] = end
  while (year < endYear || (year === endYear && month <= endMonth)) {
    months.add(month)
    month += 1
    if (month > 12) {
      month = 1
      year += 1
    }
  }
  return months
}

export function iconicEventsInRange(startDate: string, endDate: string): IconicEvent[] {
  const months = monthsInRange(startDate, endDate)
  return ICONIC_EVENTS.filter((e) => e.months.some((m) => months.has(m)))
}

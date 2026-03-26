/**
 * Build a Google Calendar URL from event data.
 * Used when the backend calendar-link endpoint is unavailable.
 */
export function buildGoogleCalendarLink(event) {
  const fmt = (d) => new Date(d).toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z'
  const params = new URLSearchParams({
    action: 'TEMPLATE',
    text: event.title,
    dates: `${fmt(event.start_at)}/${fmt(event.end_at)}`,
    details: (event.description || '').slice(0, 500),
    location: event.address || event.venue_name || '',
  })
  return `https://calendar.google.com/calendar/render?${params.toString()}`
}

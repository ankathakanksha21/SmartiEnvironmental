// Turns the API's "2026-11-05T09:30:00" into "Thu, 5 Nov 2026, 09:30".
export function formatDateTime(value) {
  return new Date(value).toLocaleString('en-GB', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

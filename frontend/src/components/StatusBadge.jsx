// A coloured label for a status. style.css sets a colour for each status.
export default function StatusBadge({ status }) {
  const className = status.toLowerCase().replace(' ', '-')
  return <span className={`badge badge-${className}`}>{status}</span>
}

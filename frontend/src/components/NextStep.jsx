import { Link } from 'react-router'

// A highlighted line that points to what should happen next.
export default function NextStep({ to, children }) {
  return (
    <div className="next-step">
      <span className="next-step-label">Next step</span>
      <Link to={to}>{children}</Link>
    </div>
  )
}

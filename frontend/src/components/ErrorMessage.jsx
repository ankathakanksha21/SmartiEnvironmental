import { Link } from 'react-router'

// Shows a failed request. A missing record gets a way back to the home page.
export default function ErrorMessage({ error }) {
  return (
    <div className="error-box" role="alert">
      <p>{error.message}</p>
      {error.status === 404 && <Link to="/">Back to the home page</Link>}
    </div>
  )
}

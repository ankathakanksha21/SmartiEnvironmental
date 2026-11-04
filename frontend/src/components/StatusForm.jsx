import { useState } from 'react'
import ErrorMessage from './ErrorMessage.jsx'
import StatusBadge from './StatusBadge.jsx'

// Shows the current status and lets the user change it.
export default function StatusForm({ current, options, save }) {
  const [status, setStatus] = useState(current)
  const [problem, setProblem] = useState(null)

  async function submit(event) {
    event.preventDefault()
    setProblem(null)
    try {
      await save(status)
    } catch (error) {
      setProblem(error)
    }
  }

  return (
    <form className="status-form" onSubmit={submit}>
      {problem && <ErrorMessage error={problem} />}
      <div className="status-form-row">
        <StatusBadge status={current} />
        <label>
          Change to{' '}
          <select value={status} onChange={(event) => setStatus(event.target.value)}>
            {options.map((option) => (
              <option key={option}>{option}</option>
            ))}
          </select>
        </label>
        <button type="submit" disabled={status === current}>
          Update status
        </button>
      </div>
    </form>
  )
}

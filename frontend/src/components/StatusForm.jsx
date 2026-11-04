import { useForm } from '../useForm.js'
import ErrorMessage from './ErrorMessage.jsx'
import StatusBadge from './StatusBadge.jsx'

// Shows the current status and lets the user change it.
export default function StatusForm({ current, options, save }) {
  const form = useForm({ status: current }, (values) => save(values.status))

  return (
    <form onSubmit={form.submit}>
      {form.problem && <ErrorMessage error={form.problem} />}
      <div className="status-form-row">
        <StatusBadge status={current} />
        <label>
          Change to{' '}
          <select name="status" value={form.values.status} onChange={form.change}>
            {options.map((option) => (
              <option key={option}>{option}</option>
            ))}
          </select>
        </label>
        <button type="submit" disabled={form.saving || form.values.status === current}>
          Update status
        </button>
      </div>
    </form>
  )
}

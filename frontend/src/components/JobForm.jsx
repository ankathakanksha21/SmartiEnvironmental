import { Link } from 'react-router'
import { useApi } from '../api.js'
import { useForm } from '../useForm.js'
import ErrorMessage from './ErrorMessage.jsx'
import Field from './Field.jsx'

// Used to book and to edit a job.
export default function JobForm({ initialValues, save, saveLabel, cancelTo }) {
  const form = useForm(initialValues, save)
  const customers = useApi('/customers')
  const staff = useApi('/staff')

  if (customers.loading || staff.loading) return <p>Loading...</p>
  if (customers.error) return <ErrorMessage error={customers.error} />
  if (staff.error) return <ErrorMessage error={staff.error} />

  // Inactive staff can't take new jobs, but a job they already have keeps them as an option.
  const staffOptions = staff.data.filter(
    (member) => member.is_active || member.id === initialValues.staff_id,
  )

  return (
    <form className="form" onSubmit={form.submit} noValidate>
      {form.problem && <ErrorMessage error={form.problem} />}

      <Field label="Customer" error={form.errors.customer_id}>
        <select name="customer_id" value={form.values.customer_id} onChange={form.change}>
          <option value="">Choose a customer</option>
          {customers.data.map((customer) => (
            <option key={customer.id} value={customer.id}>
              {customer.name} ({customer.phone})
            </option>
          ))}
        </select>
      </Field>
      {customers.data.length === 0 && (
        <p className="form-hint">
          No customers yet. <Link to="/customers/new">Add a customer first.</Link>
        </p>
      )}

      <Field label="Staff member" error={form.errors.staff_id}>
        <select name="staff_id" value={form.values.staff_id} onChange={form.change}>
          <option value="">Choose a staff member</option>
          {staffOptions.map((member) => (
            <option key={member.id} value={member.id}>
              {member.name} ({member.is_active ? member.role : 'inactive'})
            </option>
          ))}
        </select>
      </Field>
      {staffOptions.length === 0 && (
        <p className="form-hint">
          No active staff yet. <Link to="/staff/new">Add a staff member first.</Link>
        </p>
      )}

      <Field label="Date and time" error={form.errors.scheduled_at}>
        <input
          name="scheduled_at"
          type="datetime-local"
          value={form.values.scheduled_at}
          onChange={form.change}
        />
      </Field>

      <Field label="Description" error={form.errors.description}>
        <textarea
          name="description"
          rows="3"
          value={form.values.description}
          onChange={form.change}
        />
      </Field>

      <div className="form-actions">
        <button type="submit" disabled={form.saving}>
          {saveLabel}
        </button>
        <Link to={cancelTo}>Cancel</Link>
      </div>
    </form>
  )
}

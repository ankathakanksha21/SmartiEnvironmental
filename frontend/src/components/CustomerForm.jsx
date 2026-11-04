import { Link } from 'react-router'
import { ONBOARDING_STATUSES } from '../constants.js'
import { useForm } from '../useForm.js'
import ErrorMessage from './ErrorMessage.jsx'
import Field from './Field.jsx'

// Used to add and to edit a customer. Status only appears when adding,
// because an existing customer's page has its own status form.
export default function CustomerForm({ initialValues, save, saveLabel, cancelTo }) {
  const form = useForm(initialValues, save)

  // noValidate leaves the checks to the backend, so there's one set of rules and messages.
  return (
    <form className="form" onSubmit={form.submit} noValidate>
      {form.problem && <ErrorMessage error={form.problem} />}

      <Field label="Name" error={form.errors.name}>
        <input name="name" value={form.values.name} onChange={form.change} />
      </Field>

      <Field label="Phone" error={form.errors.phone}>
        <input name="phone" type="tel" value={form.values.phone} onChange={form.change} />
      </Field>

      <Field label="Email (optional)" error={form.errors.email}>
        <input name="email" type="email" value={form.values.email} onChange={form.change} />
      </Field>

      <Field label="Address" error={form.errors.address}>
        <textarea name="address" rows="3" value={form.values.address} onChange={form.change} />
      </Field>

      {'onboarding_status' in form.values && (
        <Field label="Onboarding status" error={form.errors.onboarding_status}>
          <select
            name="onboarding_status"
            value={form.values.onboarding_status}
            onChange={form.change}
          >
            {ONBOARDING_STATUSES.map((status) => (
              <option key={status}>{status}</option>
            ))}
          </select>
        </Field>
      )}

      <div className="form-actions">
        <button type="submit" disabled={form.saving}>
          {saveLabel}
        </button>
        <Link to={cancelTo}>Cancel</Link>
      </div>
    </form>
  )
}

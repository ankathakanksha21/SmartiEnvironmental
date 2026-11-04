import { Link } from 'react-router'
import { STAFF_ROLES } from '../constants.js'
import { useForm } from '../useForm.js'
import ErrorMessage from './ErrorMessage.jsx'
import Field from './Field.jsx'

// Used to add and to edit a staff member. The active checkbox only appears
// when editing, because everyone starts as active.
export default function StaffForm({ initialValues, save, saveLabel, cancelTo }) {
  const form = useForm(initialValues, save)

  return (
    <form className="form" onSubmit={form.submit} noValidate>
      {form.problem && <ErrorMessage error={form.problem} />}

      <Field label="Name" error={form.errors.name}>
        <input name="name" value={form.values.name} onChange={form.change} />
      </Field>

      <Field label="Role" error={form.errors.role}>
        <select name="role" value={form.values.role} onChange={form.change}>
          {STAFF_ROLES.map((role) => (
            <option key={role}>{role}</option>
          ))}
        </select>
      </Field>

      <Field label="Phone" error={form.errors.phone}>
        <input name="phone" type="tel" value={form.values.phone} onChange={form.change} />
      </Field>

      {'is_active' in form.values && (
        <label className="checkbox">
          <input
            name="is_active"
            type="checkbox"
            checked={form.values.is_active}
            onChange={form.change}
          />
          Active (can be assigned new jobs)
        </label>
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

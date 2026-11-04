import { Link } from 'react-router'
import { useApi } from '../api.js'
import { formatDateTime } from '../formatDateTime.js'
import ErrorMessage from './ErrorMessage.jsx'
import StatusBadge from './StatusBadge.jsx'

// Loads and lists jobs. Each page that uses it passes its own path, and can cap the number of rows.
export default function JobsTable({ path, emptyMessage, limit }) {
  const { data: jobs, error, loading } = useApi(path)

  if (loading) return <p>Loading...</p>
  if (error) return <ErrorMessage error={error} />
  if (jobs.length === 0) return <p>{emptyMessage}</p>

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Date and time</th>
            <th>Customer</th>
            <th>Staff member</th>
            <th>Description</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {jobs.slice(0, limit).map((job) => (
            <tr key={job.id}>
              <td className="no-wrap">
                <Link to={`/jobs/${job.id}`}>{formatDateTime(job.scheduled_at)}</Link>
              </td>
              <td>
                <Link to={`/customers/${job.customer.id}`}>{job.customer.name}</Link>
              </td>
              <td>
                <Link to={`/staff/${job.staff.id}`}>{job.staff.name}</Link>{' '}
                {!job.staff.is_active && <StatusBadge status="Inactive" />}
                <div className="muted">{job.staff.role}</div>
              </td>
              <td>{job.description}</td>
              <td>
                <StatusBadge status={job.status} />
                {job.is_overdue && <StatusBadge status="Overdue" />}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

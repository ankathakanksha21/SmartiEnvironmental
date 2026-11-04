import { Link } from 'react-router'
import { useApi } from '../api.js'
import { formatDateTime } from '../formatDateTime.js'
import ErrorMessage from './ErrorMessage.jsx'
import StatusBadge from './StatusBadge.jsx'

// Loads and lists jobs. The jobs page, customer pages and staff pages each pass their own path.
export default function JobsTable({ path, emptyMessage }) {
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
          {jobs.map((job) => (
            <tr key={job.id}>
              <td>
                <Link to={`/jobs/${job.id}`}>{formatDateTime(job.scheduled_at)}</Link>
              </td>
              <td>{job.customer.name}</td>
              <td>
                {job.staff.name} {!job.staff.is_active && <StatusBadge status="Inactive" />}
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

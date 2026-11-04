import { Link, useParams } from 'react-router'
import { useApi } from '../api.js'
import ErrorMessage from '../components/ErrorMessage.jsx'
import JobsTable from '../components/JobsTable.jsx'
import StatusBadge from '../components/StatusBadge.jsx'

export default function StaffDetail() {
  const { id } = useParams()
  const { data: member, error, loading } = useApi(`/staff/${id}`)

  if (loading) return <p>Loading...</p>
  if (error) return <ErrorMessage error={error} />

  return (
    <>
      <div className="page-header">
        <h1>{member.name}</h1>
        <Link className="button button-secondary" to={`/staff/${id}/edit`}>
          Edit details
        </Link>
      </div>

      <dl className="details">
        <dt>Role</dt>
        <dd>{member.role}</dd>
        <dt>Phone</dt>
        <dd>{member.phone}</dd>
        <dt>Status</dt>
        <dd>
          <StatusBadge status={member.is_active ? 'Active' : 'Inactive'} />
        </dd>
      </dl>

      <h2>Jobs</h2>
      <JobsTable path={`/jobs?staff_id=${id}`} emptyMessage="No jobs yet." />
    </>
  )
}

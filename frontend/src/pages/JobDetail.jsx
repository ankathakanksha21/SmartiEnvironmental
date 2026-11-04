import { Link, useNavigate, useParams } from 'react-router'
import { request, useApi } from '../api.js'
import ErrorMessage from '../components/ErrorMessage.jsx'
import NextStep from '../components/NextStep.jsx'
import StatusBadge from '../components/StatusBadge.jsx'
import StatusForm from '../components/StatusForm.jsx'
import { JOB_STATUSES } from '../constants.js'
import { formatDateTime } from '../formatDateTime.js'

export default function JobDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: job, error, loading, reload } = useApi(`/jobs/${id}`)

  if (loading) return <p>Loading...</p>
  if (error) return <ErrorMessage error={error} />

  async function saveStatus(status) {
    await request(`/jobs/${id}/status`, { method: 'PATCH', body: { status } })
    reload()
    navigate('.', { replace: true, state: { message: 'Job status updated.' } })
  }

  return (
    <>
      <div className="page-header">
        <h1>Job for {job.customer.name}</h1>
        <Link className="button button-secondary" to={`/jobs/${id}/edit`}>
          Edit job
        </Link>
      </div>

      {job.status === 'Completed' && (
        <NextStep to={`/jobs/new?customer_id=${job.customer.id}&description=Maintenance visit`}>
          Book a follow-up maintenance visit
        </NextStep>
      )}

      <dl className="details">
        <dt>Date and time</dt>
        <dd>
          {formatDateTime(job.scheduled_at)} {job.is_overdue && <StatusBadge status="Overdue" />}
        </dd>
        <dt>Description</dt>
        <dd className="keep-line-breaks">{job.description}</dd>
        <dt>Customer</dt>
        <dd>
          <Link to={`/customers/${job.customer.id}`}>{job.customer.name}</Link>{' '}
          <StatusBadge status={job.customer.onboarding_status} />
          <div className="muted">{job.customer.phone}</div>
          <div className="muted keep-line-breaks">{job.customer.address}</div>
        </dd>
        <dt>Staff member</dt>
        <dd>
          <Link to={`/staff/${job.staff.id}`}>{job.staff.name}</Link>{' '}
          {!job.staff.is_active && <StatusBadge status="Inactive" />}
          <div className="muted">{job.staff.role}</div>
        </dd>
      </dl>

      <h2>Job status</h2>
      <StatusForm current={job.status} options={JOB_STATUSES} save={saveStatus} />
    </>
  )
}

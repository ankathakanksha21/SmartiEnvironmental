import { Link, useNavigate, useParams } from 'react-router'
import { request, useApi } from '../api.js'
import ErrorMessage from '../components/ErrorMessage.jsx'
import JobsTable from '../components/JobsTable.jsx'
import NextStep from '../components/NextStep.jsx'
import StatusForm from '../components/StatusForm.jsx'
import { ONBOARDING_STATUSES } from '../constants.js'
import { formatDateTime } from '../formatDateTime.js'

// Works out what should happen next for a customer from their jobs.
function CustomerNextStep({ customerId }) {
  const { data: jobs, error, loading } = useApi(`/jobs?customer_id=${customerId}`)

  // The jobs table on this page already shows any problem loading these jobs.
  if (loading || error) return null

  const bookingPage = `/jobs/new?customer_id=${customerId}`
  // Jobs arrive earliest first, so this is the one to deal with next.
  const openJob = jobs.find((job) => job.status !== 'Completed')

  if (openJob) {
    const visit = openJob.is_overdue ? 'overdue visit' : 'visit'
    return (
      <NextStep to={`/jobs/${openJob.id}`}>
        Complete the {visit} on {formatDateTime(openJob.scheduled_at)}
      </NextStep>
    )
  }
  if (jobs.length > 0) {
    return (
      <NextStep to={`${bookingPage}&description=Maintenance visit`}>
        Book a maintenance visit
      </NextStep>
    )
  }
  return <NextStep to={bookingPage}>Book the first visit</NextStep>
}

export default function CustomerDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: customer, error, loading, reload } = useApi(`/customers/${id}`)

  if (loading) return <p>Loading...</p>
  if (error) return <ErrorMessage error={error} />

  async function saveStatus(status) {
    await request(`/customers/${id}/status`, {
      method: 'PATCH',
      body: { onboarding_status: status },
    })
    reload()
    navigate('.', { replace: true, state: { message: 'Onboarding status updated.' } })
  }

  return (
    <>
      <div className="page-header">
        <h1>{customer.name}</h1>
        <Link className="button button-secondary" to={`/customers/${id}/edit`}>
          Edit details
        </Link>
      </div>

      <CustomerNextStep customerId={id} />

      <dl className="details">
        <dt>Phone</dt>
        <dd>{customer.phone}</dd>
        <dt>Email</dt>
        <dd>{customer.email || 'None'}</dd>
        <dt>Address</dt>
        <dd className="keep-line-breaks">{customer.address}</dd>
      </dl>

      <h2>Onboarding status</h2>
      <StatusForm
        current={customer.onboarding_status}
        options={ONBOARDING_STATUSES}
        save={saveStatus}
      />

      <div className="section-header">
        <h2>Jobs</h2>
        <Link className="button button-secondary" to={`/jobs/new?customer_id=${id}`}>
          Book a job
        </Link>
      </div>
      <JobsTable path={`/jobs?customer_id=${id}`} emptyMessage="No jobs yet." />
    </>
  )
}

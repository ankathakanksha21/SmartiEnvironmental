import { Link, useOutletContext, useParams } from 'react-router'
import { request, useApi } from '../api.js'
import CustomerNextStep from '../components/CustomerNextStep.jsx'
import ErrorMessage from '../components/ErrorMessage.jsx'
import JobsTable from '../components/JobsTable.jsx'
import StatusForm from '../components/StatusForm.jsx'
import { ONBOARDING_STATUSES } from '../constants.js'

export default function CustomerDetail() {
  const { id } = useParams()
  const showMessage = useOutletContext()
  const { data: customer, error, loading, reload } = useApi(`/customers/${id}`)

  if (loading) return <p>Loading...</p>
  if (error) return <ErrorMessage error={error} />

  async function saveStatus(status) {
    await request(`/customers/${id}/status`, {
      method: 'PATCH',
      body: { onboarding_status: status },
    })
    reload()
    showMessage('Onboarding status updated.')
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

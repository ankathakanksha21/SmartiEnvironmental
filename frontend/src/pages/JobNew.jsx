import { useNavigate, useSearchParams } from 'react-router'
import { request } from '../api.js'
import JobForm from '../components/JobForm.jsx'

export default function JobNew() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  // A customer's page links here with their id, so they start selected.
  const customerId = searchParams.get('customer_id')

  async function save(values) {
    const job = await request('/jobs', { method: 'POST', body: values })
    navigate(`/jobs/${job.id}`)
  }

  return (
    <>
      <h1>Book a job</h1>
      <JobForm
        initialValues={{
          customer_id: customerId ?? '',
          staff_id: '',
          scheduled_at: '',
          description: '',
        }}
        save={save}
        saveLabel="Book job"
        cancelTo={customerId ? `/customers/${customerId}` : '/jobs'}
      />
    </>
  )
}

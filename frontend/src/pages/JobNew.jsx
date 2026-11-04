import { useNavigate, useOutletContext, useSearchParams } from 'react-router'
import { request } from '../api.js'
import JobForm from '../components/JobForm.jsx'

export default function JobNew() {
  const navigate = useNavigate()
  const showMessage = useOutletContext()
  const [searchParams] = useSearchParams()
  // Customer and job pages link here with the customer's id, so that customer starts selected.
  const customerId = searchParams.get('customer_id')

  async function save(values) {
    const job = await request('/jobs', { method: 'POST', body: values })
    showMessage('Job booked.')
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
          // A follow-up link can suggest a description, such as "Maintenance visit".
          description: searchParams.get('description') ?? '',
        }}
        save={save}
        saveLabel="Book job"
        cancelTo={customerId ? `/customers/${customerId}` : '/jobs'}
      />
    </>
  )
}

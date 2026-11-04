import { useNavigate, useParams } from 'react-router'
import { request, useApi } from '../api.js'
import ErrorMessage from '../components/ErrorMessage.jsx'
import JobForm from '../components/JobForm.jsx'

export default function JobEdit() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: job, error, loading } = useApi(`/jobs/${id}`)

  if (loading) return <p>Loading...</p>
  if (error) return <ErrorMessage error={error} />

  async function save(values) {
    await request(`/jobs/${id}`, { method: 'PUT', body: values })
    navigate(`/jobs/${id}`, { state: { message: 'Job saved.' } })
  }

  return (
    <>
      <h1>Edit job for {job.customer.name}</h1>
      <JobForm
        initialValues={{
          customer_id: job.customer.id,
          staff_id: job.staff.id,
          // A datetime-local input takes "2026-11-05T09:30", with no seconds.
          scheduled_at: job.scheduled_at.slice(0, 16),
          description: job.description,
        }}
        save={save}
        saveLabel="Save changes"
        cancelTo={`/jobs/${id}`}
      />
    </>
  )
}

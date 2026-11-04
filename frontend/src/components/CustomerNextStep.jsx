import { Link } from 'react-router'
import { useApi } from '../api.js'
import { formatDateTime } from '../formatDateTime.js'

function NextStepLine({ to, children }) {
  return (
    <div className="next-step">
      <span className="next-step-label">Next step</span>
      <Link to={to}>{children}</Link>
    </div>
  )
}

// A highlighted line that works out what should happen next for a customer from their jobs.
export default function CustomerNextStep({ customerId }) {
  const { data: jobs, error, loading } = useApi(`/jobs?customer_id=${customerId}`)

  // This line only points the way, so the page carries on without it if the jobs can't load.
  if (loading || error) return null

  const bookingPage = `/jobs/new?customer_id=${customerId}`
  // Jobs arrive earliest first, so this is the one to deal with next.
  const openJob = jobs.find((job) => job.status !== 'Completed')

  if (openJob) {
    return (
      <NextStepLine to={`/jobs/${openJob.id}`}>
        Complete the {openJob.is_overdue ? 'overdue job from' : 'job on'}{' '}
        {formatDateTime(openJob.scheduled_at)}
      </NextStepLine>
    )
  }
  if (jobs.length > 0) {
    return (
      <NextStepLine to={`${bookingPage}&description=Maintenance%20visit`}>
        Book a follow-up maintenance visit
      </NextStepLine>
    )
  }
  return <NextStepLine to={bookingPage}>Book the first job</NextStepLine>
}

import { Link, useSearchParams } from 'react-router'
import JobsTable from '../components/JobsTable.jsx'

// A job is a booked visit, so upcoming appointments are the future jobs not yet completed.
export default function JobList() {
  const [searchParams] = useSearchParams()
  const showAll = searchParams.get('view') === 'all'

  return (
    <>
      <div className="page-header">
        <h1>{showAll ? 'All jobs' : 'Upcoming appointments'}</h1>
        <Link className="button" to="/jobs/new">
          Book a job
        </Link>
      </div>

      <div className="view-tabs">
        <Link className={showAll ? '' : 'active'} to="/jobs">
          Upcoming
        </Link>
        <Link className={showAll ? 'active' : ''} to="/jobs?view=all">
          All jobs
        </Link>
      </div>

      <JobsTable
        path={showAll ? '/jobs' : '/jobs?upcoming=true'}
        emptyMessage={showAll ? 'No jobs yet.' : 'No upcoming appointments.'}
      />
    </>
  )
}

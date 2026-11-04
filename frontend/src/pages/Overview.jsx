import { Link } from 'react-router'
import { useApi } from '../api.js'
import ErrorMessage from '../components/ErrorMessage.jsx'
import JobsTable from '../components/JobsTable.jsx'
import StatusBadge from '../components/StatusBadge.jsx'

// The home page. It shows what needs attention and how busy each person is.
export default function Overview() {
  const customers = useApi('/customers')
  const jobs = useApi('/jobs')
  const upcoming = useApi('/jobs?upcoming=true')
  const staff = useApi('/staff')

  const requests = [customers, jobs, upcoming, staff]
  if (requests.some((result) => result.loading)) return <p>Loading...</p>
  const failed = requests.find((result) => result.error)
  if (failed) return <ErrorMessage error={failed.error} />

  const counts = [
    {
      label: 'New enquiries',
      value: customers.data.filter((customer) => customer.onboarding_status === 'New Enquiry')
        .length,
      to: '/customers',
    },
    { label: 'Upcoming appointments', value: upcoming.data.length, to: '/jobs' },
    {
      label: 'Jobs in progress',
      value: jobs.data.filter((job) => job.status === 'In Progress').length,
      to: '/jobs?view=all',
    },
    {
      label: 'Overdue jobs',
      value: jobs.data.filter((job) => job.is_overdue).length,
      to: '/jobs?view=all',
    },
  ]

  const openJobsFor = (member) =>
    jobs.data.filter((job) => job.staff.id === member.id && job.status !== 'Completed').length

  // Someone who has left still shows here if they have open jobs to hand over.
  const workload = staff.data.filter((member) => member.is_active || openJobsFor(member) > 0)

  return (
    <>
      <h1>Overview</h1>

      <div className="stat-grid">
        {counts.map((count) => (
          <Link key={count.label} className="stat-card" to={count.to}>
            <span className="stat-value">{count.value}</span>
            <span className="stat-label">{count.label}</span>
          </Link>
        ))}
      </div>

      <h2>Next appointments</h2>
      <JobsTable path="/jobs?upcoming=true" limit={5} emptyMessage="No upcoming appointments." />

      <h2>Staff workload</h2>
      {workload.length === 0 ? (
        <p>No active staff.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Open jobs</th>
              </tr>
            </thead>
            <tbody>
              {workload.map((member) => (
                <tr key={member.id}>
                  <td>
                    <Link to={`/staff/${member.id}`}>{member.name}</Link>{' '}
                    {!member.is_active && <StatusBadge status="Inactive" />}
                  </td>
                  <td>{member.role}</td>
                  <td>{openJobsFor(member)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  )
}

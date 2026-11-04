import { Link } from 'react-router'
import { useApi } from '../api.js'
import ErrorMessage from '../components/ErrorMessage.jsx'
import StatusBadge from '../components/StatusBadge.jsx'

export default function StaffList() {
  const { data: staff, error, loading } = useApi('/staff')

  if (loading) return <p>Loading...</p>
  if (error) return <ErrorMessage error={error} />

  return (
    <>
      <div className="page-header">
        <h1>Staff</h1>
        <Link className="button" to="/staff/new">
          Add staff member
        </Link>
      </div>

      {staff.length === 0 ? (
        <p>No staff yet.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Phone</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {staff.map((member) => (
                <tr key={member.id}>
                  <td>
                    <Link to={`/staff/${member.id}`}>{member.name}</Link>
                  </td>
                  <td>{member.role}</td>
                  <td>{member.phone}</td>
                  <td>
                    <StatusBadge status={member.is_active ? 'Active' : 'Inactive'} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  )
}

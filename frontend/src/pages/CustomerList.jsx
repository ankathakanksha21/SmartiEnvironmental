import { Link } from 'react-router'
import { useApi } from '../api.js'
import ErrorMessage from '../components/ErrorMessage.jsx'
import StatusBadge from '../components/StatusBadge.jsx'

export default function CustomerList() {
  const { data: customers, error, loading } = useApi('/customers')

  if (loading) return <p>Loading...</p>
  if (error) return <ErrorMessage error={error} />

  return (
    <>
      <div className="page-header">
        <h1>Customers</h1>
        <Link className="button" to="/customers/new">
          Add customer
        </Link>
      </div>

      {customers.length === 0 ? (
        <p>No customers yet.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Phone</th>
                <th>Email</th>
                <th>Onboarding status</th>
              </tr>
            </thead>
            <tbody>
              {customers.map((customer) => (
                <tr key={customer.id}>
                  <td>
                    <Link to={`/customers/${customer.id}`}>{customer.name}</Link>
                  </td>
                  <td>{customer.phone}</td>
                  <td>{customer.email}</td>
                  <td>
                    <StatusBadge status={customer.onboarding_status} />
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

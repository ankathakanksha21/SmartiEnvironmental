import { useNavigate, useParams } from 'react-router'
import { request, useApi } from '../api.js'
import CustomerForm from '../components/CustomerForm.jsx'
import ErrorMessage from '../components/ErrorMessage.jsx'

export default function CustomerEdit() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: customer, error, loading } = useApi(`/customers/${id}`)

  if (loading) return <p>Loading...</p>
  if (error) return <ErrorMessage error={error} />

  async function save(values) {
    await request(`/customers/${id}`, { method: 'PUT', body: values })
    navigate(`/customers/${id}`, { state: { message: 'Customer details saved.' } })
  }

  const { name, phone, email, address } = customer

  return (
    <>
      <h1>Edit {customer.name}</h1>
      <CustomerForm
        initialValues={{ name, phone, email, address }}
        save={save}
        saveLabel="Save changes"
        cancelTo={`/customers/${id}`}
      />
    </>
  )
}

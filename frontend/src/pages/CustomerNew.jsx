import { useNavigate } from 'react-router'
import { request } from '../api.js'
import CustomerForm from '../components/CustomerForm.jsx'

const EMPTY_CUSTOMER = {
  name: '',
  phone: '',
  email: '',
  address: '',
  onboarding_status: 'New Enquiry',
}

export default function CustomerNew() {
  const navigate = useNavigate()

  async function save(values) {
    const customer = await request('/customers', { method: 'POST', body: values })
    navigate(`/customers/${customer.id}`, { state: { message: 'Customer added.' } })
  }

  return (
    <>
      <h1>Add customer</h1>
      <CustomerForm
        initialValues={EMPTY_CUSTOMER}
        save={save}
        saveLabel="Add customer"
        cancelTo="/customers"
      />
    </>
  )
}

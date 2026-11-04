import { useNavigate, useOutletContext } from 'react-router'
import { request } from '../api.js'
import StaffForm from '../components/StaffForm.jsx'
import { STAFF_ROLES } from '../constants.js'

const EMPTY_STAFF = { name: '', role: STAFF_ROLES[0], phone: '' }

export default function StaffNew() {
  const navigate = useNavigate()
  const showMessage = useOutletContext()

  async function save(values) {
    const member = await request('/staff', { method: 'POST', body: values })
    showMessage('Staff member added.')
    navigate(`/staff/${member.id}`)
  }

  return (
    <>
      <h1>Add staff member</h1>
      <StaffForm
        initialValues={EMPTY_STAFF}
        save={save}
        saveLabel="Add staff member"
        cancelTo="/staff"
      />
    </>
  )
}

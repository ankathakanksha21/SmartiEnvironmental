import { useNavigate, useParams } from 'react-router'
import { request, useApi } from '../api.js'
import ErrorMessage from '../components/ErrorMessage.jsx'
import StaffForm from '../components/StaffForm.jsx'

export default function StaffEdit() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: member, error, loading } = useApi(`/staff/${id}`)

  if (loading) return <p>Loading...</p>
  if (error) return <ErrorMessage error={error} />

  async function save(values) {
    await request(`/staff/${id}`, { method: 'PUT', body: values })
    navigate(`/staff/${id}`)
  }

  const { name, role, phone, is_active } = member

  return (
    <>
      <h1>Edit {member.name}</h1>
      <StaffForm
        initialValues={{ name, role, phone, is_active }}
        save={save}
        saveLabel="Save changes"
        cancelTo={`/staff/${id}`}
      />
    </>
  )
}

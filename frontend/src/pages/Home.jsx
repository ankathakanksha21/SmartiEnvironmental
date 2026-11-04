import { useApi } from '../api.js'
import ErrorMessage from '../components/ErrorMessage.jsx'

export default function Home() {
  const { data, error, loading } = useApi('/health')

  if (loading) return <p>Loading...</p>
  if (error) return <ErrorMessage error={error} />

  return (
    <>
      <h1>Smarti CRM</h1>
      <p>Backend status: {data.status}</p>
    </>
  )
}

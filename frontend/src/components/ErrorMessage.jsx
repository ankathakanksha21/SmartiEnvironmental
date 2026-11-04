// Shows a failed request.
export default function ErrorMessage({ error }) {
  return (
    <div className="error-box" role="alert">
      <p>{error.message}</p>
    </div>
  )
}

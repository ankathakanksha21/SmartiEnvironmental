// Every call to the backend goes through this file.

import { useEffect, useState } from 'react'

export class ApiError extends Error {
  constructor(status, message, fieldErrors = {}) {
    super(message)
    this.status = status
    this.fieldErrors = fieldErrors
  }
}

const SERVER_PROBLEM = 'Something went wrong. Check the backend is running, then try again.'
const INVALID_INPUT = 'Please fix the errors and try again.'

export async function request(path, { method = 'GET', body } = {}) {
  let response
  try {
    response = await fetch(`/api${path}`, {
      method,
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    })
  } catch {
    throw new ApiError(0, SERVER_PROBLEM)
  }

  // Every answer from our API is JSON. Anything else, such as a proxy error, counts as a failure.
  const data = await response.json().catch(() => null)
  if (!response.ok || data === null) {
    const message = data?.detail ?? (data?.errors ? INVALID_INPUT : SERVER_PROBLEM)
    throw new ApiError(response.status, message, data?.errors)
  }
  return data
}

// Loads data for a page. Call reload() to fetch it again after a change.
export function useApi(path) {
  const [result, setResult] = useState({ data: null, error: null, loading: true })
  const [reloads, setReloads] = useState(0)

  useEffect(() => {
    // If the page closes before this answer arrives, ignore the answer.
    let ignore = false
    request(path).then(
      (data) => !ignore && setResult({ data, error: null, loading: false }),
      (error) => !ignore && setResult({ data: null, error, loading: false }),
    )
    return () => {
      ignore = true
    }
  }, [path, reloads])

  return { ...result, reload: () => setReloads((count) => count + 1) }
}

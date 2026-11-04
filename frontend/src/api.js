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
  const [result, setResult] = useState({ path: null, data: null, error: null })
  const [reloads, setReloads] = useState(0)

  useEffect(() => {
    // If the page closes before this answer arrives, ignore the answer.
    let ignore = false
    request(path).then(
      (data) => !ignore && setResult({ path, data, error: null }),
      (error) => !ignore && setResult({ path, data: null, error }),
    )
    return () => {
      ignore = true
    }
  }, [path, reloads])

  // The answer may belong to another record if the URL's id just changed. Reporting
  // "loading" makes the page remove its form, so the form can't save old values
  // over the new record.
  const loading = result.path !== path
  return {
    data: loading ? null : result.data,
    error: loading ? null : result.error,
    loading,
    reload: () => setReloads((count) => count + 1),
  }
}

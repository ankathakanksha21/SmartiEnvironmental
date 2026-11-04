// Every call to the backend goes through this file.

import { useCallback, useEffect, useState } from 'react'

export class ApiError extends Error {
  constructor(status, message, fieldErrors = {}) {
    super(message)
    this.status = status
    this.fieldErrors = fieldErrors
  }
}

const SERVER_PROBLEM = 'Something went wrong. Check the backend is running, then try again.'

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

  // A proxy error has no JSON body, so a failed parse counts as no data.
  const data = await response.json().catch(() => null)
  if (!response.ok) {
    throw new ApiError(response.status, data?.detail ?? SERVER_PROBLEM, data?.errors)
  }
  return data
}

// Loads data for a page. Call reload() to fetch it again after a change.
export function useApi(path) {
  const [result, setResult] = useState({ path: null, data: null, error: null })
  const [reloads, setReloads] = useState(0)

  useEffect(() => {
    // If the page moves on before this answer arrives, ignore the answer.
    let ignore = false
    request(path).then(
      (data) => !ignore && setResult({ path, data, error: null }),
      (error) => !ignore && setResult({ path, data: null, error }),
    )
    return () => {
      ignore = true
    }
  }, [path, reloads])

  const reload = useCallback(() => setReloads((count) => count + 1), [])

  // Until the answer for this path arrives, the page is still loading.
  const current = result.path === path
  return {
    data: current ? result.data : null,
    error: current ? result.error : null,
    loading: !current,
    reload,
  }
}

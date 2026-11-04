// The state every form needs: its values, its errors, and whether it's saving.

import { useState } from 'react'

export function useForm(initialValues, save) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  const [problem, setProblem] = useState(null)
  const [saving, setSaving] = useState(false)

  function change(event) {
    const { name, type, checked, value } = event.target
    setValues({ ...values, [name]: type === 'checkbox' ? checked : value })
  }

  async function submit(event) {
    event.preventDefault()
    setSaving(true)
    setErrors({})
    setProblem(null)
    try {
      await save(values)
    } catch (error) {
      setErrors(error.fieldErrors)
      setProblem(error)
    }
    setSaving(false)
  }

  return { values, errors, problem, saving, change, submit }
}

import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import Alert from '../components/ui/Alert'

export default function RegisterPage() {
  const { registerMutation } = useAuth()
  const [form, setForm] = useState({
    first_name: '', last_name: '', email: '', password: '', role: 'attendee',
  })
  const [errors, setErrors] = useState({})

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }))

  const validate = () => {
    const errs = {}
    if (!form.first_name) errs.first_name = 'First name is required'
    if (!form.last_name) errs.last_name = 'Last name is required'
    if (!form.email) errs.email = 'Email is required'
    if (form.password.length < 8) errs.password = 'Password must be at least 8 characters'
    setErrors(errs)
    return Object.keys(errs).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validate()) return
    try {
      await registerMutation.mutateAsync(form)
    } catch (err) {
      const detail = err.response?.data?.detail
      if (typeof detail === 'string') setErrors({ form: detail })
      else setErrors({ form: 'Registration failed. Please try again.' })
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-gray-50">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-gray-900">Create your account</h1>
            <p className="text-gray-500 text-sm mt-1">Join EventHub — it's free!</p>
          </div>

          {errors.form && <Alert type="error" className="mb-4">{errors.form}</Alert>}

          <form onSubmit={handleSubmit} noValidate className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Input id="first_name" label="First name" value={form.first_name} onChange={set('first_name')} error={errors.first_name} autoComplete="given-name" />
              <Input id="last_name" label="Last name" value={form.last_name} onChange={set('last_name')} error={errors.last_name} autoComplete="family-name" />
            </div>
            <Input id="email" label="Email address" type="email" value={form.email} onChange={set('email')} error={errors.email} autoComplete="email" />
            <Input id="password" label="Password" type="password" value={form.password} onChange={set('password')} error={errors.password} autoComplete="new-password" />

            <div>
              <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-1">I want to…</label>
              <select
                id="role"
                value={form.role}
                onChange={set('role')}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
              >
                <option value="attendee">Attend events</option>
                <option value="organizer">Organize events</option>
              </select>
            </div>

            <Button type="submit" loading={registerMutation.isPending} className="w-full" size="lg">
              Create Account
            </Button>
          </form>

          <p className="text-center text-sm text-gray-500 mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-blue-600 font-medium hover:underline focus:ring-2 focus:ring-blue-500 rounded">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
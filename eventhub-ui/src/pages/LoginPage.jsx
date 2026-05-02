import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import Alert from '../components/ui/Alert'

export default function LoginPage() {
  const { loginMutation } = useAuth()
  const [form, setForm] = useState({ email: '', password: '' })
  const [errors, setErrors] = useState({})

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }))

  const validate = () => {
    const errs = {}
    if (!form.email) errs.email = 'Email is required'
    if (!form.password) errs.password = 'Password is required'
    setErrors(errs)
    return Object.keys(errs).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validate()) return
    try {
      await loginMutation.mutateAsync(form)
    } catch (err) {
      setErrors({ form: err.response?.data?.detail || 'Invalid credentials' })
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-gray-50">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-gray-900">Welcome back</h1>
            <p className="text-gray-500 text-sm mt-1">Sign in to your EventHub account</p>
          </div>

          {errors.form && <Alert type="error" className="mb-4">{errors.form}</Alert>}

          <form onSubmit={handleSubmit} noValidate className="space-y-4">
            <Input
              id="email" label="Email address" type="email"
              value={form.email} onChange={set('email')}
              error={errors.email} autoComplete="email"
            />
            <Input
              id="password" label="Password" type="password"
              value={form.password} onChange={set('password')}
              error={errors.password} autoComplete="current-password"
            />
            <div className="flex justify-end">
              <Link to="/reset-password" className="text-sm text-blue-600 hover:underline focus:ring-2 focus:ring-blue-500 rounded">
                Forgot password?
              </Link>
            </div>
            <Button type="submit" loading={loginMutation.isPending} className="w-full" size="lg">
              Sign In
            </Button>
          </form>

          <p className="text-center text-sm text-gray-500 mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-blue-600 font-medium hover:underline focus:ring-2 focus:ring-blue-500 rounded">
              Register free
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
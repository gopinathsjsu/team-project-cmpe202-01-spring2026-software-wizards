import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import Alert from '../components/ui/Alert'

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')
  const { requestResetMutation, resetPasswordMutation } = useAuth()
  const [email, setEmail] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [done, setDone] = useState(false)
  const [error, setError] = useState('')

  const handleRequest = async (e) => {
    e.preventDefault()
    await requestResetMutation.mutateAsync(email)
    setDone(true)
  }

  const handleReset = async (e) => {
    e.preventDefault()
    try {
      await resetPasswordMutation.mutateAsync({ token, new_password: newPassword })
    } catch (err) {
      setError(err.response?.data?.detail || 'Reset failed')
    }
  }

  if (token) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4 bg-gray-50">
        <div className="w-full max-w-md bg-white rounded-2xl border border-gray-200 p-8 shadow-sm">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Set New Password</h1>
          {error && <Alert type="error" className="mb-4">{error}</Alert>}
          <form onSubmit={handleReset} noValidate className="space-y-4">
            <Input id="new_password" label="New Password" type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} autoComplete="new-password" />
            <Button type="submit" loading={resetPasswordMutation.isPending} className="w-full">Reset Password</Button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-gray-50">
      <div className="w-full max-w-md bg-white rounded-2xl border border-gray-200 p-8 shadow-sm">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Reset Password</h1>
        <p className="text-sm text-gray-500 mb-6">Enter your email and we'll send you a reset link.</p>
        {done ? (
          <Alert type="success">If that email is registered, a reset link is on its way!</Alert>
        ) : (
          <form onSubmit={handleRequest} noValidate className="space-y-4">
            <Input id="reset_email" label="Email address" type="email" value={email} onChange={(e) => setEmail(e.target.value)} autoComplete="email" />
            <Button type="submit" loading={requestResetMutation.isPending} className="w-full">Send Reset Link</Button>
          </form>
        )}
      </div>
    </div>
  )
}

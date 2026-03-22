import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import api from '../api/client'
import useAuthStore from '../store/authStore'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import Alert from '../components/ui/Alert'

export default function ProfilePage() {
  const { user, updateUser } = useAuthStore()
  const [form, setForm] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    bio: user?.bio || '',
    avatar_url: user?.avatar_url || '',
  })
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  const updateMutation = useMutation({
    mutationFn: (data) => api.put('/users/me', data).then((r) => r.data),
    onSuccess: (data) => {
      updateUser(data)
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    },
    onError: (err) => setError(err.response?.data?.detail || 'Update failed'),
  })

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }))

  return (
    <div className="max-w-2xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">My Profile</h1>

      {success && <Alert type="success" className="mb-4">Profile updated successfully!</Alert>}
      {error && <Alert type="error" className="mb-4">{error}</Alert>}

      <div className="bg-white border border-gray-200 rounded-2xl p-6 space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <Input id="first_name" label="First Name" value={form.first_name} onChange={set('first_name')} />
          <Input id="last_name" label="Last Name" value={form.last_name} onChange={set('last_name')} />
        </div>
        <Input id="bio" label="Bio" value={form.bio} onChange={set('bio')} />
        <Input id="avatar_url" label="Avatar URL" type="url" value={form.avatar_url} onChange={set('avatar_url')} />

        <div className="pt-2">
          <p className="text-sm text-gray-500 mb-1">Role: <strong>{user?.role}</strong></p>
          <p className="text-sm text-gray-500">Email: <strong>{user?.email}</strong></p>
        </div>

        <Button
          onClick={() => updateMutation.mutate(form)}
          loading={updateMutation.isPending}
        >
          Save Changes
        </Button>
      </div>
    </div>
  )
}

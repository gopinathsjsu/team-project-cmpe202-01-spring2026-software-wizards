import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'
import useAuthStore from '../store/authStore'

export function useAuth() {
  const navigate = useNavigate()
  const { login, logout } = useAuthStore()

  const loginMutation = useMutation({
    mutationFn: (credentials) => api.post('/auth/login', credentials),
    onSuccess: ({ data }) => {
      login(data.user, data.access_token, data.refresh_token)
      navigate('/')
    },
  })

  const registerMutation = useMutation({
    mutationFn: (userData) => api.post('/auth/register', userData),
    onSuccess: ({ data }) => {
      login(data.user, data.access_token, data.refresh_token)
      navigate('/')
    },
  })

  const requestResetMutation = useMutation({
    mutationFn: (email) => api.post('/auth/request-password-reset', { email }),
  })

  const resetPasswordMutation = useMutation({
    mutationFn: ({ token, new_password }) =>
      api.post('/auth/reset-password', { token, new_password }),
    onSuccess: () => navigate('/login'),
  })

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return {
    loginMutation,
    registerMutation,
    requestResetMutation,
    resetPasswordMutation,
    logout: handleLogout,
  }
}
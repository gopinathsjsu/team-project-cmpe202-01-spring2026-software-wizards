/**
 * Custom Hook Pattern — admin-specific mutations.
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../api/client'

export function useAdminEvents(params = {}, options = {}) {
  return useQuery({
    queryKey: ['admin-events', params],
    queryFn: () => api.get('/admin/events', { params }).then((r) => r.data),
    ...options,
  })
}

export function useAdminUsers(params = {}) {
  return useQuery({
    queryKey: ['admin-users', params],
    queryFn: () => api.get('/admin/users', { params }).then((r) => r.data),
  })
}

export function useAdmin() {
  const queryClient = useQueryClient()

  const approveEvent = useMutation({
    mutationFn: (id) => api.put(`/admin/events/${id}/approve`).then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-events'] }),
  })

  const rejectEvent = useMutation({
    mutationFn: ({ id, reason }) =>
      api.put(`/admin/events/${id}/reject`, null, { params: { reason } }).then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-events'] }),
  })

  const suspendUser = useMutation({
    mutationFn: (id) => api.put(`/admin/users/${id}/suspend`).then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-users'] }),
  })

  const reactivateUser = useMutation({
    mutationFn: (id) => api.put(`/admin/users/${id}/reactivate`).then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-users'] }),
  })

  return { approveEvent, rejectEvent, suspendUser, reactivateUser }
}

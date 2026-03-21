/**
 * Custom Hook Pattern — registration mutations with query invalidation.
 * Mirrors the Observer pattern: success invalidates related cached queries.
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../api/client'

export function useRegistration() {
  const queryClient = useQueryClient()

  const register = useMutation({
    mutationFn: (data) => api.post('/registrations', data).then((r) => r.data),
    onSuccess: () => {
      // Observer-like: invalidate caches so ticket counts refresh
      queryClient.invalidateQueries({ queryKey: ['events'] })
      queryClient.invalidateQueries({ queryKey: ['my-registrations'] })
    },
  })

  const cancel = useMutation({
    mutationFn: (id) => api.delete(`/registrations/${id}`).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['my-registrations'] })
      queryClient.invalidateQueries({ queryKey: ['events'] })
    },
  })

  const checkin = useMutation({
    mutationFn: ({ eventId, registrationId }) =>
      api.post(`/events/${eventId}/checkin/${registrationId}`).then((r) => r.data),
    onSuccess: (_, { eventId }) => {
      queryClient.invalidateQueries({ queryKey: ['attendees', eventId] })
    },
  })

  return { register, cancel, checkin }
}

export function useMyRegistrations(params = {}) {
  return useQuery({
    queryKey: ['my-registrations', params],
    queryFn: () => api.get('/registrations', { params }).then((r) => r.data),
  })
}

export function useRegistrationDetail(id) {
  return useQuery({
    queryKey: ['registration', id],
    queryFn: () => api.get(`/registrations/${id}`).then((r) => r.data),
    enabled: !!id,
  })
}

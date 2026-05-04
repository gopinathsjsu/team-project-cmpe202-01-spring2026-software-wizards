/**
 * Custom Hook Pattern — encapsulates event fetching logic.
 * Returns React Query results so components stay lean.
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../api/client'

export function useEvents(params = {}) {
  return useQuery({
    queryKey: ['events', params],
    queryFn: () => api.get('/events', { params }).then((r) => r.data),
  })
}

export function useEvent(id) {
  return useQuery({
    queryKey: ['events', id],
    queryFn: () => api.get(`/events/${id}`).then((r) => r.data),
    enabled: !!id,
  })
}

export function useMyEvents(params = {}) {
  return useQuery({
    queryKey: ['my-events', params],
    queryFn: () => api.get('/events/mine', { params }).then((r) => r.data),
  })
}

export function useCategories() {
  return useQuery({
    queryKey: ['categories'],
    queryFn: () => api.get('/categories').then((r) => r.data),
    staleTime: 5 * 60_000,
  })
}

export function useCreateEvent() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data) => api.post('/events', data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['events'] })
      queryClient.invalidateQueries({ queryKey: ['my-events'] })
    },
  })
}

export function useUpdateEvent(id) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data) => api.put(`/events/${id}`, data).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['events', id] })
      queryClient.invalidateQueries({ queryKey: ['events'] })
    },
  })
}

export function useSubmitEvent() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id) => api.post(`/events/${id}/submit`).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['events'] })
      queryClient.invalidateQueries({ queryKey: ['my-events'] })
    },
  })
}

export function useDeleteEvent() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id) => api.delete(`/events/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['events'] })
      queryClient.invalidateQueries({ queryKey: ['my-events'] })
    },
  })
}

export function useCreateTicket(eventId) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data) => api.post(`/events/${eventId}/tickets`, data).then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['events', eventId] }),
  })
}

export function useEventAttendees(eventId, params = {}) {
  return useQuery({
    queryKey: ['attendees', eventId, params],
    queryFn: () => api.get(`/events/${eventId}/attendees`, { params }).then((r) => r.data),
    enabled: !!eventId,
  })
}

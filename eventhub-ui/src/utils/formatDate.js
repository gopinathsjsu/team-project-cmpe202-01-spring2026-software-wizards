import { format, formatDistanceToNow, isPast } from 'date-fns'

export const formatEventDate = (dateStr) =>
  format(new Date(dateStr), 'EEEE, MMMM d, yyyy')

export const formatEventTime = (dateStr) =>
  format(new Date(dateStr), 'h:mm a')

export const formatEventDateTime = (dateStr) =>
  format(new Date(dateStr), 'MMM d, yyyy · h:mm a')

export const formatRelative = (dateStr) =>
  formatDistanceToNow(new Date(dateStr), { addSuffix: true })

export const isEventPast = (dateStr) => isPast(new Date(dateStr))

export const formatPrice = (price) =>
  price === 0 ? 'Free' : `$${Number(price).toFixed(2)}`

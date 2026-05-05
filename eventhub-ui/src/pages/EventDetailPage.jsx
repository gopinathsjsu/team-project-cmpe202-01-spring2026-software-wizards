import { useState } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { MapPin, Calendar, Users, Globe, Tag, ExternalLink } from 'lucide-react'
import { useEvent } from '../hooks/useEvents'
import { useAdmin } from '../hooks/useAdmin'
import EventMap from '../components/map/EventMap'
import TicketSelector from '../components/tickets/TicketSelector'
import QRCodeDisplay from '../components/tickets/QRCodeDisplay'
import Badge from '../components/ui/Badge'
import Modal from '../components/ui/Modal'
import Button from '../components/ui/Button'
import Spinner from '../components/ui/Spinner'
import Input from '../components/ui/Input'
import { formatEventDate, formatEventTime, formatPrice } from '../utils/formatDate'
import api from '../api/client'
import useAuthStore from '../store/authStore'

export default function EventDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const isAdmin = user?.role === 'admin'
  const { approveEvent, rejectEvent } = useAdmin()
  const { data: event, isLoading, isError } = useEvent(id)
  const [regResult, setRegResult] = useState(null)
  const [calLinks, setCalLinks] = useState(null)
  const [rejectOpen, setRejectOpen] = useState(false)
  const [rejectReason, setRejectReason] = useState('')

  const fetchCalLinks = async () => {
    const { data } = await api.get(`/events/${id}/calendar-link`)
    setCalLinks(data)
  }

  const handleApprove = async () => {
    await approveEvent.mutateAsync(event.id)
    navigate('/admin/events')
  }

  const handleReject = async () => {
    await rejectEvent.mutateAsync({ id: event.id, reason: rejectReason })
    setRejectOpen(false)
    setRejectReason('')
    navigate('/admin/events')
  }

  if (isLoading) return <div className="flex justify-center py-32"><Spinner size="lg" /></div>
  if (isError || !event) return (
    <div className="text-center py-32">
      <p className="text-2xl font-bold text-gray-700">Event not found</p>
      <Link to="/events" className="text-blue-600 hover:underline mt-2 block">Back to events</Link>
    </div>
  )

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {isAdmin && event.status === 'pending' && (
        <div className="sticky top-16 z-30 mb-6 bg-white border border-gray-200 rounded-xl px-4 py-3 flex items-center justify-between shadow-sm">
          <div>
            <p className="text-sm font-medium text-gray-900">Admin review</p>
            <p className="text-xs text-gray-500">Approve or reject this pending event</p>
          </div>
          <div className="flex items-center gap-2">
            <Button size="sm" onClick={handleApprove} loading={approveEvent.isPending}>
              Approve
            </Button>
            <Button variant="danger" size="sm" onClick={() => setRejectOpen(true)}>
              Reject
            </Button>
          </div>
        </div>
      )}

      {/* Banner */}
      {event.banner_url ? (
        <img
          src={event.banner_url}
          alt={`Banner for ${event.title}`}
          className="w-full h-64 sm:h-80 object-cover rounded-2xl mb-8"
        />
      ) : (
        <div className="w-full h-48 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mb-8 flex items-center justify-center" aria-hidden="true">
          <span className="text-6xl">{event.category?.icon || '🎟️'}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        {/* Main info */}
        <div className="lg:col-span-2 space-y-6">
          <div>
            {event.category && (
              <p className="text-sm text-blue-600 font-medium mb-1">
                {event.category.icon} {event.category.name}
              </p>
            )}
            <h1 className="text-3xl font-extrabold text-gray-900">{event.title}</h1>
            <Badge status={event.status} className="mt-2">{event.status.charAt(0).toUpperCase() + event.status.slice(1)}</Badge>
          </div>

          {/* Meta */}
          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <Calendar size={16} aria-hidden="true" className="text-blue-500" />
              <time dateTime={event.start_at}>
                {formatEventDate(event.start_at)} · {formatEventTime(event.start_at)} – {formatEventTime(event.end_at)}
              </time>
            </div>
            <div className="flex items-center gap-2">
              <MapPin size={16} aria-hidden="true" className="text-blue-500" />
              <span>{event.is_virtual ? 'Virtual Event' : `${event.venue_name || ''}, ${event.city || ''}`}</span>
            </div>
            <div className="flex items-center gap-2">
              <Users size={16} aria-hidden="true" className="text-blue-500" />
              <span>{event.registration_count} attending · {event.capacity} capacity</span>
            </div>
            {event.is_virtual && (
              <div className="flex items-center gap-2">
                <Globe size={16} aria-hidden="true" className="text-blue-500" />
                <span>Online Event</span>
              </div>
            )}
          </div>

          {/* Tags */}
          {event.tags?.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {event.tags.map((tag) => (
                <span key={tag} className="flex items-center gap-1 bg-gray-100 text-gray-700 rounded-full px-3 py-1 text-xs">
                  <Tag size={11} aria-hidden="true" /> {tag}
                </span>
              ))}
            </div>
          )}

          {/* Description */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">About this event</h2>
            <p className="text-gray-600 leading-relaxed whitespace-pre-line">{event.description}</p>
          </div>

          {/* Organizer */}
          {event.organizer && (
            <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-xl">
              <div className="h-10 w-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold" aria-hidden="true">
                {event.organizer.first_name[0]}
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">
                  Organized by {event.organizer.first_name} {event.organizer.last_name}
                </p>
                {event.organizer.bio && <p className="text-xs text-gray-500 mt-0.5">{event.organizer.bio}</p>}
              </div>
            </div>
          )}

          {/* Map */}
          <EventMap event={event} />

          {/* Calendar links */}
          {!isAdmin && (
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-3">Add to Calendar</h2>
              <div className="flex flex-wrap gap-3">
                {calLinks ? (
                  <>
                    <a href={calLinks.google} target="_blank" rel="noopener noreferrer"
                      className="flex items-center gap-1.5 text-sm text-blue-600 hover:underline focus:ring-2 focus:ring-blue-500 rounded">
                      <ExternalLink size={14} aria-hidden="true" /> Google Calendar
                    </a>
                    <a href={calLinks.outlook} target="_blank" rel="noopener noreferrer"
                      className="flex items-center gap-1.5 text-sm text-blue-600 hover:underline focus:ring-2 focus:ring-blue-500 rounded">
                      <ExternalLink size={14} aria-hidden="true" /> Outlook
                    </a>
                    <a href={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/events/${event.id}/calendar.ics`} download
                      className="flex items-center gap-1.5 text-sm text-blue-600 hover:underline focus:ring-2 focus:ring-blue-500 rounded">
                      Download .ics
                    </a>
                  </>
                ) : (
                  <button onClick={fetchCalLinks} className="text-sm text-blue-600 hover:underline focus:ring-2 focus:ring-blue-500 rounded">
                    Show calendar options
                  </button>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Ticket sidebar */}
        {!isAdmin && (
          <aside className="space-y-4">
            <div className="sticky top-24 bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
              <h2 className="text-lg font-semibold text-gray-900 mb-1">Get Tickets</h2>
              {event.ticket_types?.length > 0 && (
                <p className="text-sm text-gray-500 mb-4">
                  From {formatPrice(Math.min(...event.ticket_types.map(t => t.price)))}
                </p>
              )}
              {event.status === 'published' ? (
                <TicketSelector
                  event={event}
                  onSuccess={(result) => setRegResult(result)}
                />
              ) : (
                <p className="text-sm text-gray-500">Registration is not currently available for this event.</p>
              )}
            </div>
          </aside>
        )}
      </div>

      {/* Success modal */}
      <Modal
        isOpen={!!regResult}
        onClose={() => setRegResult(null)}
        title="Registration Confirmed! 🎉"
      >
        {regResult && (
          <div className="space-y-4">
            <p className="text-sm text-gray-600">
              You're registered for <strong>{event.title}</strong>.
              A confirmation email is on its way!
            </p>
            <QRCodeDisplay qrToken={regResult.qr_token} eventTitle={event.title} />
            <p className="text-xs text-gray-500 text-center">
              Reference: {regResult.payment_ref || 'Free ticket'}
            </p>
          </div>
        )}
      </Modal>

      {/* Reject modal */}
      <Modal isOpen={rejectOpen} onClose={() => setRejectOpen(false)} title="Reject Event">
        <div className="space-y-4">
          <Input
            id="reject_reason"
            label="Rejection reason (optional)"
            value={rejectReason}
            onChange={(e) => setRejectReason(e.target.value)}
            placeholder="Missing required details…"
          />
          <div className="flex justify-end gap-3">
            <Button variant="secondary" onClick={() => setRejectOpen(false)}>Cancel</Button>
            <Button variant="danger" onClick={handleReject} loading={rejectEvent.isPending}>Confirm Reject</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}

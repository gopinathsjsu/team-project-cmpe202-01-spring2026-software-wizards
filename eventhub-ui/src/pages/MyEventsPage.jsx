import { Link } from 'react-router-dom'
import { Plus, Edit, Trash2, CheckCircle, Clock } from 'lucide-react'
import { useMyEvents, useSubmitEvent, useDeleteEvent } from '../hooks/useEvents'
import useAuthStore from '../store/authStore'
import Badge from '../components/ui/Badge'
import Button from '../components/ui/Button'
import Spinner from '../components/ui/Spinner'
import { formatEventDateTime } from '../utils/formatDate'

export default function MyEventsPage() {
  const { user } = useAuthStore()
  const { data, isLoading } = useMyEvents({ size: 50 })
  const submitEvent = useSubmitEvent()
  const deleteEvent = useDeleteEvent()

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">My Events</h1>
        {['organizer', 'admin'].includes(user?.role) && (
          <Link to="/dashboard/events/new">
            <Button><Plus size={16} aria-hidden="true" /> Create Event</Button>
          </Link>
        )}
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20"><Spinner size="lg" /></div>
      ) : data?.items?.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <p className="text-4xl mb-3" aria-hidden="true">📅</p>
          <p className="font-medium">No events yet</p>
          <Link to="/dashboard/events/new" className="text-blue-600 hover:underline text-sm mt-1 block">Create your first event</Link>
        </div>
      ) : (
        <div className="space-y-3">
          {data?.items?.map((event) => (
            <div key={event.id} className="bg-white border border-gray-200 rounded-xl p-5 flex items-center justify-between gap-4">
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-gray-900 truncate">{event.title}</p>
                <p className="text-sm text-gray-500 mt-0.5">
                  <time dateTime={event.start_at}>{formatEventDateTime(event.start_at)}</time>
                  {event.city && ` · ${event.city}`}
                </p>
                <Badge status={event.status} className="mt-2">
                  {event.status.charAt(0).toUpperCase() + event.status.slice(1)}
                </Badge>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                {event.status === 'draft' || event.status === 'rejected' ? (
                  <>
                    <Link to={`/dashboard/events/${event.id}/edit`}>
                      <Button variant="secondary" size="sm" aria-label={`Edit ${event.title}`}>
                        <Edit size={14} aria-hidden="true" />
                      </Button>
                    </Link>
                    <Button
                      size="sm"
                      onClick={() => submitEvent.mutate(event.id)}
                      loading={submitEvent.isPending}
                      aria-label={`Submit ${event.title} for review`}
                    >
                      <CheckCircle size={14} aria-hidden="true" /> Submit
                    </Button>
                  </>
                ) : event.status === 'pending' ? (
                  <div className="flex items-center gap-1 text-sm text-yellow-600">
                    <Clock size={14} aria-hidden="true" /> Under Review
                  </div>
                ) : (
                  <Link to={`/events/${event.id}/attendees`}>
                    <Button variant="secondary" size="sm">Attendees</Button>
                  </Link>
                )}
                {event.status !== 'cancelled' && (
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => confirm('Cancel this event?') && deleteEvent.mutate(event.id)}
                    aria-label={`Cancel event ${event.title}`}
                  >
                    <Trash2 size={14} aria-hidden="true" />
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

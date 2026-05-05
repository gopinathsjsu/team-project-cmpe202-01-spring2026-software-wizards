import { useParams, Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { useEventAttendees, useEvent } from '../hooks/useEvents'
import Spinner from '../components/ui/Spinner'
import { formatEventDateTime } from '../utils/formatDate'

export default function EventAttendeesPage() {
  const { id } = useParams()
  const { data, isLoading } = useEventAttendees(id)
  const { data: event } = useEvent(id)

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <Link to="/my-events" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-800 mb-6">
        <ArrowLeft size={14} /> Back to My Events
      </Link>

      <h1 className="text-2xl font-bold text-gray-900">Attendees</h1>
      {event?.title && (
        <p className="text-gray-500 mt-1 mb-6">{event.title}</p>
      )}
      {!event?.title && <div className="mb-6" />}

      {isLoading ? (
        <div className="flex justify-center py-20"><Spinner size="lg" /></div>
      ) : !data?.items?.length ? (
        <div className="text-center py-20 text-gray-500">
          <p className="text-4xl mb-3" aria-hidden="true">👥</p>
          <p className="font-medium">No registrations yet</p>
        </div>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-gray-200">
          <table className="min-w-full divide-y divide-gray-200 text-sm">
            <thead className="bg-gray-50">
              <tr>
                {['Name', 'Email', 'Ticket', 'Qty', 'Amount', 'Status', 'Registered'].map((h) => (
                  <th key={h} className="px-4 py-3 text-left font-semibold text-gray-600">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 bg-white">
              {data.items.map((a) => (
                <tr key={a.attendee_id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium text-gray-900">{a.first_name} {a.last_name}</td>
                  <td className="px-4 py-3 text-gray-600">{a.email}</td>
                  <td className="px-4 py-3 text-gray-600">{a.ticket_name}</td>
                  <td className="px-4 py-3 text-gray-600">{a.quantity}</td>
                  <td className="px-4 py-3 text-gray-600">${Number(a.total_amount).toFixed(2)}</td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                      a.status === 'confirmed' ? 'bg-green-100 text-green-700' :
                      a.status === 'cancelled' ? 'bg-red-100 text-red-700' :
                      'bg-gray-100 text-gray-600'
                    }`}>
                      {a.status.charAt(0).toUpperCase() + a.status.slice(1)}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-500">{formatEventDateTime(a.registered_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="px-4 py-2 text-xs text-gray-400 border-t border-gray-100">
            {data.total} registration{data.total !== 1 ? 's' : ''} total
          </p>
        </div>
      )}
    </div>
  )
}

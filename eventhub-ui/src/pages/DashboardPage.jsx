import { Link } from 'react-router-dom'
import { Plus, Calendar, Users, TrendingUp } from 'lucide-react'
import { useEvents } from '../hooks/useEvents'
import useAuthStore from '../store/authStore'
import Badge from '../components/ui/Badge'
import Button from '../components/ui/Button'
import Spinner from '../components/ui/Spinner'
import { formatEventDateTime } from '../utils/formatDate'

export default function DashboardPage() {
  const { user } = useAuthStore()
  const { data, isLoading } = useEvents({ organizer_id: user?.id, size: 10 })

  const stats = {
    total: data?.total || 0,
    published: data?.items?.filter(e => e.status === 'published').length || 0,
    pending: data?.items?.filter(e => e.status === 'pending').length || 0,
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500 text-sm mt-1">Welcome back, {user?.first_name}!</p>
        </div>
        <Link to="/dashboard/events/new">
          <Button><Plus size={16} aria-hidden="true" /> New Event</Button>
        </Link>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        {[
          { label: 'Total Events', value: stats.total, icon: Calendar, color: 'text-blue-600 bg-blue-50' },
          { label: 'Published', value: stats.published, icon: TrendingUp, color: 'text-green-600 bg-green-50' },
          { label: 'Pending Review', value: stats.pending, icon: Users, color: 'text-yellow-600 bg-yellow-50' },
        ].map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="bg-white border border-gray-200 rounded-xl p-5 flex items-center gap-4">
            <div className={`h-12 w-12 rounded-xl flex items-center justify-center ${color}`}>
              <Icon size={22} aria-hidden="true" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{value}</p>
              <p className="text-sm text-gray-500">{label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Recent events */}
      <div className="bg-white border border-gray-200 rounded-2xl">
        <div className="flex items-center justify-between px-6 py-4 border-b">
          <h2 className="font-semibold text-gray-900">Recent Events</h2>
          <Link to="/my-events" className="text-sm text-blue-600 hover:underline">View all</Link>
        </div>

        {isLoading ? (
          <div className="flex justify-center py-10"><Spinner /></div>
        ) : data?.items?.length === 0 ? (
          <div className="text-center py-10 text-gray-500">
            <p>No events yet.</p>
            <Link to="/dashboard/events/new" className="text-blue-600 hover:underline text-sm">Create one</Link>
          </div>
        ) : (
          <div>
            {data?.items?.map((event) => (
              <div key={event.id} className="flex items-center justify-between px-6 py-4 border-b last:border-0 hover:bg-gray-50">
                <div>
                  <Link to={`/events/${event.id}`} className="font-medium text-gray-900 hover:text-blue-600">{event.title}</Link>
                  <p className="text-sm text-gray-500 mt-0.5"><time dateTime={event.start_at}>{formatEventDateTime(event.start_at)}</time></p>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-sm text-gray-500">{event.registration_count} registered</span>
                  <Badge status={event.status}>{event.status.charAt(0).toUpperCase() + event.status.slice(1)}</Badge>
                  <Link to={`/dashboard/events/${event.id}/edit`} className="text-sm text-blue-600 hover:underline focus:ring-2 focus:ring-blue-500 rounded">Edit</Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

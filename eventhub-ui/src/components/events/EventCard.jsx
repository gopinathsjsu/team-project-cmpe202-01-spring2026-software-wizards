import { Link } from 'react-router-dom'
import { MapPin, Calendar, Users } from 'lucide-react'
import Badge from '../ui/Badge'
import { formatEventDateTime, formatPrice } from '../../utils/formatDate'

export default function EventCard({ event }) {
  const minPrice = formatPrice(event.min_price ?? 0)

  return (
    <article className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
      <Link to={`/events/${event.id}`} aria-label={`View details for ${event.title}`}>
        {event.banner_url ? (
          <img
            src={event.banner_url}
            alt={`Banner for ${event.title}`}
            className="w-full h-44 object-cover"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-44 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center" aria-hidden="true">
            <span className="text-4xl">{event.category?.icon || '🎟️'}</span>
          </div>
        )}
      </Link>
      <div className="p-4">
        {event.category && (
          <p className="text-xs text-blue-600 font-medium mb-1">
            {event.category.icon} {event.category.name}
          </p>
        )}
        <Link to={`/events/${event.id}`} className="hover:underline">
          <h3 className="font-semibold text-gray-900 text-base leading-snug line-clamp-2">{event.title}</h3>
        </Link>
        <div className="mt-2 space-y-1 text-sm text-gray-500">
          <div className="flex items-center gap-1.5">
            <Calendar size={13} aria-hidden="true" />
            <time dateTime={event.start_at}>{formatEventDateTime(event.start_at)}</time>
          </div>
          {event.city && (
            <div className="flex items-center gap-1.5">
              <MapPin size={13} aria-hidden="true" />
              <span>{event.is_virtual ? 'Virtual' : event.city}</span>
            </div>
          )}
          <div className="flex items-center gap-1.5">
            <Users size={13} aria-hidden="true" />
            <span>{event.registration_count} registered</span>
          </div>
        </div>
        <div className="mt-3 flex items-center justify-between">
          <Badge status={minPrice === 'Free' ? 'free' : 'paid'}>
            {minPrice}
          </Badge>
          {event.is_virtual && <Badge status="published">Virtual</Badge>}
        </div>
      </div>
    </article>
  )
}

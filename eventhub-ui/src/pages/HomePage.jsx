import { Link, useNavigate } from 'react-router-dom'
import { useEvents, useCategories } from '../hooks/useEvents'
import EventCard from '../components/events/EventCard'
import SearchBar from '../components/events/SearchBar'
import Spinner from '../components/ui/Spinner'

export default function HomePage() {
  const navigate = useNavigate()
  const { data: featuredData, isLoading } = useEvents({ sort: 'popularity', size: 6 })
  const { data: categories = [] } = useCategories()

  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-blue-600 to-purple-700 text-white py-20 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl font-extrabold mb-4">
            Discover Events Near You
          </h1>
          <p className="text-blue-100 text-lg mb-8">
            Conferences, concerts, workshops, hackathons — find and register in seconds.
          </p>
          <SearchBar onSearch={(q) => navigate(`/events?q=${encodeURIComponent(q)}`)} />
        </div>
      </section>

      {/* Category quick-links */}
      {categories.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Browse by Category</h2>
          <div className="flex flex-wrap gap-3">
            {categories.map((cat) => (
              <Link
                key={cat.id}
                to={`/events?category_id=${cat.id}`}
                className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-full text-sm font-medium text-gray-700 hover:border-blue-400 hover:text-blue-600 transition-colors focus:ring-2 focus:ring-blue-500"
              >
                <span aria-hidden="true">{cat.icon}</span> {cat.name}
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Featured events */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900">Popular Events</h2>
          <Link to="/events" className="text-sm text-blue-600 hover:underline font-medium">
            View all →
          </Link>
        </div>

        {isLoading ? (
          <div className="flex justify-center py-12"><Spinner size="lg" /></div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredData?.items?.map((event) => (
              <EventCard key={event.id} event={event} />
            ))}
          </div>
        )}
      </section>
    </div>
  )
}

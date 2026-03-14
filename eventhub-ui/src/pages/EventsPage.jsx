import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useEvents } from '../hooks/useEvents'
import EventCard from '../components/events/EventCard'
import SearchBar from '../components/events/SearchBar'
import FilterPanel from '../components/events/FilterPanel'
import Spinner from '../components/ui/Spinner'
import Button from '../components/ui/Button'

export default function EventsPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [page, setPage] = useState(1)

  const [filters, setFilters] = useState({
    q: searchParams.get('q') || undefined,
    category_id: searchParams.get('category_id') || undefined,
    city: searchParams.get('city') || undefined,
    sort: searchParams.get('sort') || 'date',
    is_free: searchParams.get('is_free') || undefined,
    is_virtual: searchParams.get('is_virtual') || undefined,
  })

  const { data, isLoading, isError } = useEvents({ ...filters, page, size: 12 })

  // Sync filters → URL
  useEffect(() => {
    const params = {}
    Object.entries(filters).forEach(([k, v]) => { if (v !== undefined && v !== '') params[k] = v })
    setSearchParams(params, { replace: true })
    setPage(1)
  }, [filters])

  const handleFiltersChange = (newFilters) => setFilters(newFilters)
  const handleSearch = (q) => setFilters((f) => ({ ...f, q: q || undefined }))

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Browse Events</h1>

      <SearchBar defaultValue={filters.q || ''} onSearch={handleSearch} />

      <div className="mt-8 flex flex-col md:flex-row gap-8">
        {/* Filters sidebar */}
        <aside className="w-full md:w-56 shrink-0">
          <FilterPanel filters={filters} onChange={handleFiltersChange} />
        </aside>

        {/* Event grid */}
        <div className="flex-1">
          {isLoading ? (
            <div className="flex justify-center py-20"><Spinner size="lg" /></div>
          ) : isError ? (
            <p className="text-red-600 text-center py-10">Failed to load events. Please try again.</p>
          ) : data?.items?.length === 0 ? (
            <div className="text-center py-20 text-gray-500">
              <p className="text-5xl mb-4" aria-hidden="true">🔍</p>
              <p className="text-lg font-medium">No events found</p>
              <p className="text-sm">Try adjusting your filters.</p>
            </div>
          ) : (
            <>
              <p className="text-sm text-gray-500 mb-4">{data?.total} event{data?.total !== 1 ? 's' : ''} found</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {data?.items?.map((event) => (
                  <EventCard key={event.id} event={event} />
                ))}
              </div>

              {/* Pagination */}
              {data?.pages > 1 && (
                <div className="mt-10 flex justify-center items-center gap-3" aria-label="Pagination">
                  <Button
                    variant="secondary"
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    disabled={page === 1}
                  >
                    Previous
                  </Button>
                  <span className="text-sm text-gray-600">Page {page} of {data.pages}</span>
                  <Button
                    variant="secondary"
                    onClick={() => setPage((p) => Math.min(data.pages, p + 1))}
                    disabled={page === data.pages}
                  >
                    Next
                  </Button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

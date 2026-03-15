import { useCategories } from '../../hooks/useEvents'

export default function FilterPanel({ filters, onChange }) {
  const { data: categories = [] } = useCategories()

  const set = (key, value) => onChange({ ...filters, [key]: value })

  return (
    <aside className="space-y-5" aria-label="Event filters">
      <div>
        <label htmlFor="filter-category" className="block text-sm font-medium text-gray-700 mb-1">
          Category
        </label>
        <select
          id="filter-category"
          value={filters.category_id || ''}
          onChange={(e) => set('category_id', e.target.value || undefined)}
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Categories</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>{c.icon} {c.name}</option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="filter-city" className="block text-sm font-medium text-gray-700 mb-1">
          City
        </label>
        <input
          id="filter-city"
          type="text"
          placeholder="e.g. Austin"
          value={filters.city || ''}
          onChange={(e) => set('city', e.target.value || undefined)}
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label htmlFor="filter-sort" className="block text-sm font-medium text-gray-700 mb-1">
          Sort By
        </label>
        <select
          id="filter-sort"
          value={filters.sort || 'date'}
          onChange={(e) => set('sort', e.target.value)}
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
        >
          <option value="date">Upcoming</option>
          <option value="popularity">Most Popular</option>
          <option value="recent">Recently Added</option>
        </select>
      </div>

      <fieldset>
        <legend className="text-sm font-medium text-gray-700 mb-2">Filters</legend>
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
            <input
              type="checkbox"
              checked={filters.is_free === 'true' || filters.is_free === true}
              onChange={(e) => set('is_free', e.target.checked ? true : undefined)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            Free events only
          </label>
          <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
            <input
              type="checkbox"
              checked={filters.is_virtual === 'true' || filters.is_virtual === true}
              onChange={(e) => set('is_virtual', e.target.checked ? true : undefined)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            Virtual events only
          </label>
        </div>
      </fieldset>
    </aside>
  )
}

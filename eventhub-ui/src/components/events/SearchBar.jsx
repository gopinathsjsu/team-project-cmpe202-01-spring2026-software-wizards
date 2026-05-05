import { useState } from 'react'
import { Search } from 'lucide-react'
import Button from '../ui/Button'

export default function SearchBar({ defaultValue = '', onSearch }) {
  const [q, setQ] = useState(defaultValue)

  const handleSubmit = (e) => {
    e.preventDefault()
    onSearch(q)
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2" role="search">
      <label htmlFor="event-search" className="sr-only">Search events</label>
      <div className="relative flex-1">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 h-4 w-4" aria-hidden="true" />
        <input
          id="event-search"
          type="search"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search events, topics, speakers…"
          className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg text-sm text-black placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <Button type="submit" size="md">Search</Button>
    </form>
  )
}

import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Menu, X, ChevronDown, Search } from 'lucide-react'
import useAuthStore from '../../store/authStore'
import { useAuth } from '../../hooks/useAuth'
import { useCategories } from '../../hooks/useEvents'

export default function Navbar() {
  const { user } = useAuthStore()
  const { logout } = useAuth()
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const [catMenuOpen, setCatMenuOpen] = useState(false)
  const [searchQ, setSearchQ] = useState('')
  const { data: categories = [] } = useCategories()

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQ.trim()) navigate(`/events?q=${encodeURIComponent(searchQ.trim())}`)
  }

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" aria-label="Main navigation">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 font-bold text-xl text-blue-600">
            🎟️ EventHub
          </Link>

          {/* Center — search + categories (hidden on mobile) */}
          <div className="hidden sm:flex items-center gap-4 flex-1 max-w-xl mx-8">
            <form onSubmit={handleSearch} className="flex-1 flex" role="search">
              <label htmlFor="nav-search" className="sr-only">Search events</label>
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 h-4 w-4" aria-hidden="true" />
                <input
                  id="nav-search"
                  type="search"
                  placeholder="Search events…"
                  value={searchQ}
                  onChange={(e) => setSearchQ(e.target.value)}
                  className="w-full pl-9 pr-4 py-2 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </form>

            {/* Category dropdown */}
            <div className="relative">
              <button
                onClick={() => setCatMenuOpen(!catMenuOpen)}
                aria-expanded={catMenuOpen}
                aria-haspopup="true"
                className="flex items-center gap-1 text-sm text-gray-600 hover:text-blue-600 focus:ring-2 focus:ring-blue-500 rounded px-2 py-1"
              >
                Categories <ChevronDown size={14} aria-hidden="true" />
              </button>
              {catMenuOpen && (
                <div className="absolute top-full right-0 mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                  {categories.map((cat) => (
                    <Link
                      key={cat.id}
                      to={`/events?category_id=${cat.id}`}
                      onClick={() => setCatMenuOpen(false)}
                      className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                    >
                      <span aria-hidden="true">{cat.icon}</span> {cat.name}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Right — auth buttons */}
          <div className="hidden sm:flex items-center gap-3">
            {user ? (
              <div className="relative">
                <button
                  onClick={() => setUserMenuOpen(!userMenuOpen)}
                  aria-expanded={userMenuOpen}
                  aria-haspopup="true"
                  className="flex items-center gap-2 text-sm font-medium text-gray-700 hover:text-blue-600 focus:ring-2 focus:ring-blue-500 rounded px-2 py-1"
                >
                  {user.avatar_url
                    ? <img src={user.avatar_url} alt={`${user.first_name}'s avatar`} className="h-7 w-7 rounded-full object-cover" />
                    : <span className="h-7 w-7 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs font-bold" aria-hidden="true">{user.first_name[0]}</span>
                  }
                  {user.first_name}
                  <ChevronDown size={14} aria-hidden="true" />
                </button>
                {userMenuOpen && (
                  <div className="absolute right-0 mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                    <Link to="/my-registrations" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" onClick={() => setUserMenuOpen(false)}>My Tickets</Link>
                    {(user.role === 'organizer' || user.role === 'admin') && (
                      <Link to="/my-events" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" onClick={() => setUserMenuOpen(false)}>My Events</Link>
                    )}
                    {(user.role === 'organizer' || user.role === 'admin') && (
                      <Link to="/dashboard" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" onClick={() => setUserMenuOpen(false)}>Dashboard</Link>
                    )}
                    {user.role === 'admin' && (
                      <Link to="/admin" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" onClick={() => setUserMenuOpen(false)}>Admin</Link>
                    )}
                    <Link to="/profile" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" onClick={() => setUserMenuOpen(false)}>Profile</Link>
                    <hr className="my-1" />
                    <button onClick={() => { setUserMenuOpen(false); logout() }} className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50">
                      Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <Link to="/login" className="text-sm font-medium text-gray-700 hover:text-blue-600 focus:ring-2 focus:ring-blue-500 rounded px-2 py-1">Login</Link>
                <Link to="/register" className="bg-blue-600 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500">
                  Register
                </Link>
              </>
            )}
          </div>

          {/* Mobile hamburger */}
          <button
            className="sm:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100 focus:ring-2 focus:ring-blue-500"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-expanded={menuOpen}
            aria-label="Toggle navigation menu"
          >
            {menuOpen ? <X size={20} aria-hidden="true" /> : <Menu size={20} aria-hidden="true" />}
          </button>
        </div>

        {/* Mobile menu */}
        {menuOpen && (
          <div className="sm:hidden pb-4 border-t border-gray-100 pt-3 space-y-2">
            <form onSubmit={handleSearch} className="px-2">
              <label htmlFor="mobile-search" className="sr-only">Search events</label>
              <input
                id="mobile-search"
                type="search"
                placeholder="Search events…"
                value={searchQ}
                onChange={(e) => setSearchQ(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
              />
            </form>
            <Link to="/events" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded" onClick={() => setMenuOpen(false)}>Browse Events</Link>
            {user ? (
              <>
                <Link to="/my-registrations" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded" onClick={() => setMenuOpen(false)}>My Tickets</Link>
                {(user.role === 'organizer' || user.role === 'admin') && (
                  <Link to="/my-events" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded" onClick={() => setMenuOpen(false)}>My Events</Link>
                )}
                {(user.role === 'organizer' || user.role === 'admin') && (
                  <Link to="/dashboard" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded" onClick={() => setMenuOpen(false)}>Dashboard</Link>
                )}
                {user.role === 'admin' && (
                  <Link to="/admin" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded" onClick={() => setMenuOpen(false)}>Admin</Link>
                )}
                <Link to="/profile" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded" onClick={() => setMenuOpen(false)}>Profile</Link>
                <button onClick={() => { setMenuOpen(false); logout() }} className="block w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded">Logout</button>
              </>
            ) : (
              <>
                <Link to="/login" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded" onClick={() => setMenuOpen(false)}>Login</Link>
                <Link to="/register" className="block px-3 py-2 text-sm text-blue-600 font-medium hover:bg-blue-50 rounded" onClick={() => setMenuOpen(false)}>Register</Link>
              </>
            )}
          </div>
        )}
      </nav>
    </header>
  )
}
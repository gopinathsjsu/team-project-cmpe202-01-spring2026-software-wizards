import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center px-4 text-center">
      <p className="text-8xl font-black text-gray-200" aria-hidden="true">404</p>
      <h1 className="text-2xl font-bold text-gray-900 mt-4">Page not found</h1>
      <p className="text-gray-500 mt-2">The page you're looking for doesn't exist.</p>
      <Link to="/" className="mt-6 inline-flex items-center gap-2 bg-blue-600 text-white px-6 py-2.5 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 font-medium text-sm">
        Back to Home
      </Link>
    </div>
  )
}

const colors = {
  draft: 'bg-gray-100 text-gray-700',
  pending: 'bg-yellow-100 text-yellow-800',
  published: 'bg-green-100 text-green-800',
  cancelled: 'bg-red-100 text-red-800',
  rejected: 'bg-red-100 text-red-800',
  confirmed: 'bg-green-100 text-green-800',
  free: 'bg-blue-100 text-blue-800',
  paid: 'bg-purple-100 text-purple-800',
}

export default function Badge({ children, status, className = '' }) {
  const colorClass = colors[status] || 'bg-gray-100 text-gray-700'
  return (
    // Status badges always include text — color is not the only indicator (accessibility)
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colorClass} ${className}`}>
      {children}
    </span>
  )
}

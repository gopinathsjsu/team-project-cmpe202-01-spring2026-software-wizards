import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Calendar, MapPin, QrCode, X } from 'lucide-react'
import { useMyRegistrations } from '../hooks/useRegistration'
import { useRegistration } from '../hooks/useRegistration'
import QRCodeDisplay from '../components/tickets/QRCodeDisplay'
import Badge from '../components/ui/Badge'
import Modal from '../components/ui/Modal'
import Button from '../components/ui/Button'
import Spinner from '../components/ui/Spinner'
import Alert from '../components/ui/Alert'
import { formatEventDateTime, formatPrice } from '../utils/formatDate'

export default function MyRegistrationsPage() {
  const [filter, setFilter] = useState('all')
  const { data, isLoading } = useMyRegistrations(
    filter === 'upcoming' ? { upcoming: true } : filter !== 'all' ? { status: filter } : {}
  )
  const { cancel } = useRegistration()
  const [qrReg, setQrReg] = useState(null)
  const [cancelError, setCancelError] = useState('')

  const handleCancel = async (id) => {
    if (!confirm('Cancel this registration?')) return
    try {
      await cancel.mutateAsync(id)
    } catch (err) {
      setCancelError(err.response?.data?.detail || 'Cancellation failed')
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">My Tickets</h1>

      {cancelError && <Alert type="error" className="mb-4">{cancelError}</Alert>}

      {/* Filter tabs */}
      <div className="flex gap-2 mb-6" role="tablist" aria-label="Registration filters">
        {['all', 'upcoming', 'confirmed', 'cancelled'].map((f) => (
          <button
            key={f}
            role="tab"
            aria-selected={filter === f}
            onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors focus:ring-2 focus:ring-blue-500
              ${filter === f ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20"><Spinner size="lg" /></div>
      ) : data?.items?.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <p className="text-4xl mb-3" aria-hidden="true">🎟️</p>
          <p className="font-medium">No registrations yet</p>
          <Link to="/events" className="text-blue-600 hover:underline text-sm mt-1 block">Browse events</Link>
        </div>
      ) : (
        <div className="space-y-4">
          {data?.items?.map((reg) => (
            <div key={reg.id} className="bg-white border border-gray-200 rounded-xl p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <p className="font-semibold text-gray-900">{reg.event?.title}</p>
                  {reg.event?.start_at && (
                    <div className="flex items-center gap-1.5 text-sm text-gray-500 mt-1">
                      <Calendar size={13} aria-hidden="true" />
                      <time dateTime={reg.event.start_at}>{formatEventDateTime(reg.event.start_at)}</time>
                    </div>
                  )}
                  {reg.event?.venue_name && (
                    <div className="flex items-center gap-1.5 text-sm text-gray-500 mt-0.5">
                      <MapPin size={13} aria-hidden="true" />
                      <span>{reg.event.venue_name}</span>
                    </div>
                  )}
                  <div className="mt-2 flex flex-wrap items-center gap-3">
                    <Badge status={reg.status}>{reg.status.charAt(0).toUpperCase() + reg.status.slice(1)}</Badge>
                    <span className="text-sm text-gray-500">
                      {reg.quantity} × {reg.ticket_type?.name} · {formatPrice(reg.total_amount)}
                    </span>
                  </div>
                </div>
                <div className="flex flex-col gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setQrReg(reg)}
                    aria-label="Show QR code"
                  >
                    <QrCode size={16} aria-hidden="true" /> QR
                  </Button>
                  {reg.status === 'confirmed' && (
                    <Button
                      variant="secondary"
                      size="sm"
                      loading={cancel.isPending}
                      onClick={() => handleCancel(reg.id)}
                      aria-label="Cancel registration"
                    >
                      <X size={14} aria-hidden="true" /> Cancel
                    </Button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* QR modal */}
      <Modal isOpen={!!qrReg} onClose={() => setQrReg(null)} title="Your QR Code">
        {qrReg && <QRCodeDisplay qrToken={qrReg.qr_token} eventTitle={qrReg.event?.title} />}
      </Modal>
    </div>
  )
}

import { useState } from 'react'
import { Check, X, Ban, RefreshCw } from 'lucide-react'
import { useAdminEvents, useAdminUsers, useAdmin } from '../hooks/useAdmin'
import Badge from '../components/ui/Badge'
import Button from '../components/ui/Button'
import Modal from '../components/ui/Modal'
import Spinner from '../components/ui/Spinner'
import Input from '../components/ui/Input'
import { formatEventDateTime } from '../utils/formatDate'

export default function AdminPage() {
  const [tab, setTab] = useState('events')
  const [rejectModal, setRejectModal] = useState(null)
  const [rejectReason, setRejectReason] = useState('')
  const { data: eventsData, isLoading: eventsLoading } = useAdminEvents({ status: 'pending' })
  const { data: usersData, isLoading: usersLoading } = useAdminUsers()
  const { approveEvent, rejectEvent, suspendUser, reactivateUser } = useAdmin()

  const handleReject = async () => {
    await rejectEvent.mutateAsync({ id: rejectModal, reason: rejectReason })
    setRejectModal(null)
    setRejectReason('')
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Admin Panel</h1>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 border-b border-gray-200" role="tablist">
        {['events', 'users'].map((t) => (
          <button
            key={t}
            role="tab"
            aria-selected={tab === t}
            onClick={() => setTab(t)}
            className={`px-5 py-2.5 text-sm font-medium border-b-2 transition-colors focus:ring-2 focus:ring-blue-500 -mb-px
              ${tab === t ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'}`}
          >
            {t === 'events' ? 'Pending Events' : 'Users'}
          </button>
        ))}
      </div>

      {/* Events tab */}
      {tab === 'events' && (
        <div>
          {eventsLoading ? (
            <div className="flex justify-center py-10"><Spinner size="lg" /></div>
          ) : eventsData?.items?.length === 0 ? (
            <p className="text-center py-10 text-gray-500">No pending events. 🎉</p>
          ) : (
            <div className="space-y-3">
              {eventsData?.items?.map((event) => (
                <div key={event.id} className="bg-white border border-gray-200 rounded-xl p-5 flex items-center justify-between gap-4">
                  <div className="flex-1">
                    <p className="font-semibold text-gray-900">{event.title}</p>
                    <p className="text-sm text-gray-500 mt-0.5">
                      <time dateTime={event.start_at}>{formatEventDateTime(event.start_at)}</time>
                      {event.city && ` · ${event.city}`}
                    </p>
                    <Badge status="pending" className="mt-2">Pending Review</Badge>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      onClick={() => approveEvent.mutate(event.id)}
                      loading={approveEvent.isPending}
                      aria-label={`Approve event ${event.title}`}
                    >
                      <Check size={14} aria-hidden="true" /> Approve
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => setRejectModal(event.id)}
                      aria-label={`Reject event ${event.title}`}
                    >
                      <X size={14} aria-hidden="true" /> Reject
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Users tab */}
      {tab === 'users' && (
        <div>
          {usersLoading ? (
            <div className="flex justify-center py-10"><Spinner size="lg" /></div>
          ) : (
            <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
                  <tr>
                    <th className="px-4 py-3 text-left">Name</th>
                    <th className="px-4 py-3 text-left">Email</th>
                    <th className="px-4 py-3 text-left">Role</th>
                    <th className="px-4 py-3 text-left">Status</th>
                    <th className="px-4 py-3 text-left">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {usersData?.items?.map((user) => (
                    <tr key={user.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 font-medium text-gray-900">{user.first_name} {user.last_name}</td>
                      <td className="px-4 py-3 text-gray-500">{user.email}</td>
                      <td className="px-4 py-3">
                        <Badge status={user.role === 'admin' ? 'published' : 'free'}>{user.role}</Badge>
                      </td>
                      <td className="px-4 py-3">
                        <Badge status={user.is_active ? 'confirmed' : 'cancelled'}>
                          {user.is_active ? 'Active' : 'Suspended'}
                        </Badge>
                      </td>
                      <td className="px-4 py-3">
                        {user.is_active ? (
                          <Button variant="danger" size="sm" onClick={() => suspendUser.mutate(user.id)} loading={suspendUser.isPending} aria-label={`Suspend ${user.first_name}`}>
                            <Ban size={12} aria-hidden="true" /> Suspend
                          </Button>
                        ) : (
                          <Button variant="secondary" size="sm" onClick={() => reactivateUser.mutate(user.id)} loading={reactivateUser.isPending} aria-label={`Reactivate ${user.first_name}`}>
                            <RefreshCw size={12} aria-hidden="true" /> Reactivate
                          </Button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Reject modal */}
      <Modal isOpen={!!rejectModal} onClose={() => setRejectModal(null)} title="Reject Event">
        <div className="space-y-4">
          <Input id="reject_reason" label="Rejection reason (optional)" value={rejectReason} onChange={(e) => setRejectReason(e.target.value)} placeholder="Missing required details…" />
          <div className="flex justify-end gap-3">
            <Button variant="secondary" onClick={() => setRejectModal(null)}>Cancel</Button>
            <Button variant="danger" onClick={handleReject} loading={rejectEvent.isPending}>Confirm Reject</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}

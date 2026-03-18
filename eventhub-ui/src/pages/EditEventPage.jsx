import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useEvent, useUpdateEvent, useCreateTicket, useCategories } from '../hooks/useEvents'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import Alert from '../components/ui/Alert'
import Spinner from '../components/ui/Spinner'

export default function EditEventPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: event, isLoading } = useEvent(id)
  const { data: categories = [] } = useCategories()
  const updateEvent = useUpdateEvent(id)
  const createTicket = useCreateTicket(id)
  const [form, setForm] = useState(null)
  const [newTicket, setNewTicket] = useState({ name: '', price: 0, quantity_total: 50 })
  const [errors, setErrors] = useState({})
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    if (event) setForm({
      title: event.title,
      description: event.description,
      category_id: event.category_id || '',
      start_at: event.start_at?.slice(0, 16),
      end_at: event.end_at?.slice(0, 16),
      venue_name: event.venue_name || '',
      address: event.address || '',
      city: event.city || '',
      capacity: event.capacity,
      is_virtual: event.is_virtual,
      tags: event.tags?.join(', ') || '',
    })
  }, [event])

  const set = (k) => (e) => {
    const val = e.target.type === 'checkbox' ? e.target.checked : e.target.value
    setForm((f) => ({ ...f, [k]: val }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await updateEvent.mutateAsync({
        ...form,
        tags: form.tags ? form.tags.split(',').map(t => t.trim()).filter(Boolean) : [],
        category_id: form.category_id || null,
      })
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setErrors({ form: err.response?.data?.detail || 'Update failed' })
    }
  }

  const handleAddTicket = async () => {
    try {
      await createTicket.mutateAsync(newTicket)
      setNewTicket({ name: '', price: 0, quantity_total: 50 })
    } catch (err) {
      setErrors({ ticket: err.response?.data?.detail || 'Failed to add ticket' })
    }
  }

  if (isLoading || !form) return <div className="flex justify-center py-32"><Spinner size="lg" /></div>

  return (
    <div className="max-w-2xl mx-auto px-4 py-10">
      <div className="flex items-center gap-3 mb-6">
        <Link to="/my-events" className="text-gray-500 hover:text-gray-700 text-sm">← My Events</Link>
        <h1 className="text-2xl font-bold text-gray-900">Edit Event</h1>
      </div>

      {success && <Alert type="success" className="mb-4">Event updated!</Alert>}
      {errors.form && <Alert type="error" className="mb-4">{errors.form}</Alert>}

      <form onSubmit={handleSubmit} noValidate className="space-y-6">
        <div className="bg-white border border-gray-200 rounded-2xl p-6 space-y-4">
          <Input id="title" label="Title" value={form.title} onChange={set('title')} />
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea id="description" rows={4} value={form.description} onChange={set('description')}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label htmlFor="edit_category" className="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select id="edit_category" value={form.category_id} onChange={set('category_id')}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500">
              <option value="">None</option>
              {categories.map((c) => <option key={c.id} value={c.id}>{c.icon} {c.name}</option>)}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input id="edit_start" label="Start" type="datetime-local" value={form.start_at} onChange={set('start_at')} />
            <Input id="edit_end" label="End" type="datetime-local" value={form.end_at} onChange={set('end_at')} />
          </div>
          <label className="flex items-center gap-2 text-sm cursor-pointer">
            <input type="checkbox" checked={form.is_virtual} onChange={set('is_virtual')} className="rounded text-blue-600 focus:ring-blue-500" />
            Virtual event
          </label>
          {!form.is_virtual && (
            <>
              <Input id="edit_venue" label="Venue" value={form.venue_name} onChange={set('venue_name')} />
              <Input id="edit_address" label="Address" value={form.address} onChange={set('address')} />
              <Input id="edit_city" label="City" value={form.city} onChange={set('city')} />
            </>
          )}
          <Input id="edit_capacity" label="Capacity" type="number" value={form.capacity} onChange={set('capacity')} />
        </div>

        {/* Existing tickets */}
        {event.ticket_types?.length > 0 && (
          <div className="bg-white border border-gray-200 rounded-2xl p-6">
            <h2 className="font-semibold text-gray-900 mb-3">Ticket Types</h2>
            {event.ticket_types.map((t) => (
              <div key={t.id} className="flex items-center justify-between py-2 border-b last:border-0 text-sm">
                <span>{t.name}</span>
                <span className="text-gray-500">${t.price} · {t.quantity_available}/{t.quantity_total} left</span>
              </div>
            ))}
          </div>
        )}

        {/* Add ticket */}
        <div className="bg-white border border-gray-200 rounded-2xl p-6 space-y-3">
          <h2 className="font-semibold text-gray-900">Add Ticket Type</h2>
          {errors.ticket && <Alert type="error">{errors.ticket}</Alert>}
          <div className="grid grid-cols-3 gap-3">
            <Input id="new_ticket_name" label="Name" value={newTicket.name} onChange={(e) => setNewTicket(t => ({ ...t, name: e.target.value }))} />
            <Input id="new_ticket_price" label="Price" type="number" min={0} step="0.01" value={newTicket.price} onChange={(e) => setNewTicket(t => ({ ...t, price: e.target.value }))} />
            <Input id="new_ticket_qty" label="Quantity" type="number" min={1} value={newTicket.quantity_total} onChange={(e) => setNewTicket(t => ({ ...t, quantity_total: e.target.value }))} />
          </div>
          <Button type="button" variant="secondary" onClick={handleAddTicket} loading={createTicket.isPending}>Add Ticket</Button>
        </div>

        <div className="flex justify-end gap-3">
          <Link to="/my-events"><Button variant="secondary">Cancel</Button></Link>
          <Button type="submit" loading={updateEvent.isPending}>Save Changes</Button>
        </div>
      </form>
    </div>
  )
}

import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useCreateEvent, useCreateTicket, useCategories } from '../hooks/useEvents'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import Alert from '../components/ui/Alert'

export default function CreateEventPage() {
  const navigate = useNavigate()
  const { data: categories = [] } = useCategories()
  const createEvent = useCreateEvent()

  const [form, setForm] = useState({
    title: '', description: '', category_id: '',
    start_at: '', end_at: '', timezone: 'UTC',
    venue_name: '', address: '', city: '',
    capacity: 100, is_virtual: false,
    tags: '',
  })
  const [ticket, setTicket] = useState({ name: 'General Admission', price: 0, quantity_total: 100 })
  const [errors, setErrors] = useState({})
  const [step, setStep] = useState(1) // 1=details, 2=tickets
  const createTicketMutation = useCreateTicket(null) // will get event id after creation

  const set = (k) => (e) => {
    const val = e.target.type === 'checkbox' ? e.target.checked : e.target.value
    setForm((f) => ({ ...f, [k]: val }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const errs = {}
    if (!form.title) errs.title = 'Title required'
    if (!form.description) errs.description = 'Description required'
    if (!form.start_at) errs.start_at = 'Start date required'
    if (!form.end_at) errs.end_at = 'End date required'
    if (!ticket.name) errs.ticket_name = 'Ticket name required'
    if (ticket.quantity_total < 1) errs.ticket_qty = 'Quantity must be at least 1'
    setErrors(errs)
    if (Object.keys(errs).length) return

    try {
      const toISO = (s) => s ? new Date(s).toISOString() : s
      const payload = {
        ...form,
        start_at: toISO(form.start_at),
        end_at: toISO(form.end_at),
        tags: form.tags ? form.tags.split(',').map(t => t.trim()).filter(Boolean) : [],
        category_id: form.category_id || null,
        capacity: parseInt(form.capacity),
      }
      const event = await createEvent.mutateAsync(payload)

      // Create default ticket type
      await import('../api/client').then(({ default: api }) =>
        api.post(`/events/${event.id}/tickets`, {
          name: ticket.name,
          price: parseFloat(ticket.price),
          quantity_total: parseInt(ticket.quantity_total),
          is_active: true,
        })
      )

      navigate('/my-events')
    } catch (err) {
      setErrors({ form: err.response?.data?.detail || 'Failed to create event' })
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-10">
      <div className="flex items-center gap-3 mb-6">
        <Link to="/my-events" className="text-gray-500 hover:text-gray-700 text-sm">← My Events</Link>
        <h1 className="text-2xl font-bold text-gray-900">Create New Event</h1>
      </div>

      {errors.form && <Alert type="error" className="mb-4">{errors.form}</Alert>}

      <form onSubmit={handleSubmit} noValidate className="space-y-6">
        <div className="bg-white border border-gray-200 rounded-2xl p-6 space-y-4">
          <h2 className="font-semibold text-gray-900">Event Details</h2>
          <Input id="title" label="Event Title *" value={form.title} onChange={set('title')} error={errors.title} />
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">Description *</label>
            <textarea id="description" rows={4} value={form.description} onChange={set('description')}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
              aria-describedby={errors.description ? 'desc-error' : undefined}
            />
            {errors.description && <p id="desc-error" role="alert" className="text-xs text-red-600 mt-1">{errors.description}</p>}
          </div>
          <div>
            <label htmlFor="category_id" className="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select id="category_id" value={form.category_id} onChange={set('category_id')}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500">
              <option value="">None</option>
              {categories.map((c) => <option key={c.id} value={c.id}>{c.icon} {c.name}</option>)}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input id="start_at" label="Start Date & Time *" type="datetime-local" value={form.start_at} onChange={set('start_at')} error={errors.start_at} />
            <Input id="end_at" label="End Date & Time *" type="datetime-local" value={form.end_at} onChange={set('end_at')} error={errors.end_at} />
          </div>
          <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
            <input type="checkbox" checked={form.is_virtual} onChange={set('is_virtual')} className="rounded text-blue-600 focus:ring-blue-500" />
            Virtual event (online only)
          </label>
          {!form.is_virtual && (
            <>
              <Input id="venue_name" label="Venue Name" value={form.venue_name} onChange={set('venue_name')} />
              <Input id="address" label="Address" value={form.address} onChange={set('address')} placeholder="123 Main St, Austin TX" />
              <Input id="city" label="City" value={form.city} onChange={set('city')} />
            </>
          )}
          <div className="grid grid-cols-2 gap-4">
            <Input id="capacity" label="Capacity" type="number" min={1} value={form.capacity} onChange={set('capacity')} />
            <Input id="tags" label="Tags (comma-separated)" value={form.tags} onChange={set('tags')} placeholder="react, javascript" />
          </div>
        </div>

        {/* Ticket section */}
        <div className="bg-white border border-gray-200 rounded-2xl p-6 space-y-4">
          <h2 className="font-semibold text-gray-900">Default Ticket Type</h2>
          <p className="text-xs text-gray-500">You can add more ticket types after creating the event.</p>
          <div className="grid grid-cols-3 gap-4">
            <Input id="ticket_name" label="Name" value={ticket.name} onChange={(e) => setTicket(t => ({ ...t, name: e.target.value }))} error={errors.ticket_name} />
            <Input id="ticket_price" label="Price ($)" type="number" min={0} step="0.01" value={ticket.price} onChange={(e) => setTicket(t => ({ ...t, price: e.target.value }))} />
            <Input id="ticket_qty" label="Quantity" type="number" min={1} value={ticket.quantity_total} onChange={(e) => setTicket(t => ({ ...t, quantity_total: e.target.value }))} error={errors.ticket_qty} />
          </div>
        </div>

        <div className="flex justify-end gap-3">
          <Link to="/my-events"><Button variant="secondary">Cancel</Button></Link>
          <Button type="submit" loading={createEvent.isPending}>Create Event</Button>
        </div>
      </form>
    </div>
  )
}

import { useState } from 'react'
import { formatPrice } from '../../utils/formatDate'
import { luhn } from '../../utils/luhn'
import Button from '../ui/Button'
import Input from '../ui/Input'
import Alert from '../ui/Alert'
import { useRegistration } from '../../hooks/useRegistration'
import useAuthStore from '../../store/authStore'

export default function TicketSelector({ event, onSuccess }) {
  const { user } = useAuthStore()
  const { register } = useRegistration()

  const [selectedTicket, setSelectedTicket] = useState(null)
  const [quantity, setQuantity] = useState(1)
  const [payment, setPayment] = useState({ card_number: '', expiry_month: '', expiry_year: '', cvv: '' })
  const [errors, setErrors] = useState({})

  const tickets = event.ticket_types?.filter((t) => t.is_active && t.quantity_available > 0) || []

  const validate = () => {
    const errs = {}
    if (!selectedTicket) { errs.ticket = 'Please select a ticket type' }
    if (quantity < 1) { errs.quantity = 'Quantity must be at least 1' }
    if (selectedTicket && selectedTicket.price > 0) {
      const stripped = payment.card_number.replace(/\s/g, '')
      if (!luhn(stripped)) errs.card_number = 'Invalid card number'
      if (!payment.expiry_month) errs.expiry_month = 'Required'
      if (!payment.expiry_year) errs.expiry_year = 'Required'
      if (!payment.cvv) errs.cvv = 'Required'
    }
    setErrors(errs)
    return Object.keys(errs).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validate()) return

    const payload = {
      event_id: event.id,
      ticket_type_id: selectedTicket.id,
      quantity,
    }
    if (selectedTicket.price > 0) {
      payload.payment = {
        card_number: payment.card_number.replace(/\s/g, ''),
        expiry_month: parseInt(payment.expiry_month),
        expiry_year: parseInt(payment.expiry_year),
        cvv: payment.cvv,
      }
    }

    try {
      const result = await register.mutateAsync(payload)
      onSuccess?.(result)
    } catch (err) {
      setErrors({ form: err.response?.data?.detail || 'Registration failed. Please try again.' })
    }
  }

  if (!user) return (
    <Alert type="info">
      <a href="/login" className="font-medium underline">Log in</a> to register for this event.
    </Alert>
  )

  if (tickets.length === 0) return (
    <Alert type="warning">No tickets available at this time.</Alert>
  )

  return (
    <form onSubmit={handleSubmit} noValidate className="space-y-4">
      {errors.form && <Alert type="error">{errors.form}</Alert>}

      {/* Ticket type selection */}
      <fieldset>
        <legend className="text-sm font-medium text-gray-700 mb-2">Select Ticket Type</legend>
        <div className="space-y-2">
          {tickets.map((ticket) => (
            <label
              key={ticket.id}
              className={`flex items-center justify-between p-3 border rounded-lg cursor-pointer hover:border-blue-400 transition-colors ${selectedTicket?.id === ticket.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}`}
            >
              <div className="flex items-center gap-3">
                <input
                  type="radio"
                  name="ticket_type"
                  value={ticket.id}
                  checked={selectedTicket?.id === ticket.id}
                  onChange={() => { setSelectedTicket(ticket); setErrors({}) }}
                  className="text-blue-600 focus:ring-blue-500"
                />
                <div>
                  <p className="font-medium text-gray-900 text-sm">{ticket.name}</p>
                  <p className="text-xs text-gray-500">{ticket.quantity_available} left</p>
                </div>
              </div>
              <span className="font-semibold text-gray-900">{formatPrice(ticket.price)}</span>
            </label>
          ))}
        </div>
        {errors.ticket && <p role="alert" className="text-xs text-red-600 mt-1">{errors.ticket}</p>}
      </fieldset>

      {/* Quantity */}
      <Input
        label="Quantity"
        id="quantity"
        type="number"
        min={1}
        max={selectedTicket?.quantity_available || 10}
        value={quantity}
        onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
        error={errors.quantity}
      />

      {/* Payment — only shown for paid tickets */}
      {selectedTicket && selectedTicket.price > 0 && (
        <div className="space-y-3 border border-gray-200 rounded-lg p-4">
          <p className="text-sm font-medium text-gray-700">Payment Details <span className="text-xs font-normal text-gray-400">(Mock — not processed)</span></p>
          <Input
            label="Card Number"
            id="card_number"
            type="text"
            inputMode="numeric"
            placeholder="4242 4242 4242 4242"
            value={payment.card_number}
            onChange={(e) => setPayment({ ...payment, card_number: e.target.value })}
            error={errors.card_number}
          />
          <div className="grid grid-cols-3 gap-3">
            <Input
              label="Exp. Month"
              id="expiry_month"
              type="number"
              placeholder="12"
              min={1} max={12}
              value={payment.expiry_month}
              onChange={(e) => setPayment({ ...payment, expiry_month: e.target.value })}
              error={errors.expiry_month}
            />
            <Input
              label="Exp. Year"
              id="expiry_year"
              type="number"
              placeholder="2028"
              value={payment.expiry_year}
              onChange={(e) => setPayment({ ...payment, expiry_year: e.target.value })}
              error={errors.expiry_year}
            />
            <Input
              label="CVV"
              id="cvv"
              type="text"
              placeholder="123"
              maxLength={4}
              value={payment.cvv}
              onChange={(e) => setPayment({ ...payment, cvv: e.target.value })}
              error={errors.cvv}
            />
          </div>
        </div>
      )}

      {/* Total + Submit */}
      {selectedTicket && (
        <div className="flex items-center justify-between pt-2">
          <div>
            <p className="text-sm text-gray-500">Total</p>
            <p className="text-xl font-bold text-gray-900">
              {formatPrice(selectedTicket.price * quantity)}
            </p>
          </div>
          <Button type="submit" loading={register.isPending} size="lg">
            {selectedTicket.price > 0 ? 'Complete Purchase' : 'Register Free'}
          </Button>
        </div>
      )}
    </form>
  )
}

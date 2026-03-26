/**
 * Leaflet map component — only renders when lat/lng are present and event is not virtual.
 * Uses OpenStreetMap tiles (no API key required).
 */
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'

// Fix default marker icon path issue with Vite/webpack bundlers
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

export default function EventMap({ event }) {
  // Don't render for virtual events or events without coordinates
  if (event.is_virtual || !event.latitude || !event.longitude) return null

  const lat = parseFloat(event.latitude)
  const lng = parseFloat(event.longitude)

  return (
    <div>
      <h3 className="text-lg font-semibold text-gray-900 mb-3">Venue Location</h3>
      <MapContainer
        center={[lat, lng]}
        zoom={14}
        style={{ height: '300px', borderRadius: '12px' }}
        aria-label={`Map showing location of ${event.venue_name || 'event venue'}`}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        <Marker position={[lat, lng]}>
          <Popup>
            <strong>{event.venue_name}</strong>
            <br />
            {event.address}
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  )
}

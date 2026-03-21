import { QRCodeSVG } from 'qrcode.react'

export default function QRCodeDisplay({ qrToken, eventTitle }) {
  return (
    <div className="flex flex-col items-center gap-3 p-6 bg-white border border-gray-200 rounded-xl">
      <QRCodeSVG
        value={qrToken}
        size={180}
        bgColor="#ffffff"
        fgColor="#1e293b"
        aria-label={`QR code for ${eventTitle || 'your registration'}`}
      />
      <p className="text-xs text-gray-500 font-mono break-all text-center max-w-xs">{qrToken}</p>
      <p className="text-xs text-gray-400">Show this at the event for check-in</p>
    </div>
  )
}

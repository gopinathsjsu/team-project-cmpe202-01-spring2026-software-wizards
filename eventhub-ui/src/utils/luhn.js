/**
 * Luhn algorithm — validates card numbers on the frontend before submitting.
 * Same logic is also validated on the backend in registration_service.py.
 */
export function luhn(n) {
  let sum = 0
  let alt = false
  for (let i = n.length - 1; i >= 0; i--) {
    let d = parseInt(n[i], 10)
    if (alt) {
      d *= 2
      if (d > 9) d -= 9
    }
    sum += d
    alt = !alt
  }
  return sum % 10 === 0
}

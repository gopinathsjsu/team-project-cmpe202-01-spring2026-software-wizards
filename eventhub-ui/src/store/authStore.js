/**
 * Zustand auth store — persists token to localStorage.
 * Singleton-like: single store instance shared across the app.
 */
import { create } from 'zustand'

const useAuthStore = create((set) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  token: localStorage.getItem('access_token') || null,

  login: (user, accessToken, refreshToken) => {
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
    localStorage.setItem('user', JSON.stringify(user))
    set({ user, token: accessToken })
  },

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    set({ user: null, token: null })
  },

  updateUser: (updates) =>
    set((state) => {
      const updated = { ...state.user, ...updates }
      localStorage.setItem('user', JSON.stringify(updated))
      return { user: updated }
    }),
}))

export default useAuthStore

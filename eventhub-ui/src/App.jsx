import { Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'
import useAuthStore from './store/authStore'

// Pages (lazy-loaded for performance)
import { lazy, Suspense } from 'react'
import Spinner from './components/ui/Spinner'

const HomePage = lazy(() => import('./pages/HomePage'))
const EventsPage = lazy(() => import('./pages/EventsPage'))
const EventDetailPage = lazy(() => import('./pages/EventDetailPage'))
const LoginPage = lazy(() => import('./pages/LoginPage'))
const RegisterPage = lazy(() => import('./pages/RegisterPage'))
const MyEventsPage = lazy(() => import('./pages/MyEventsPage'))
const DashboardPage = lazy(() => import('./pages/DashboardPage'))
const CreateEventPage = lazy(() => import('./pages/CreateEventPage'))
const EditEventPage = lazy(() => import('./pages/EditEventPage'))
const AdminPage = lazy(() => import('./pages/AdminPage'))
const ProfilePage = lazy(() => import('./pages/ProfilePage'))
const MyRegistrationsPage = lazy(() => import('./pages/MyRegistrationsPage'))
const ResetPasswordPage = lazy(() => import('./pages/ResetPasswordPage'))
const NotFoundPage = lazy(() => import('./pages/NotFoundPage'))

function RequireAuth({ children, roles }) {
  const { user } = useAuthStore()
  if (!user) return <Navigate to="/login" replace />
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />
  return children
}

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />
      <main className="flex-1">
        <Suspense fallback={<div className="flex justify-center py-20"><Spinner size="lg" /></div>}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/events" element={<EventsPage />} />
            <Route path="/events/:id" element={<EventDetailPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/reset-password" element={<ResetPasswordPage />} />

            <Route path="/profile" element={
              <RequireAuth><ProfilePage /></RequireAuth>
            } />
            <Route path="/my-events" element={
              <RequireAuth roles={['organizer', 'admin']}><MyEventsPage /></RequireAuth>
            } />
            <Route path="/my-registrations" element={
              <RequireAuth><MyRegistrationsPage /></RequireAuth>
            } />
            <Route path="/dashboard" element={
              <RequireAuth roles={['organizer', 'admin']}><DashboardPage /></RequireAuth>
            } />
            <Route path="/dashboard/events/new" element={
              <RequireAuth roles={['organizer', 'admin']}><CreateEventPage /></RequireAuth>
            } />
            <Route path="/dashboard/events/:id/edit" element={
              <RequireAuth roles={['organizer', 'admin']}><EditEventPage /></RequireAuth>
            } />
            <Route path="/admin" element={
              <RequireAuth roles={['admin']}><AdminPage /></RequireAuth>
            } />

            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Suspense>
      </main>
      <Footer />
    </div>
  )
}
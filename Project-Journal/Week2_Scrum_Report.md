# Week 2 Scrum Report (Sprint 1)

## Weekly Scrum Report
### Team Members: Atharva Mokashi, Maitreya Patankar, Shefali Saini, Shubham Baid
### Week: Feb 23–Mar 1, 2026

---

## 1. What tasks did I work on / complete?

### Atharva Mokashi
- Implemented `app/services/auth_service.py` (JWT generation/verification, bcrypt password hashing)
- Added `app/dependencies.py` for FastAPI DI — `get_current_user` and `get_current_active_user`
- Built `app/routers/auth.py` with `/register` and `/login` endpoints
- Registered all routers in `app/main.py`

### Maitreya Patankar
- Added `app/models/event.py` and `app/models/category.py`
- Added `app/schemas/event.py`, `app/schemas/category.py`, `app/schemas/common.py` (pagination schema)

### Shefali Saini
- Added `api/client.js` (Axios with JWT interceptor) and `authStore.js` (Zustand)
- Built `App.jsx` with protected route logic, `Navbar.jsx`, `Footer.jsx`
- Added `LoginPage.jsx` and `RegisterPage.jsx`

### Shubham Baid
- Added `app/models/registration.py` and `app/models/ticket_type.py`
- Added `app/schemas/registration.py` and `app/schemas/ticket.py`
- Completed Alembic initial migration `001_initial_schema.py`

---

## 2. What am I planning to work on next?

### Atharva Mokashi
- Add `app/crud/user_crud.py` (Repository pattern) and `/users` profile endpoints

### Maitreya Patankar
- Implement event CRUD repository and `event_service.py` with Observer + Strategy patterns

### Shefali Saini
- Add `useAuth` custom hook, `EventsPage`, and reusable UI components

### Shubham Baid
- Implement registration CRUD, registration service, and registrations/tickets routers

---

## 3. What tasks are blocked waiting on another team member?

### Atharva Mokashi
- No blockers.

### Maitreya Patankar
- No blockers.

### Shefali Saini
- No blockers.

### Shubham Baid
- No blockers.

---

## XP Core Values Followed This Week

### **Communication**
Atharva shared the JWT token format and Authorization header pattern with Shefali before she built `client.js`, avoiding a mis-wiring that would have caused 401 errors during integration. Backend and frontend stayed aligned on the auth contract throughout the week.

### **Feedback**
Shefali tested the auth pages against the real `/auth` endpoints as soon as they were deployed, catching integration issues immediately rather than discovering them later during full-stack testing.

---

## Collaboration Notes
All four tracks progressed in parallel this week with no cross-team blockers. Atharva and Shefali had the tightest dependency — auth backend and frontend pages — and coordinated directly. The Alembic migration being complete locks in the full database schema for the rest of Sprint 1.

# Week 3 Scrum Report (Sprint 1)

## Weekly Scrum Report
### Team Members: Atharva Mokashi, Maitreya Patankar, Shefali Saini, Shubham Baid
### Week: Mar 2–8, 2026

---

## 1. What tasks did I work on / complete?

### Atharva Mokashi
- Added `app/crud/base_crud.py` — generic Repository base class with `get`, `get_multi`, `create`, `update`, `delete`
- Added `app/crud/user_crud.py` extending `BaseCRUD`
- Built `app/routers/users.py` (GET/PATCH profile, change password)

### Maitreya Patankar
- Added `app/crud/event_crud.py` (Repository pattern with complex filter queries) and `app/crud/category_crud.py`
- Implemented `app/services/event_service.py` with `EventStatusSubject` (Observer) and `EventSortStrategy` (Strategy)
- Added `app/routers/events.py` and `app/routers/categories.py`

### Shefali Saini
- Added `useAuth.js` custom hook
- Built reusable UI components: `Button.jsx`, `Input.jsx`, `Badge.jsx`, `Modal.jsx`, `Spinner.jsx`, `Alert.jsx`

### Shubham Baid
- Implemented `app/crud/registration_crud.py` and `app/crud/ticket_crud.py`
- Added `app/services/registration_service.py` (capacity management, ticket inventory)
- Added `app/routers/registrations.py` and `app/routers/tickets.py`

---

## 2. What am I planning to work on next?

### Atharva Mokashi
- Add password reset token flow

### Maitreya Patankar
- Implement `notification_service.py` using Factory pattern for notification channels

### Shefali Saini
- Build `EventCard`, `EventsPage`, `SearchBar`, `FilterPanel`

### Shubham Baid
- Add email service and admin router

---

## 3. What tasks are blocked waiting on another team member?

### Atharva Mokashi
- No blockers.

### Maitreya Patankar
- No blockers.

### Shefali Saini
- Waiting for events API to be stable before wiring data into pages. Coordinated with Maitreya — events router merged Mar 7.

### Shubham Baid
- No blockers.

---

## XP Core Values Followed This Week

### **Simplicity**
`BaseCRUD` eliminates CRUD boilerplate across all repositories — each entity-specific class only overrides what is genuinely different. `EventSortStrategy` uses callable strategies as parameters rather than a deep class hierarchy; adding a new sort order is a one-line addition.

### **Feedback**
Shefali held off building `EventsPage` against a mock and waited one day for Maitreya's events router to merge. Wiring against the real API once avoided having to rewire a mock-based page later.

---

## Collaboration Notes
Sprint 1 wraps this week with the full CRUD and service layer complete. Shubham was able to pull in `BaseCRUD` on Monday morning and move fast. The events router merging on Mar 7 unblocks Shefali for Sprint 2 feature work starting next week.

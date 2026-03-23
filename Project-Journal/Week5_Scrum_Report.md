# Week 5 Scrum Report (Sprint 2)

## Weekly Scrum Report
### Team Members: Atharva Mokashi, Maitreya Patankar, Shefali Saini, Shubham Baid
### Week: Mar 16–22, 2026

---

## 1. What tasks did I work on / complete?

### Atharva Mokashi
- Added password reset token generation in auth service
- Built `ResetPasswordPage.jsx` on the frontend in coordination with Shefali
- Reviewed `registration_service.py` for correctness

### Maitreya Patankar
- Completed `app/services/s3_service.py` (presigned URL upload flow)
- Completed `app/services/calendar_service.py` (Google Calendar + iCal link generation)
- Integrated both services into the events router

### Shefali Saini
- Added `CreateEventPage.jsx` and `EditEventPage.jsx` (with image upload via S3 presigned URL)
- Added `DashboardPage.jsx`, `MyEventsPage.jsx`, `MyRegistrationsPage.jsx`
- Added `QRCodeDisplay.jsx`, `useRegistration.js`, `ProfilePage.jsx`
- Added `index.css` with Tailwind base styles

### Shubham Baid
- Added `AdminPage.jsx` and `useAdmin.js` with user management and event approval UI
- Added `NotFoundPage.jsx` and 404 routing in `App.jsx`

---

## 2. What am I planning to work on next?

### Atharva Mokashi
- Begin writing unit tests for auth service

### Maitreya Patankar
- Write unit tests for event service patterns. Optimize queries with eager loading.

### Shefali Saini
- Add `EventMap.jsx`, utility functions, and finish accessibility pass

### Shubham Baid
- Set up `pytest.ini`, `tests/conftest.py`, and write integration tests for registration flow

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
Password reset required Atharva and Shefali to agree on the token-in-URL flow before either side was built. The direct coordination meant the backend and frontend were implemented consistently without a mismatch.

### **Simplicity**
`calendar_service.py` and `s3_service.py` are narrow services with a single responsibility each. No shared state, no cross-service dependencies — each can be tested and replaced independently.

---

## Collaboration Notes
Week 5 was the highest-output week of the sprint. Shefali delivered eight pages and a custom hook; Maitreya completed both remaining backend services. The Google Calendar story deferred from Sprint 2 is now done. Sprint 2 feature work is essentially complete — test coverage starts next week.

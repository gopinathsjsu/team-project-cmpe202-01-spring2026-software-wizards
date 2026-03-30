# Week 6 Scrum Report (Sprint 2)

## Weekly Scrum Report
### Team Members: Atharva Mokashi, Maitreya Patankar, Shefali Saini, Shubham Baid
### Week: Mar 23–29, 2026

---

## 1. What tasks did I work on / complete?

### Atharva Mokashi
- Added `tests/test_auth.py` covering register, login, JWT validation, and protected route access
- Set up `pytest.ini` config

### Maitreya Patankar
- Finalized `s3_service.py` and `calendar_service.py` integration
- Added `tests/test_events.py` for event CRUD and sort strategies

### Shefali Saini
- Added `EventMap.jsx` (Leaflet integration)
- Added `utils/formatDate.js`, `utils/buildCalendarLink.js`, `utils/luhn.js` (ticket number validation)
- Added global `index.css`. Fixed responsive layout issues on mobile breakpoints.

### Shubham Baid
- Added `tests/conftest.py` (async test client, in-memory SQLite DB fixture)
- Added `tests/test_registrations.py` and `tests/test_admin.py`
- Added `scripts/seed.py` and `scripts/reset_db.py`

---

## 2. What am I planning to work on next?

### Atharva Mokashi
- Fix edge cases found in testing: duplicate email returning 500, expired token not clearing on frontend

### Maitreya Patankar
- Fix event capacity race condition identified during testing

### Shefali Saini
- Final accessibility pass — ARIA labels, keyboard navigation

### Shubham Baid
- Add GitHub Actions CI/CD workflow. Add health check endpoint.

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

### **Feedback**
Writing `test_auth.py` immediately surfaced the duplicate email edge case (returning 500 instead of 422) and the expired token handling gap. Testing surfaced these issues at exactly the right time — before the bug-fix sprint, not after shipping.

### **Respect**
Shubham documented the SQLite test fixture as an explicit trade-off (fast, but doesn't exercise migration paths) rather than leaving it as an undocumented limitation. Honest documentation keeps future contributors from being misled.

---

## Collaboration Notes
Sprint 2 closes with all four test modules in place. The bugs found during testing give Sprint 3 a clear, scoped defect list rather than vague "there might be issues." The seed and reset scripts from Shubham immediately improved the local development experience for the whole team.

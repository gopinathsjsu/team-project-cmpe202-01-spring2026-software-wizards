# Week 4 Scrum Report (Sprint 2)

## Weekly Scrum Report
### Team Members: Atharva Mokashi, Maitreya Patankar, Shefali Saini, Shubham Baid
### Week: Mar 9–15, 2026

---

## 1. What tasks did I work on / complete?

### Atharva Mokashi
- Led team sync on API contract — aligned request/response schemas with Shefali's frontend expectations
- Reviewed Maitreya's Observer pattern implementation in `event_service.py`

### Maitreya Patankar
- Implemented `notification_service.py` (Factory pattern — `EmailNotifier`, `InAppNotifier` based on channel type)
- Wired Observer into event service so status changes dispatch notifications
- Began `app/services/s3_service.py` for image uploads *(partially complete due to AWS credentials blocker)*

### Shefali Saini
- Added `EventCard.jsx`, `EventsPage.jsx` (search + filter), `SearchBar.jsx`, `FilterPanel.jsx`
- Added `EventDetailPage.jsx` with ticket purchase flow and `TicketSelector.jsx`
- Added `useEvents.js` custom hook

### Shubham Baid
- Added `app/services/email_service.py` (SMTP with template rendering)
- Added `app/routers/admin.py` (user ban/unban, event approval, stats endpoints)

---

## 2. What am I planning to work on next?

### Atharva Mokashi
- Add password reset endpoint and coordinate with Shefali on `ResetPasswordPage.jsx`

### Maitreya Patankar
- Complete `s3_service.py` and build `calendar_service.py`

### Shefali Saini
- Add `CreateEventPage`, `EditEventPage`, `DashboardPage`, `MyEventsPage`

### Shubham Baid
- Build `AdminPage` and `useAdmin` hook. Set up test infrastructure.

---

## 3. What tasks are blocked waiting on another team member?

### Atharva Mokashi
- No blockers.

### Maitreya Patankar
- **Blocked:** AWS credentials needed to develop and test `s3_service.py`. *(Resolved mid-week — Atharva shared credentials)*

### Shefali Saini
- No blockers.

### Shubham Baid
- No blockers.

---

## XP Core Values Followed This Week

### **Communication**
The API contract sync on Monday caught field name mismatches between backend schemas and Shefali's frontend expectations before any integration code was written. The AWS credentials blocker was raised the same day it was hit, and resolved mid-week rather than sitting until the next standup.

### **Courage**
The team chose to implement the Factory + Observer combination for notifications despite the added complexity. The decision paid off — adding `InAppNotifier` required no changes to `event_service.py`, only a new branch in the Factory.

---

# Sprint 2 Report & Planned Backlog

## Sprint Objective
Build the core product features: full event CRUD with organizer workflows, attendee registration with tickets, search and filter, S3 image uploads, admin panel, email notifications, and complete frontend pages for all major user flows.

---

## Planned Sprint 2 Backlog (User Story Format)

| Story ID | User Story | Status |
|----------|------------|--------|
| **S2-01** | As an organizer, I can create, edit, and delete events. | ✅ Completed |
| **S2-02** | As an attendee, I can register for an event and receive a ticket. | ✅ Completed |
| **S2-03** | As a user, I can search and filter events by category, date, and location. | ✅ Completed |
| **S2-04** | As an organizer, I can upload an event banner image via S3 presigned URL. | ✅ Completed |
| **S2-05** | As an admin, I can approve/reject events and ban users. | ✅ Completed |
| **S2-06** | As an attendee, I can view a QR code ticket for my registration. | ✅ Completed |
| **S2-07** | As a user, I can reset my password via email link. | ✅ Completed |
| **S2-08** | As a user, I receive email notifications on registration. | ⚠️ Partial — backend complete, frontend notification display deferred |
| **S2-09** | As a user, I can add an event to Google Calendar. | → Deferred to Sprint 3 (AWS blocker pushed calendar work out of Sprint 2) |

---

## Sprint Summary
Sprint 2 delivered the core product features. Seven of nine stories fully completed. Google Calendar integration was deferred due to the AWS credentials blocker eating into Maitreya's week. Email notification backend is done; frontend display was not completed within the sprint. Both items carry into Sprint 3.

# Week 7 Scrum Report (Sprint 3)

## Weekly Scrum Report
### Team Members: Atharva Mokashi, Maitreya Patankar, Shefali Saini, Shubham Baid
### Week: Mar 30–Apr 5, 2026

---

## 1. What tasks did I work on / complete?

### Atharva Mokashi
- Fixed JWT token expiry — Zustand store was not clearing on 401 responses
- Fixed duplicate email validation returning 500 instead of 422
- Added rate limiting middleware to auth endpoints

### Maitreya Patankar
- Fixed event capacity race condition — added `SELECT FOR UPDATE` in registration service
- Updated Observer to correctly unsubscribe when an event is cancelled
- Added API docstrings for OpenAPI auto-generation

### Shefali Saini
- Added ARIA labels on all interactive elements, focus rings, keyboard-navigable modal
- Fixed React Query cache invalidation bug after event creation

### Shubham Baid
- Added `.github/workflows/ci.yml` (GitHub Actions: lint + test on push)
- Added `/health` endpoint to the API
- Verified Docker Compose works end-to-end on a clean checkout

---

## 2. What am I planning to work on next?

### Atharva Mokashi
- Final security audit: CORS configuration review, input sanitization

### Maitreya Patankar
- Database query optimization with eager loading for event list endpoint

### Shefali Saini
- Final UI polish — loading skeletons, error boundaries

### Shubham Baid
- Performance testing, deployment documentation

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
The CI pipeline went live this week and immediately provided automated feedback on every push. Bug fixes from testing (JWT expiry, duplicate email, race condition, cache invalidation) were all caught by the test suite before merging — exactly the feedback loop the tests were written for.

### **Communication**
The race condition fix in `registration_service.py` touched code Shubham had written tests for. Maitreya flagged the change to Shubham so `test_registrations.py` could be updated alongside the fix rather than being left broken.

---

# Sprint 3 Report & Planned Backlog

## Sprint Objective
Fix all bugs identified from Sprint 2 testing, establish CI/CD, close deferred stories (calendar, password reset), and harden the app with security and performance work.

---

## Planned Sprint 3 Backlog (User Story Format)

| Story ID | User Story | Status |
|----------|------------|--------|
| **S3-01** | As a developer, auth flows have passing automated tests so regressions are caught automatically. | ✅ Completed |
| **S3-02** | As a developer, event CRUD and sort strategy logic has passing tests. | ✅ Completed |
| **S3-03** | As a developer, CI/CD runs lint and tests on every push so `main` stays green. | ✅ Completed |
| **S3-04** | As a user, the app works correctly on mobile viewports. | ✅ Completed |
| **S3-05** | As a user, I can reset my password via email link. *(carried from Sprint 2)* | ✅ Completed |
| **S3-06** | As a user, I can add an event to Google Calendar. *(carried from Sprint 2)* | ✅ Completed |
| **S3-07** | As a developer, event list queries are optimized with eager loading and a DB index. | ✅ Completed |
| **S3-08** | As a developer, the app passes a security audit (CORS, CSP, input sanitization, auth gaps). | ✅ Completed |

---

## Sprint Summary
Sprint 3 closed all open defects and delivered all 8 stories including the 2 carried from Sprint 2. The race condition fix and CI pipeline were the most impactful items this sprint. The team goes into Sprint 4 with a green test suite and a hardened API.

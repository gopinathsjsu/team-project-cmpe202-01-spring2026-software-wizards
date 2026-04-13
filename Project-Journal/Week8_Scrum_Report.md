# Week 8 Scrum Report (Sprint 3)

## Weekly Scrum Report
### Team Members: Atharva Mokashi, Maitreya Patankar, Shefali Saini, Shubham Baid
### Week: Apr 6–12, 2026

---

## 1. What tasks did I work on / complete?

### Atharva Mokashi
- Completed security audit — tightened CORS origins, added `Content-Security-Policy` header, sanitized event description input
- Reviewed all endpoints for authorization gaps and fixed missing ownership check on event update

### Maitreya Patankar
- Optimized event list query — added `selectinload` for categories and ticket types, reducing N+1 queries
- Added Alembic index migration for `event.start_datetime`
- Completed OpenAPI descriptions for all event endpoints

### Shefali Saini
- Added loading skeleton components
- Added React error boundary around page routes
- Improved form error messages. Minor Tailwind spacing/typography polish pass.

### Shubham Baid
- Ran k6 load test against events endpoint — identified timeout on unindexed query (resolved by Maitreya's migration)
- Verified all 4 test files pass in CI
- Documented deployment steps in README

---

## 2. What am I planning to work on next?

### Atharva Mokashi
- Final README updates. Record demo video walkthrough.

### Maitreya Patankar
- Final review of design pattern documentation for submission.

### Shefali Saini
- Final cross-browser testing. Update project journal frontend section.

### Shubham Baid
- Deployment preparation — finalize Docker images, confirm environment variables.

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

### **Courage**
Atharva's security audit found a CORS wildcard (`allow_origins=["*"]`) that had been in `main.py` since day one. Rather than leaving it for after submission, the team fixed it immediately along with the missing authorization check on event update.

### **Simplicity**
The query optimization was two lines of `selectinload` — no architecture change needed. The security fixes were targeted: one middleware addition, one `bleach.clean()` call, one ownership guard. Nothing was over-engineered.

---

## Collaboration Notes
Shubham's load test and Maitreya's optimization were tightly coordinated this week — the test without the fix produced the baseline numbers, and the fix without re-running the test would have given no measurable evidence of improvement. Running them in sequence gave the team a concrete before/after.

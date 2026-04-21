# Week 9 Scrum Report (Sprint 4)

## Weekly Scrum Report
### Team Members: Atharva Mokashi, Maitreya Patankar, Shefali Saini, Shubham Baid
### Week: Apr 13–20, 2026

---

## 1. What tasks did I work on / complete?

### Atharva Mokashi
- Final README updates
- Recorded demo video walkthrough of auth and user management flows
- Updated project journal

### Maitreya Patankar
- Final merge of `develop` into `main`
- Verified all design patterns are documented in README
- Updated project journal with sprint 4 entry

### Shefali Saini
- Final cross-browser test (Chrome, Firefox, Safari)
- Verified mobile layout on 375px viewport
- Final `index.css` pass

### Shubham Baid
- Deployment verification on Docker Compose
- Added final environment variable documentation (`.env.example`)
- Verified CI passes on `main`. Updated project journal.

---

## 2. What am I planning to work on next?

### All team members
- Final submission review and upload.

---

## 3. What tasks are blocked waiting on another team member?

### All team members
- No blockers.

---

## XP Core Values Followed This Week

### **Respect**
Documentation was treated with the same care as code. Maitreya reviewed Atharva's design pattern writeups for accuracy before the final merge. No one rushed through Sprint 4 just because the engineering was done.

### **Communication**
Cross-browser testing by Shefali surfaced a minor CSS issue that needed Atharva's input on the CSP header. Raised immediately on Discord and resolved the same day without delaying the submission timeline.

---

# Sprint 4 Report & Planned Backlog

## Sprint Objective
Finalize documentation, verify deployment, record demo, and deliver a clean merge to `main` with a green CI build.

---

## Planned Sprint 4 Backlog (User Story Format)

| Story ID | User Story | Status |
|----------|------------|--------|
| **S4-01** | As a developer, the project runs end-to-end via `docker compose up` on a clean machine with only a `.env` file. | ✅ Completed |
| **S4-02** | As a team, the Project Journal is complete — weekly entries, XP Core Values, Scrum Backlog, Burndown Charts. | ✅ Completed |
| **S4-03** | As a reviewer, all 8 design patterns are documented in the README with code references. | ✅ Completed |
| **S4-04** | As a reviewer, the API is self-documented via OpenAPI with descriptions for all endpoints. | ✅ Completed |
| **S4-05** | As a team, a demo video walkthrough is recorded and accessible for evaluation. | ✅ Completed |

---

## Sprint Summary
Sprint 4 completed in 5 working days with all 5 stories done. The `develop → main` merge passed CI with all 35 tests green. The project is documented, deployable, and submission-ready.

---

## Overall Project Retrospective

### What went well
- Component ownership kept merge conflicts minimal throughout the project
- API contract sync at Sprint 2 kickoff prevented integration rework
- CI/CD pipeline caught a broken import on its first day live
- Performance testing before shipping caught the N+1 query issue that would have been invisible in manual testing

### What could be improved
- AWS credentials should have been shared before Sprint 2 started — the 2-day blocker in Week 4 was avoidable
- Email notification scope was underestimated — "backend done" was not the same as "story done"
- The known registration race condition was identified in Week 3 but not fixed until Week 7 — should have been a Sprint 2 story

### Key learnings
- Short feedback loops (API contract, code review, CI, daily standups) caught the largest class of integration issues early
- `SELECT FOR UPDATE` is sufficient for ticket inventory concurrency at this scale — no distributed locking needed
- Zustand + React Query was the right call over Redux — the auth store has been 40 lines since Week 2

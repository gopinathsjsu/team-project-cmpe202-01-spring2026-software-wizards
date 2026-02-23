# Week 1 Scrum Report (Sprint 1)

## Weekly Scrum Report
### Team Members: Atharva Mokashi, Maitreya Patankar, Shefali Saini, Shubham Baid
### Week: Feb 16–22, 2026

---

## 1. What tasks did I work on / complete?

### Atharva Mokashi
- Initialized GitHub repository, added README and `.gitignore`
- Set up FastAPI project skeleton with `requirements.txt`
- Implemented `app/database.py` (async SQLAlchemy + `lru_cache` Singleton) and `app/config.py` (Pydantic settings)
- Added `app/models/base.py` with `TimestampMixin`, `User` model, and user schemas (DTO pattern)

### Maitreya Patankar
- Reviewed project requirements and PRD
- Contributed to initial `app/main.py` structure
- Started drafting `Event` and `Category` models

### Shefali Saini
- Initialized React + Vite project, configured Tailwind CSS and PostCSS
- Decided on page-based routing with React Router v6
- Set up folder structure: `pages/`, `components/`, `hooks/`, `store/`, `api/`, `utils/`

### Shubham Baid
- Set up `docker-compose.yml` with PostgreSQL, API, and UI services
- Added `Dockerfile` for the API
- Drafted `Registration` and `TicketType` model schemas

---

## 2. What am I planning to work on next?

### Atharva Mokashi
- Implement JWT auth service, `app/dependencies.py`, and `/auth` router

### Maitreya Patankar
- Finalize `app/models/event.py`, `app/models/category.py`, and corresponding schemas

### Shefali Saini
- Set up Axios API client, Zustand auth store, `App.jsx` routing, Navbar, Footer

### Shubham Baid
- Finalize registration/ticket models once Event model is merged

---

## 3. What tasks are blocked waiting on another team member?

### Atharva Mokashi
- No blockers.

### Maitreya Patankar
- Waiting on `base.py` from Atharva to finalize models. *(Resolved Feb 20)*

### Shefali Saini
- No blockers.

### Shubham Baid
- Waiting on `app/models/event.py` from Maitreya to finalize registration model relationships. *(Expected Feb 24)*

---

## XP Core Values Followed This Week

### **Communication**
Team held a kickoff meeting to divide component ownership clearly — Atharva (auth/backend), Maitreya (events), Shefali (frontend), Shubham (registrations/infra). Maitreya's base.py dependency was surfaced early and resolved within the same week instead of stalling.

### **Simplicity**
Repository structure was kept minimal from day one. The Singleton pattern for the DB session used Python's built-in `@lru_cache` rather than a custom class — simplest correct approach.

---

# Sprint 1 Report & Planned Backlog

## Sprint Objective
Set up the project foundation: repository, Docker environment, data models, JWT authentication, CRUD repository layer, and a working React frontend with routing and auth pages.

---

## Planned Sprint 1 Backlog (User Story Format)

| Story ID | User Story | Status |
|----------|------------|--------|
| **S1-01** | As a developer, I want a GitHub repo with README and `.gitignore` so collaboration is set up correctly. | ✅ Completed |
| **S1-02** | As a developer, I want a Dockerized environment so all team members run the full stack consistently. | ✅ Completed |
| **S1-03** | As a developer, I want `database.py` and `config.py` with Singleton pattern so the backend has a reliable data connection. | ✅ Completed |
| **S1-04** | As a developer, I want core models (`User`, `Event`, `Registration`, `TicketType`) with an Alembic migration so data persists in PostgreSQL. | ✅ Completed |
| **S1-05** | As a user, I can register and log in with JWT auth so my session is secure. | ✅ Completed |
| **S1-06** | As a developer, I want a generic `BaseCRUD` repository so data access is consistent across all entities. | ✅ Completed |
| **S1-07** | As a user, I can open the frontend app and navigate to Login and Register pages. | ✅ Completed |

---

## Sprint Summary
Sprint 1 delivered the full project foundation on schedule. All 7 stories completed. The team split work along component ownership lines and resolved inter-member dependencies quickly. Codebase is ready for Sprint 2 feature development.

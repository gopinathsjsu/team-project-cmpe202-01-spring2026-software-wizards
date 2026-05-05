[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/xRTHk3Dv)

# EventHub

## Project Overview

EventHub is a full-stack event management and ticketing platform inspired by Eventbrite. It enables organizers to create, manage, and publish events while allowing attendees to discover events, purchase tickets, and receive automated reminders. The platform supports an admin approval workflow, real-time seat tracking, QR-code-based check-in, and calendar integrations.

## Team Information

- **Course**: CMPE 202
- **University**: San Jose State University
- **Team Name**: Software Wizards
- **Team Members**:

  | Name | SJSU ID |
  |------|---------|
  | Atharva Prasanna Mokashi | 019117046 |
  | Maitreya Patankar | 019146166 |
  | Shefali Saini | 018281848 |
  | Shubham Baid | 018221333 |

## Tech Stack

### Frontend
- **React 18** — UI framework
- **Vite** — build tool and dev server
- **React Router v6** — client-side routing
- **Axios** — HTTP client for API calls
- **TailwindCSS** — utility-first CSS framework
- **Zustand** — lightweight global state management
- **TanStack Query (React Query)** — server-state caching and data fetching
- **Leaflet / React-Leaflet** — interactive event location maps
- **qrcode.react** — QR code generation for tickets
- **lucide-react** — icon library
- **date-fns** — date formatting utilities

### Backend
- **Python 3.12** — runtime
- **FastAPI** — async web framework
- **SQLAlchemy 2 (async)** — ORM with async PostgreSQL support
- **PostgreSQL 15** — relational database
- **Alembic** — database migrations
- **Pydantic v2** — request/response validation and settings management
- **python-jose** — JWT authentication tokens
- **passlib / bcrypt** — password hashing
- **APScheduler** — background scheduler for 48-hour event reminders
- **icalendar** — iCal (.ics) calendar export
- **AWS S3 (boto3)** — image storage
- **SMTP** — transactional email

### Design Patterns
- **Singleton** — `Settings` instantiated once via `@lru_cache` in `config.py`
- **Observer** — `EventSubject` notifies `AttendeeNotificationObserver` and `OrganizerNotificationObserver` on event status changes
- **Dependency Injection** — all route handlers receive dependencies via FastAPI's `Depends()`

### Deployment
- **Docker Compose** — orchestrates PostgreSQL, API, and UI services locally
- **AWS EC2** — hosts the production API and frontend
- **AWS S3** — stores event banner images

## Project Structure

```
team-project-cmpe202-01-spring2026-software-wizards/
├── eventhub-api/                  # FastAPI backend
│   ├── app/
│   │   ├── config.py              # Singleton settings (pydantic-settings + lru_cache)
│   │   ├── database.py            # Async SQLAlchemy engine and session factory
│   │   ├── dependencies.py        # Reusable FastAPI Depends() — auth, role guards
│   │   ├── main.py                # App factory; registers routers, middleware, scheduler
│   │   ├── models/                # SQLAlchemy ORM models
│   │   │   ├── user.py            # User (attendee / organizer / admin)
│   │   │   ├── event.py           # Event with TSVECTOR full-text search column
│   │   │   ├── category.py        # Event categories
│   │   │   ├── ticket_type.py     # Ticket tiers per event (free / paid)
│   │   │   └── registration.py    # Registration + QR token + check-in timestamp
│   │   ├── schemas/               # Pydantic request/response schemas
│   │   ├── crud/                  # Database access layer (async CRUD helpers)
│   │   ├── routers/               # Route definitions
│   │   │   ├── auth.py            # Register, login, refresh, password reset
│   │   │   ├── users.py           # User profile
│   │   │   ├── events.py          # Event CRUD, search, calendar export, CSV export
│   │   │   ├── categories.py      # Category management
│   │   │   ├── tickets.py         # Ticket type management
│   │   │   ├── registrations.py   # Register for event, cancel, QR check-in
│   │   │   └── admin.py           # Admin — approve/reject events, manage users
│   │   └── services/
│   │       ├── event_service.py   # Observer pattern, geocoding, reminder logic
│   │       ├── email_service.py   # Transactional email helpers
│   │       ├── notification_service.py
│   │       ├── registration_service.py
│   │       ├── calendar_service.py  # iCal, Google Calendar, Outlook links
│   │       ├── auth_service.py
│   │       └── s3_service.py      # AWS S3 upload/delete
│   ├── alembic/                   # Database migration scripts
│   ├── scripts/
│   │   ├── seed.py                # Populate DB with sample data
│   │   └── reset_db.py            # Drop and recreate all tables
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_events.py
│   │   ├── test_registrations.py
│   │   └── test_admin.py
│   ├── Dockerfile
│   ├── entrypoint.sh              # Runs Alembic migrations then starts Uvicorn
│   ├── requirements.txt
│   └── alembic.ini
│
├── eventhub-ui/                   # React + Vite frontend
│   ├── src/
│   │   ├── api/                   # Axios instance and per-resource API modules
│   │   ├── components/
│   │   │   ├── events/            # EventCard, EventFilters, EventStatusBadge, etc.
│   │   │   ├── layout/            # Navbar, Footer, PageWrapper
│   │   │   ├── map/               # Leaflet map component for event location
│   │   │   ├── tickets/           # TicketSelector, TicketSummary
│   │   │   └── ui/                # Shared primitives (Button, Modal, Spinner, etc.)
│   │   ├── hooks/                 # Custom React hooks (useAuth, useEvents, etc.)
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── EventsPage.jsx
│   │   │   ├── EventDetailPage.jsx
│   │   │   ├── CreateEventPage.jsx
│   │   │   ├── EditEventPage.jsx
│   │   │   ├── MyEventsPage.jsx
│   │   │   ├── EventAttendeesPage.jsx
│   │   │   ├── MyRegistrationsPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── AdminPage.jsx
│   │   │   ├── ProfilePage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   ├── ResetPasswordPage.jsx
│   │   │   └── NotFoundPage.jsx
│   │   ├── store/                 # Zustand stores (auth, UI state)
│   │   ├── utils/                 # Date helpers, formatters
│   │   ├── App.jsx                # Route definitions
│   │   └── main.jsx               # Entry point
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── Project-Journal/               # Scrum reports and burndown charts (Weeks 1–9)
├── docker-compose.yml             # Local dev orchestration (db, api, ui)
└── README.md
```

## Features

### Core Functionality

1. **User Authentication & Roles**
   - Register and login with JWT-based auth (access + refresh tokens)
   - Three roles: **Attendee**, **Organizer**, **Admin**
   - Password reset via emailed token

2. **Event Lifecycle (Organizer)**
   - Create events with title, description, venue/location, banner image, capacity, and tags
   - Define multiple ticket tiers per event (free or paid) with quantity limits and sale deadlines
   - Submit event for admin approval; track status (Draft → Pending → Published / Rejected)
   - Edit or cancel published events; export attendee list as CSV

3. **Event Discovery (Attendee)**
   - Browse and search all published events
   - Full-text search powered by PostgreSQL TSVECTOR + GIN index
   - Filter by category, city, date range, virtual/in-person, free/paid
   - Sort by date, popularity, or recency
   - Interactive Leaflet map showing event location

4. **Ticketing & Registration**
   - Select ticket tier and quantity; register in one step
   - Unique QR token generated per registration
   - Organizer scans QR code to check in attendees on the day
   - Cancel registration (releases seats back to inventory)

5. **Automated Notifications**
   - Email confirmation on registration
   - APScheduler sends 48-hour reminder emails every 5 minutes (checks upcoming events)
   - Observer pattern notifies attendees and organizers on event status changes

6. **Calendar Integration**
   - Export event to iCal (.ics) file
   - One-click "Add to Google Calendar" and "Add to Outlook" links

7. **Admin Dashboard**
   - Review and approve or reject submitted events (with rejection reason)
   - Manage users (view, deactivate)
   - View platform-wide statistics

### Event Details
- Title, description, status (draft / pending / published / cancelled / rejected)
- Start and end datetime with timezone
- Venue name, address, city, latitude/longitude
- Capacity, virtual flag, banner image, tags
- Multiple ticket types: name, price, total quantity, quantity sold, sale deadline

## User Roles & Permissions

### Attendee
- Register and login
- Browse and search published events
- Register for events and manage own registrations
- Download iCal / calendar links

### Organizer
- All attendee permissions
- Create, edit, and delete own events
- Manage ticket types per event
- View attendee list and check in attendees via QR
- Export attendee list to CSV

### Admin
- All organizer permissions
- Approve or reject pending events (with reason)
- View and manage all users and all events
- Access admin dashboard with platform statistics

## Database Schema

### Tables
1. **users** — id, email, password_hash, first_name, last_name, role (attendee/organizer/admin), bio, avatar_url, is_active
2. **events** — id, organizer_id, category_id, title, description, status, start_at, end_at, timezone, venue_name, address, city, latitude, longitude, capacity, is_virtual, banner_url, tags, search_vector, rejection_reason
3. **categories** — id, name, description
4. **ticket_types** — id, event_id, name, price, quantity_total, quantity_sold, is_active, sale_ends_at
5. **registrations** — id, attendee_id, event_id, ticket_type_id, status, quantity, total_amount, payment_ref, qr_token, checked_in_at, reminder_sent
6. **password_reset_tokens** — id, user_id, token, expires_at, used

## API Endpoints

All endpoints are prefixed with `/api/v1`.

### Authentication
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/register` | Register new user |
| `POST` | `/auth/login` | Login, receive access + refresh tokens |
| `POST` | `/auth/refresh` | Refresh access token |
| `POST` | `/auth/forgot-password` | Send password reset email |
| `POST` | `/auth/reset-password` | Reset password with token |

### Users
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/users/me` | Get current user profile |
| `PUT` | `/users/me` | Update profile |

### Events
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/events` | List/search published events (paginated, filterable) |
| `GET` | `/events/mine` | List organizer's own events |
| `POST` | `/events` | Create event (organizer) |
| `GET` | `/events/{id}` | Get event detail |
| `PUT` | `/events/{id}` | Update event |
| `DELETE` | `/events/{id}` | Delete event |
| `POST` | `/events/{id}/submit` | Submit event for admin approval |
| `GET` | `/events/{id}/attendees` | List attendees (organizer) |
| `GET` | `/events/{id}/attendees/csv` | Export attendees as CSV |
| `GET` | `/events/{id}/calendar/ics` | Download iCal file |
| `GET` | `/events/{id}/calendar/google` | Google Calendar link |
| `GET` | `/events/{id}/calendar/outlook` | Outlook calendar link |

### Categories
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/categories` | List all categories |
| `POST` | `/categories` | Create category (admin) |
| `PUT` | `/categories/{id}` | Update category (admin) |
| `DELETE` | `/categories/{id}` | Delete category (admin) |

### Ticket Types
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/tickets/event/{event_id}` | List ticket types for an event |
| `POST` | `/tickets/event/{event_id}` | Create ticket type (organizer) |
| `PUT` | `/tickets/{id}` | Update ticket type |
| `DELETE` | `/tickets/{id}` | Delete ticket type |

### Registrations
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/registrations/mine` | List current user's registrations |
| `POST` | `/registrations` | Register for an event |
| `DELETE` | `/registrations/{id}` | Cancel registration |
| `POST` | `/registrations/{id}/checkin` | Check in attendee via QR token |

### Admin
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/admin/events/pending` | List events awaiting approval |
| `POST` | `/admin/events/{id}/approve` | Approve event |
| `POST` | `/admin/events/{id}/reject` | Reject event with reason |
| `GET` | `/admin/users` | List all users |
| `PUT` | `/admin/users/{id}` | Update user (e.g., deactivate) |
| `GET` | `/admin/stats` | Platform statistics |

### Health
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness check |

Interactive API docs are available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc`.

## Setup Instructions

### Prerequisites
- Docker & Docker Compose (recommended)
- **Or** locally: Python 3.12+, Node.js 20+, PostgreSQL 15

### Quick Start with Docker (recommended)

```bash
# Clone the repository
git clone <repository-url>
cd team-project-cmpe202-01-spring2026-software-wizards

# Copy and configure backend environment variables
cp eventhub-api/.env.example eventhub-api/.env
# Edit eventhub-api/.env with your SMTP credentials and any other overrides

# Start all services (PostgreSQL, API, UI)
docker compose up --build

# In a separate terminal, seed the database with sample data (optional)
docker compose exec api python scripts/seed.py
```

Services will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Manual Backend Setup

```bash
cd eventhub-api

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — set DATABASE_URL, SECRET_KEY, SMTP credentials, etc.

# Run database migrations
alembic upgrade head

# (Optional) Seed sample data
python scripts/seed.py

# Start the development server
uvicorn app.main:app --reload --port 8000
```

### Manual Frontend Setup

```bash
cd eventhub-ui

# Install dependencies
npm install

# Configure environment
# Create .env with: VITE_API_URL=http://localhost:8000

# Start the development server
npm run dev
```

### Running Tests

```bash
cd eventhub-api

# Run all tests with coverage
pytest --cov=app tests/

# Run a specific test file
pytest tests/test_events.py -v
```

## Environment Variables

### Backend (`eventhub-api/.env`)
| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (`postgresql+asyncpg://...`) |
| `SECRET_KEY` | Random 256-bit secret for JWT signing |
| `ALGORITHM` | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL (default: `30`) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL (default: `7`) |
| `SMTP_HOST` | SMTP server host |
| `SMTP_PORT` | SMTP server port |
| `SMTP_USER` | SMTP username |
| `SMTP_PASSWORD` | SMTP password |
| `SMTP_FROM` | Sender email address |
| `FRONTEND_URL` | Frontend base URL (used in reset-password links) |
| `AWS_ACCESS_KEY_ID` | AWS credentials for S3 |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials for S3 |
| `AWS_REGION` | AWS region (default: `us-east-1`) |
| `S3_BUCKET` | S3 bucket name for event images |
| `ENVIRONMENT` | `development` or `production` |

### Frontend (`eventhub-ui/.env`)
| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend API base URL |

## Deployment Architecture

The application is deployed on AWS with the following infrastructure:

- **AWS EC2** — runs the containerized FastAPI API and serves the built React frontend
- **AWS Load Balancer** — distributes incoming traffic across EC2 instances
- **AWS Auto Scaling** — scales EC2 instances up and down based on demand
- **AWS S3** — stores event banner images; served via pre-signed URLs
- **PostgreSQL** — hosted on AWS RDS

## Project Journal

Weekly scrum reports and sprint burndown charts are in the `Project-Journal/` directory (Weeks 1–9).

## License

This is an academic project for CMPE 202 at San Jose State University.

## Support

For questions or issues, please contact any team member or open an issue in the GitHub repository.

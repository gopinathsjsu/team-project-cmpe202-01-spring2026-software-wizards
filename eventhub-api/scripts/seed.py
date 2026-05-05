"""
Seed script — populates the database with realistic mock data using Faker.
Run: python scripts/seed.py

Demo credentials
  Admin:       admin@eventhub.dev        / Admin1234!
  Organizers:  organizer1@eventhub.dev   / Passw0rd!
               organizer2@eventhub.dev   / Passw0rd!
               organizer3@eventhub.dev   / Passw0rd!
               organizer4@eventhub.dev   / Passw0rd!
               organizer5@eventhub.dev   / Passw0rd!
  Attendees:   attendee01@eventhub.dev   / Passw0rd!
               attendee02@eventhub.dev   / Passw0rd!
               ...
               attendee20@eventhub.dev   / Passw0rd!
"""
import asyncio
import random
from datetime import datetime, timedelta, timezone

from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

CITIES = [
    {"name": "Austin", "state": "TX", "lat": 30.2672, "lng": -97.7431},
    {"name": "New York", "state": "NY", "lat": 40.7128, "lng": -74.0060},
    {"name": "San Francisco", "state": "CA", "lat": 37.7749, "lng": -122.4194},
    {"name": "Chicago", "state": "IL", "lat": 41.8781, "lng": -87.6298},
    {"name": "Seattle", "state": "WA", "lat": 47.6062, "lng": -122.3321},
    {"name": "Boston", "state": "MA", "lat": 42.3601, "lng": -71.0589},
    {"name": "Los Angeles", "state": "CA", "lat": 34.0522, "lng": -118.2437},
    {"name": "Denver", "state": "CO", "lat": 39.7392, "lng": -104.9903},
]

CATEGORIES = [
    {"name": "Technology", "slug": "technology", "icon": "💻"},
    {"name": "Music", "slug": "music", "icon": "🎵"},
    {"name": "Sports", "slug": "sports", "icon": "⚽"},
    {"name": "Arts & Culture", "slug": "arts-culture", "icon": "🎨"},
    {"name": "Food & Drink", "slug": "food-drink", "icon": "🍕"},
    {"name": "Business", "slug": "business", "icon": "💼"},
    {"name": "Health & Wellness", "slug": "health-wellness", "icon": "🏃"},
    {"name": "Education", "slug": "education", "icon": "📚"},
]

ORGANIZER_NAMES = [
    ("Alice", "Chen"),
    ("Brian", "Patel"),
    ("Carol", "Nguyen"),
    ("David", "Kim"),
    ("Elena", "Rodriguez"),
]

ATTENDEE_NAMES = [
    ("James", "Wilson"),
    ("Sophia", "Martinez"),
    ("Liam", "Thompson"),
    ("Emma", "Johnson"),
    ("Noah", "Brown"),
    ("Olivia", "Davis"),
    ("William", "Garcia"),
    ("Ava", "Miller"),
    ("Benjamin", "Taylor"),
    ("Isabella", "Anderson"),
    ("Mason", "Thomas"),
    ("Mia", "Jackson"),
    ("Ethan", "White"),
    ("Charlotte", "Harris"),
    ("Alexander", "Martin"),
    ("Amelia", "Lee"),
    ("Henry", "Clark"),
    ("Harper", "Lewis"),
    ("Sebastian", "Robinson"),
    ("Evelyn", "Walker"),
]

EVENT_TITLES = [
    "AI & Machine Learning Summit 2025",
    "React Conf: Building Tomorrow's Web",
    "Startup Pitch Night — Silicon Valley",
    "Jazz Under the Stars",
    "Bay Area 5K Fun Run",
    "Contemporary Art Exhibition Opening",
    "Farm-to-Table Dinner Experience",
    "Women in Tech Leadership Forum",
    "Yoga & Mindfulness Retreat",
    "Python for Data Science Workshop",
    "Hip-Hop & Street Dance Showcase",
    "Entrepreneurship Bootcamp",
    "Food Truck Festival",
    "Cloud Architecture Deep Dive",
    "Indie Film Screening & Q&A",
    "CrossFit Open Championship",
    "Vegan Cooking Masterclass",
    "Cybersecurity Threats & Defense",
    "Photography Walk: Urban Landscapes",
    "Product Management Workshop",
    "Electronic Music Night",
    "Marathon Training Kick-Off",
    "Craft Beer & Cheese Pairing",
    "Kubernetes & DevOps Conf",
    "Comedy Night: Open Mic",
    "Mental Health & Wellness Seminar",
    "GraphQL Workshop for Engineers",
    "Salsa & Latin Dance Social",
    "Green Energy Innovation Expo",
    "Book Club: Science Fiction",
    "UX Design Thinking Sprint",
    "Basketball 3v3 Tournament",
    "Street Food Safari",
    "Blockchain & Web3 Summit",
    "Acoustic Live Sessions",
    "Half Marathon — City Classic",
    "Pottery & Ceramics Studio Day",
    "Sales & Growth Hacking Masterclass",
    "Sunrise Meditation & Brunch",
    "React Native Mobile Hackathon",
]


async def seed():
    import sys
    sys.path.insert(0, ".")

    from app.database import AsyncSessionLocal
    from app.models.user import User
    from app.models.category import Category
    from app.models.event import Event
    from app.models.ticket_type import TicketType
    from app.models.registration import Registration
    from app.services.auth_service import auth_service
    import secrets

    async with AsyncSessionLocal() as db:
        print("Seeding categories...")
        cats = []
        for c in CATEGORIES:
            cat = Category(**c, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
            db.add(cat)
            cats.append(cat)
        await db.commit()
        for c in cats:
            await db.refresh(c)

        print("Seeding users...")
        admin = User(
            email="admin@eventhub.dev",
            password_hash=auth_service.hash_password("Admin1234!"),
            first_name="Admin",
            last_name="User",
            role="admin",
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(admin)

        organizers = []
        for i, (first, last) in enumerate(ORGANIZER_NAMES, start=1):
            org = User(
                email=f"organizer{i}@eventhub.dev",
                password_hash=auth_service.hash_password("Passw0rd!"),
                first_name=first,
                last_name=last,
                role="organizer",
                bio=fake.text(max_nb_chars=200),
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(org)
            organizers.append(org)

        attendees = []
        for i, (first, last) in enumerate(ATTENDEE_NAMES, start=1):
            att = User(
                email=f"attendee{i:02d}@eventhub.dev",
                password_hash=auth_service.hash_password("Passw0rd!"),
                first_name=first,
                last_name=last,
                role="attendee",
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(att)
            attendees.append(att)

        await db.commit()
        for u in organizers + attendees:
            await db.refresh(u)

        print("Seeding events and tickets...")
        events = []
        now = datetime.now(timezone.utc)

        for i, title in enumerate(EVENT_TITLES):
            city = random.choice(CITIES)
            cat = random.choice(cats)
            org = organizers[i % len(organizers)]

            # Mix of past, present-ish, and future events
            if i < 8:
                # Past events (already happened)
                start = now - timedelta(days=random.randint(10, 60))
            elif i < 12:
                # Pending approval events (for demo)
                start = now + timedelta(days=random.randint(5, 30))
            else:
                # Future events
                start = now + timedelta(days=random.randint(1, 120))

            end = start + timedelta(hours=random.randint(2, 8))

            # Status: a few pending for admin review, rest published
            if 8 <= i < 12:
                status = "pending"
            elif i < 8:
                status = "published"
            else:
                status = "published"

            event = Event(
                organizer_id=org.id,
                category_id=cat.id,
                title=title,
                description=fake.paragraph(nb_sentences=6),
                status=status,
                start_at=start,
                end_at=end,
                timezone="America/New_York",
                venue_name=fake.company() + " Center",
                address=fake.street_address(),
                city=city["name"],
                latitude=city["lat"] + random.uniform(-0.05, 0.05),
                longitude=city["lng"] + random.uniform(-0.05, 0.05),
                capacity=random.choice([50, 100, 250, 500, 1000]),
                is_virtual=(i % 7 == 0),
                tags=random.sample(["networking", "workshop", "conference", "hackathon", "meetup", "panel", "outdoor", "online"], k=2),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(event)
            events.append(event)

        await db.commit()
        for e in events:
            await db.refresh(e)

        # Add ticket types
        ticket_types_by_event = {}
        for event in events:
            tts = []

            free_tt = TicketType(
                event_id=event.id,
                name="General Admission",
                price=0.00,
                quantity_total=event.capacity,
                quantity_sold=0,
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(free_tt)
            tts.append(free_tt)

            if random.random() > 0.5:
                vip_tt = TicketType(
                    event_id=event.id,
                    name="VIP",
                    price=round(random.uniform(25, 200), 2),
                    quantity_total=min(50, event.capacity // 5),
                    quantity_sold=0,
                    is_active=True,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                db.add(vip_tt)
                tts.append(vip_tt)

            ticket_types_by_event[event.id] = tts

        await db.commit()
        for tts in ticket_types_by_event.values():
            for tt in tts:
                await db.refresh(tt)

        # Only register attendees for published events
        published_events = [e for e in events if e.status == "published"]

        print("Seeding registrations (all 20 attendees)...")
        registered_pairs = set()
        for attendee in attendees:
            num_events = random.randint(3, 8)
            sample_events = random.sample(published_events, min(num_events, len(published_events)))
            for event in sample_events:
                pair = (attendee.id, event.id)
                if pair in registered_pairs:
                    continue
                registered_pairs.add(pair)

                tts = ticket_types_by_event[event.id]
                tt = random.choice(tts)
                qty = 1
                if tt.quantity_sold + qty <= tt.quantity_total:
                    reg = Registration(
                        attendee_id=attendee.id,
                        event_id=event.id,
                        ticket_type_id=tt.id,
                        status="confirmed",
                        quantity=qty,
                        total_amount=float(tt.price) * qty,
                        payment_ref=f"MOCK-{secrets.token_hex(4).upper()}" if tt.price > 0 else None,
                        qr_token=secrets.token_urlsafe(32),
                        created_at=datetime.now(timezone.utc),
                        updated_at=datetime.now(timezone.utc),
                    )
                    db.add(reg)
                    tt.quantity_sold += qty
                    db.add(tt)

        await db.commit()

        pending_count = sum(1 for e in events if e.status == "pending")
        published_count = sum(1 for e in events if e.status == "published")

        print("\n✓ Seed complete!")
        print(f"\n{'─'*50}")
        print("  DEMO CREDENTIALS")
        print(f"{'─'*50}")
        print(f"  Admin:      admin@eventhub.dev        / Admin1234!")
        print(f"{'─'*50}")
        for i in range(1, 6):
            first, last = ORGANIZER_NAMES[i - 1]
            print(f"  Organizer{i}: organizer{i}@eventhub.dev    / Passw0rd!  ({first} {last})")
        print(f"{'─'*50}")
        for i in range(1, 21):
            first, last = ATTENDEE_NAMES[i - 1]
            print(f"  Attendee{i:02d}: attendee{i:02d}@eventhub.dev   / Passw0rd!  ({first} {last})")
        print(f"{'─'*50}")
        print(f"\n  Events: {len(events)} total ({published_count} published, {pending_count} pending review)")
        print(f"  Registrations: {len(registered_pairs)} total across all 20 attendees")


if __name__ == "__main__":
    asyncio.run(seed())

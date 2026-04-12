"""
Seed script — populates the database with realistic mock data using Faker.
Run: python scripts/seed.py
"""
import asyncio
import random
from datetime import datetime, timedelta, timezone

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

fake = Faker()

CITIES = [
    {"name": "Austin", "state": "TX", "lat": 30.2672, "lng": -97.7431},
    {"name": "New York", "state": "NY", "lat": 40.7128, "lng": -74.0060},
    {"name": "San Francisco", "state": "CA", "lat": 37.7749, "lng": -122.4194},
    {"name": "Chicago", "state": "IL", "lat": 41.8781, "lng": -87.6298},
    {"name": "Seattle", "state": "WA", "lat": 47.6062, "lng": -122.3321},
    {"name": "Boston", "state": "MA", "lat": 42.3601, "lng": -71.0589},
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
        for _ in range(5):
            profile = fake.profile()
            name_parts = profile["name"].split(" ", 1)
            org = User(
                email=fake.unique.email(),
                password_hash=auth_service.hash_password("Passw0rd!"),
                first_name=name_parts[0],
                last_name=name_parts[1] if len(name_parts) > 1 else "Organizer",
                role="organizer",
                bio=fake.text(max_nb_chars=200),
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(org)
            organizers.append(org)

        attendees = []
        for _ in range(20):
            profile = fake.profile()
            name_parts = profile["name"].split(" ", 1)
            att = User(
                email=fake.unique.email(),
                password_hash=auth_service.hash_password("Passw0rd!"),
                first_name=name_parts[0],
                last_name=name_parts[1] if len(name_parts) > 1 else "Attendee",
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
        for i in range(30):
            city = random.choice(CITIES)
            cat = random.choice(cats)
            org = random.choice(organizers)
            start = now + timedelta(days=random.randint(1, 90))
            end = start + timedelta(hours=random.randint(2, 8))

            event = Event(
                organizer_id=org.id,
                category_id=cat.id,
                title=fake.catch_phrase(),
                description=fake.paragraph(nb_sentences=5),
                status="published",
                start_at=start,
                end_at=end,
                timezone="America/New_York",
                venue_name=fake.company() + " Center",
                address=fake.street_address(),
                city=city["name"],
                latitude=city["lat"] + random.uniform(-0.05, 0.05),
                longitude=city["lng"] + random.uniform(-0.05, 0.05),
                capacity=random.choice([50, 100, 250, 500, 1000]),
                is_virtual=random.random() < 0.2,
                tags=random.sample(["networking", "workshop", "conference", "hackathon", "meetup", "panel"], k=2),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(event)
            events.append(event)

        await db.commit()
        for e in events:
            await db.refresh(e)

        # Add ticket types
        ticket_types = []
        for event in events:
            # Free ticket
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
            ticket_types.append((event, free_tt))

            if random.random() > 0.5:
                # Paid VIP ticket
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
                ticket_types.append((event, vip_tt))

        await db.commit()
        for _, tt in ticket_types:
            await db.refresh(tt)

        print("Seeding registrations...")
        for attendee in attendees[:10]:
            for event, tt in random.sample(ticket_types, min(5, len(ticket_types))):
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
        print("✓ Seed complete!")
        print(f"  Admin: admin@eventhub.dev / Admin1234!")
        print(f"  Organizers: {len(organizers)} (password: Passw0rd!)")
        print(f"  Attendees: {len(attendees)} (password: Passw0rd!)")
        print(f"  Events: {len(events)}")


if __name__ == "__main__":
    asyncio.run(seed())

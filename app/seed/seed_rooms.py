from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.room import Room


def seed_rooms():
    db = SessionLocal()
    rooms = [
        Room(
            name="Ocean View Deluxe",
            max_guests=2,
            base_price=120.0,
            description="Beautiful room with ocean view",
            beds=1,
            bathrooms=1,
            is_active=True
        ),
        Room(
            name="Garden Suite",
            max_guests=3,
            base_price=150.0,
            description="Quiet suite with garden access",
            beds=2,
            bathrooms=1,
            is_active=True
        ),
        Room(
            name="Budget Room",
            max_guests=2,
            base_price=60.0,
            description="Simple and affordable room",
            beds=1,
            bathrooms=1,
            is_active=True
        ),
        Room(
            name="Family Room",
            max_guests=4,
            base_price=180.0,
            description="Spacious room for families",
            beds=2,
            bathrooms=2,
            is_active=True
        ),
        Room(
            name="Penthouse Suite",
            max_guests=2,
            base_price=300.0,
            description="Luxury penthouse with city view",
            beds=1,
            bathrooms=2,
            is_active=True
        ),
        Room(
            name="Beach Bungalow",
            max_guests=3,
            base_price=200.0,
            description="Bungalow right on the beach",
            beds=2,
            bathrooms=1,
            is_active=True
        ),
        Room(
            name="Mountain Cabin",
            max_guests=4,
            base_price=140.0,
            description="Cozy cabin in the mountains",
            beds=3,
            bathrooms=1,
            is_active=True
        ),
        Room(
            name="City Studio",
            max_guests=2,
            base_price=90.0,
            description="Modern studio in city center",
            beds=1,
            bathrooms=1,
            is_active=True
        ),
        Room(
            name="Honeymoon Suite",
            max_guests=2,
            base_price=250.0,
            description="Romantic suite for couples",
            beds=1,
            bathrooms=1,
            is_active=True
        ),
    ]

    db.add_all(rooms)
    db.commit()
    print("Seeded 9 rooms successfully")


if __name__ == "__main__":
    seed_rooms()
    print("Seed completed")


# python -m app.seed.seed_rooms
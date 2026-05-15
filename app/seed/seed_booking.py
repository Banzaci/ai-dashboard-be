from datetime import date

from app.db.session import SessionLocal

# IMPORTANT:
# dessa imports måste finnas annars skapas inte tables i SQLAlchemy metadata
from app.models.booking import Booking
from app.models.room import Room


def seed_booking():

    db = SessionLocal()

    try:

        # ---------------------------------
        # DEBUG: check schema loaded
        # ---------------------------------
        print("Seeding booking...")

        # optional sanity check
        print("Booking model OK:", Booking)
        print("Room model OK:", Room)

        # ---------------------------------
        # CREATE BOOKING
        # ---------------------------------
        booking = Booking(
            room_id="f873a94d-ecaf-4978-9e4a-ff148a39d8d6",
            start_date=date(2026, 9, 20),
            end_date=date(2026, 9, 25),
            guests=2,
            status="confirmed"
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        print("✅ Seed booking created:", booking.id)

    except Exception as e:
        db.rollback()

        print("❌ Seed failed:")
        print(str(e))

        print("\n🔎 DEBUG HELP:")
        print("- Check if 'rooms' table exists in DB")
        print("- Check if Room model is imported before Base.metadata.create_all")
        print("- Check if you're using correct database URL")

    finally:
        db.close()


if __name__ == "__main__":
    seed_booking()
# python -m app.seed.seed_booking
# f873a94d-ecaf-4978-9e4a-ff148a39d8d6
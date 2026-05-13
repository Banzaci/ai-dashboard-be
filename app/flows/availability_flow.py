from sqlalchemy.orm import Session
from app.models.room import Room  # (eller din egen model)
from datetime import datetime
from app.models.booking import Booking

def availability_flow(db, date: str, guests: int):

    if not guests:
        guests = 1

    # 1. baseline rooms
    rooms = db.query(Room).filter(
        Room.is_active == True,
        Room.max_guests >= guests
    ).all()

    if not date:
        return {
            "message": "Missing date",
            "status": "error"
        }

    query_date = datetime.strptime(date, "%Y-%m-%d").date()

    available_rooms = []

    for room in rooms:

        # kolla om rummet är bokat på datumet
        overlapping_booking = db.query(Booking).filter(
            Booking.room_id == room.id,
            Booking.start_date <= query_date,
            Booking.end_date >= query_date
        ).first()

        if not overlapping_booking:
            available_rooms.append(room)

    if not available_rooms:
        return {
            "message": "No rooms available for that date.",
            "status": "not_found",
            "rooms": []
        }

    return {
        "message": f"{len(available_rooms)} rooms available.",
        "status": "ok",
        "date": date,
        "guests": guests,
        "rooms": [
            {
                "name": r.name,
                "price": r.base_price,
                "max_guests": r.max_guests
            }
            for r in available_rooms
        ]
    }
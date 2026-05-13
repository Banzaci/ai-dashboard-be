from typing import Optional
from app.models.room import Room  # (eller din egen model)
from datetime import datetime
from app.models.booking import Booking

def availability_flow(
    db,
    guests: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):

    if start_date and not end_date:
        return {
            "message": "For how many nights?",
            "status": "missing_nights"
        }

    if not start_date:
        return {
            "message": "Missing date",
            "status": "error"
        }

    if not guests:
        guests = 1

    query_start = datetime.strptime(start_date, "%Y-%m-%d").date()

    # baseline rooms
    rooms = db.query(Room).filter(
        Room.is_active == True,
        Room.max_guests >= guests
    ).all()

    available_rooms = []

    for room in rooms:

        overlapping_booking = db.query(Booking).filter(
            Booking.room_id == room.id,
            Booking.start_date <= query_start,
            Booking.end_date >= query_start
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
        "date": start_date,
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
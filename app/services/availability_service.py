# app/services/availability_service.py
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, not_, exists

from app.models.room import Room
from app.models.booking import Booking


def search_available_rooms(db: Session, check_in: str, check_out: str, guests: int, rooms: int = 1) -> list[dict]:
    """
    Returnera rum som:
    - är aktiva och inte borttagna
    - har tillräckligt med gäster
    - inte har överlappande bokningar
    """
    check_in_date  = date.fromisoformat(check_in)
    check_out_date = date.fromisoformat(check_out)

    # Subquery – rum som har en överlappande bokning
    overlapping = (
        exists()
        .where(
            and_(
                Booking.room_id == Room.id,
                Booking.status != "cancelled",
                Booking.start_date < check_out_date,
                Booking.end_date > check_in_date,
            )
        )
    )

    available_rooms = (
        db.query(Room)
        .filter(
            Room.is_active == True,
            Room.deleted_at == None,
            Room.max_guests >= guests,
            ~overlapping,
        )
        .all()
    )

    return [
        {
            "id":          room.id,
            "name":        room.name,
            "max_guests":  room.max_guests,
            "base_price":  room.base_price,
            "description": room.description,
            "beds":        room.beds,
            "bathrooms":   room.bathrooms,
        }
        for room in available_rooms
    ]
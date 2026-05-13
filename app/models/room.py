import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name: Mapped[str] = mapped_column(String, nullable=False)

    max_guests: Mapped[int] = mapped_column(Integer, nullable=False)

    base_price: Mapped[float] = mapped_column(Float, nullable=False)

    description: Mapped[str] = mapped_column(String, nullable=False)

    beds: Mapped[int] = mapped_column(Integer, nullable=False)

    bathrooms: Mapped[int] = mapped_column(Integer, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # om du vill ha images senare:
    # images = relationship("RoomImage", back_populates="room")
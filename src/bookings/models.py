# pyright: reportUndefinedVariable=false

from sqlalchemy import UUID, Column, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.tools import uuid_column


class Booking(Base):
    __tablename__ = "bookings"

    id = uuid_column()
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    booker_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    parking_space_id: Mapped[UUID] = mapped_column(
        ForeignKey("parking_spaces.id", ondelete="CASCADE"), nullable=False
    )

    # relationships
    parking_space: Mapped["ParkingSpace"] = relationship(back_populates="bookings")  # type: ignore  # noqa: F821
    booker: Mapped["User"] = relationship(back_populates="bookings")  # type: ignore  # noqa: F821

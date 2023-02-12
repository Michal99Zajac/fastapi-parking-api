# pyright: reportUndefinedVariable=false
from typing import Optional

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class ParkingAddress(Base):
    __tablename__ = "parking_addresses"

    street = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    # relationships
    parkings: Mapped[list["Parking"]] = relationship(back_populates="address")


class Parking(Base):
    __tablename__ = "parkings"

    name = Column(String, nullable=False)
    address_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("parking_addresses.id", ondelete="SET NULL"), nullable=True
    )
    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # relationships
    address: Mapped["ParkingAddress"] = relationship(back_populates="parkings")
    owner: Mapped["User"] = relationship(back_populates="parkings")  # type: ignore # noqa: F821
    spaces: Mapped[list["ParkingSpace"]] = relationship(back_populates="parking")


class ParkingSpace(Base):
    __tablename__ = "parking_spaces"

    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    parking_id: Mapped[UUID] = mapped_column(
        ForeignKey("parkings.id", ondelete="CASCADE"), nullable=False
    )

    # relationships
    parking: Mapped["Parking"] = relationship(back_populates="spaces")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="parking_space")  # type: ignore  # noqa: F821
